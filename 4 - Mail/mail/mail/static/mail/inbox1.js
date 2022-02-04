document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email('new') );

  // By default, load the inbox
  let email = document.querySelector('h2').innerHTML;
  //alert(`Hello, ${email}!`);
  load_mailbox('inbox');
});

function compose_email(email_id) {
  
  var email_id = parseInt(email_id);

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails-list').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-content').style.display = 'none';

  if (isNaN(email_id)) {

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

  } else {

    // fetch API to open and read it
    fetch(`emails/${email_id}`, {
      method: 'GET',
    })
    .then(response => response.json())
    .then(email => {

      // Put the data into HTML
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-recipients').disabled = true;
      var prefill_subject = `${email.subject}`;
      // if the email is an initial reply
      if (prefill_subject.indexOf('Re: ') !== 0){
        prefill_subject = `Re: ${email.subject}`
      };
      document.querySelector('#compose-subject').value = prefill_subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: "${email.body}"`;

    });

  };

  // Sending an email
  document.querySelector('form').onsubmit = function() {
    const recipients_ = document.querySelector('#compose-recipients').value;
    const subject_ = document.querySelector('#compose-subject').value;
    const body_ = document.querySelector('#compose-body').value;

    alert("Sending email...");
    send_mail(recipients_, subject_, body_);
    // Self-Note: views.compose already ran in the function above
    // somehow it ran again if I didn't put return false here, if I am getting it correctly.
    load_mailbox('sent');
    return false;
  };

}

function load_mailbox(mailbox) {

  // Removing pre-created emails if exists and re-create the div
  var emailobj = document.getElementById("emails-list");
  emailobj.remove();
  var emails_obj = document.createElement('div');
  emails_obj.setAttribute("id", "emails-list");
  document.getElementsByClassName("container")[0].append(emails_obj);

  // Fetch email data
  get_emails(mailbox);
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#emails-list').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}


// Send email function
function send_mail(recipients_, subject_, body_) {

  // Fetch the API
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: `${recipients_}`,
      subject: `${subject_}`,
      body: `${body_}`,
    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    //console.log(result);
  });
}

// GET mailbox function
function get_emails(mailbox) {

  // Fetch the API
  fetch(`/emails/${mailbox}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(emails => {
    
      // Print emails
      console.log(emails);

      // ... do something else with emails ...
      emails.forEach(emails => {

        // Creating HTML structure for emails list in mailbox
        const email_element = document.createElement('div');
        email_element.className = 'email';

        // Add archive/unarchive button
        const bea = document.createElement('div');
        bea.id = 'bea';

        // CSS initial setting
        bea.style.zIndex = '-48';

        if(mailbox === 'inbox' || mailbox === 'archive') {

          const bea_button = document.createElement('button');

          bea_button.setAttribute('onmouseover', "this.parentNode.style.animationPlayState = 'paused'; this.nextSibling.firstChild.firstChild.style.backgroundColor = 'lightblue'; ");
          bea_button.setAttribute('onmouseout', "this.parentNode.style.animationPlayState = 'running'; ");

          if(mailbox === 'inbox'){
            bea_button.setAttribute('onclick', `archive_email(${emails.id});`);
            bea_button.innerHTML = 'Archive this email';
          } else {
            bea_button.setAttribute('onclick', `unarchive_email(${emails.id});`);
            bea_button.innerHTML = 'Unarchive this email';
          };
          
          bea.appendChild(bea_button);
          
        };
        email_element.appendChild(bea);

        const from_container_element = document.createElement('div');
        const from_area_element = document.createElement('div');
        const from_element = document.createElement('div');

        from_container_element.className = 'from-container';
        from_area_element.className = 'from-area';
        from_element.className = 'from';

        from_area_element.innerHTML = 'From';
        from_element.innerHTML = emails.sender;

        const subject_container_element = document.createElement('div');
        const subject_area_element = document.createElement('div');
        const subject_element = document.createElement('div');

        subject_container_element.className = 'subject-container';
        subject_area_element.className = 'subject-area';
        subject_element.className = 'subject';

        subject_area_element.innerHTML = 'Subject';
        subject_element.innerHTML = emails.subject;

        const timestamp_container_element = document.createElement('div');
        const timestamp_area_element = document.createElement('div');
        const timestamp_element = document.createElement('div');

        const email_preview_element = document.createElement('div');
        email_preview_element.className = 'email-preview';

        timestamp_container_element.className = 'time-stamp-container';
        timestamp_area_element.className = 'time-stamp-area';
        timestamp_element.className = 'time-stamp';

        timestamp_area_element.innerHTML = 'Timestamp';
        timestamp_element.innerHTML = emails.timestamp;

        email_preview_element.appendChild(from_container_element);
        from_container_element.appendChild(from_area_element);
        from_container_element.appendChild(from_element);

        email_preview_element.appendChild(subject_container_element);
        subject_container_element.appendChild(subject_area_element);
        subject_container_element.appendChild(subject_element);
        
        email_preview_element.appendChild(timestamp_container_element);
        timestamp_container_element.appendChild(timestamp_area_element);
        timestamp_container_element.appendChild(timestamp_element);

        email_element.appendChild(bea);
        // entah kenapa email_element.appendChild(bea); kehapus di HTML browser...

        // Add button-like functionality
        const a = document.createElement('a');
        const span = document.createElement('span');

        a.setAttribute('onclick', `get_email(${emails.id}); return false;`);
        a.setAttribute('href', '');
        a.setAttribute('style', "text-decoration-line: none; color: black;");

        span.appendChild(email_preview_element);
        a.appendChild(span);

        email_element.appendChild(a);
        document.querySelector('#emails-list').append(email_element);

        // Change background color if the email is already read
        email_preview_element.setAttribute('onmouseover', "this.style.backgroundColor = 'lightblue'; this.parentNode.parentNode.previousSibling.style.animationName = 'beamove'; this.parentNode.parentNode.previousSibling.style.animationDuration = '0.5s'; this.parentNode.parentNode.previousSibling.style.animationFillMode = 'forwards'; this.parentNode.parentNode.previousSibling.style.animationIterationCount = '1'; this.parentNode.parentNode.previousSibling.style.animationPlayState = 'running';");
        if (emails.read === true){
          email_preview_element.style.backgroundColor = 'gray';
          email_preview_element.setAttribute('onmouseout', "this.style.backgroundColor = 'gray'; this.parentNode.parentNode.previousSibling.style.animationName = 'beamove2'; this.parentNode.parentNode.previousSibling.style.animationDuration = '0.5s';");
        } else {
          email_preview_element.style.backgroundColor = 'white';
          email_preview_element.setAttribute('onmouseout', "this.style.backgroundColor = 'white'; this.parentNode.parentNode.previousSibling.style.animationName = 'beamove2'; this.parentNode.parentNode.previousSibling.style.animationDuration = '0.5s';");
        };
      });
  });
};

// GET email function
function get_email(email_id) {
  
  // Show the email name
  document.querySelector('#emails-view').innerHTML = `<h3>Email</h3>`;

  // Hide mailboxes
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#emails-list').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'block';
  
  // fetch API to change the read status to true
  fetch(`emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      read: true
    })
  })
  .catch(error => {
    console.log('Error: ', error);
  });
  
  // fetch API to open and read it
  fetch(`emails/${email_id}`, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(email => {

    // Print email
    console.log(email);

    // Put the data into HTML
    document.querySelector('#from-email').innerHTML = email.sender;
    document.querySelector('#recipients-email').innerHTML = email.recipients;
    document.querySelector('#subject-email').innerHTML = email.subject;
    document.querySelector('#time-stamp-email').innerHTML = email.timestamp;
    document.querySelector('#body-email').innerHTML = email.body;
    
    // reply button functionality
    document.querySelector('#reply-button').addEventListener('click', () => compose_email(email.id));

  })
  .catch(error => {
    console.log('Error: ', error);
  });
}

// Archiving email function
function archive_email(email_id) {
  
  // fetch API
  fetch(`emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true,
    })
  })
  .then(load_mailbox('inbox'));
}

// Unarchiving email function
function unarchive_email(email_id) {
  
  // fetch API
  fetch(`emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false,
    })
  })
  .then(load_mailbox('inbox'));
}

// Reply Email function
function reply_email(email_id) {

  // fetch API to open and read it
  fetch(`emails/${email_id}`, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(email => {

    // Put the data into HTML
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-recipients').disabled = true;
    var prefill_subject = `${email.subject}`;
    // if the email is an initial reply
    if (prefill_subject.indexOf('Re: ') !== 0){
      prefill_subject = `Re: ${email.subject}`
    };
    document.querySelector('#compose-subject').value = prefill_subject;
    document.querySelector('#compose-subject').disabled = true;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;

  });
}