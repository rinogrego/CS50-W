document.addEventListener("DOMContentLoaded", () => {

  console.log("Masuk ke home")

  document.querySelector('#new-post-form').onsubmit = function() {
    // const author_ = document.querySelector('#postAuthor').value;
    const content_ = document.querySelector('#postText').value;
    fetch('/posts', {
      method: 'POST',
      body: JSON.stringify({
        // author: `${author_}`,
        content: `${content_}`,
      }),
    })
    .then(async response => {
      try {
        const data = await response.json();
        console.log('Response data? ', data);
      } catch(error) {
        console.log('Error happened here!');
        console.log(error);
      }
    })
    document.querySelector('#postText').value = "";
    // return false;
  }

  ////// activating function
  //// if user haven't like the post
  // dislike_button()
  //// if user likes the post
  // like_button()
  

})


function send_post(author_, content_) {

  fetch('/posts', {
    method: 'POST',
    body: JSON.stringify({
      author: `${author_}`,
      content: `${content_}`,
    }),
    // headers: {
    //   'Accept': 'application/json',
    //   'Content-Type': 'application/json',
    // }
  })
  .then(async response => {
    try {
      const data = await response.json();
      console.log('Response data? ', data);
    } catch(error) {
      console.log('Error happened here!');
      console.log(error);
    }
  })

}


function like() {

}

function dislike() {

}


// Seems this isn't needed
function like_button(post_id, url_target) {

  fetch(`/post/${post_id}`, {
    method: "GET"
  })
  .then(async response => {
    try {
      const data = await response.json();
      console.log('Response data? ', data);
    } catch(error) {
      console.log('Error happened here!');
      console.log(error);
    }
  })

  var post_likes_count = document.getElementById(`post-${post_id}-like-count`).innerHTML;
  var new_value = parseInt(post_likes_count) + 1;
  
  // alert(`new_value: ${new_value}`);
  document.getElementById(`post-${post_id}-like-count`).innerHTML = new_value;

  document.querySelector(`#like-${post_id}-a-tag`).setAttribute('onclick', `send_dislike( ${post_id}, "${url_target}" );`);

  document.querySelector(`#like-${post_id}-button-svg`).setAttribute('fill', 'red');
  document.querySelector(`#like-${post_id}-button-svg-path-line`).style.display='none'; 
  document.querySelector(`#like-${post_id}-button-svg-path-fill`).style.display='block';

  document.querySelector(`#like-${post_id}-button-svg`).setAttribute("onmouseover", `
  document.querySelector("#like-${post_id}-button-svg").setAttribute('fill', 'red');
  document.querySelector("#like-${post_id}-button-svg").className = "bi bi-heart mt-2 w-25 float-right like-button-svg-YES";
  document.querySelector("#like-${post_id}-button-svg-path-line").style.display='none'; 
  document.querySelector("#like-${post_id}-button-svg-path-fill").style.display='block';`);

  document.querySelector(`#like-${post_id}-button-svg`).setAttribute("onmouseout", `
  document.querySelector("#like-${post_id}-button-svg").setAttribute('fill', 'red');
  document.querySelector("#like-${post_id}-button-svg-path-line").style.display='none'; 
  document.querySelector("#like-${post_id}-button-svg-path-fill").style.display='block';`);

  // document.querySelector(`#like-${post_id}-button-svg`).setAttribute("onclick", 'dislike_button()');

}


// Seems this isn't needed
function dislike_button(post_id, url_target) {

  fetch(`/post/${post_id}`, {
    method: "GET"
  })
  .then(async response => {
    try {
      const data = await response.json();
      console.log('Response data? ', data);
      console.log(data.likes)

    } catch(error) {
      console.log('Error happened here!');
      console.log(error);
    }
  })

  var post_likes_count = document.getElementById(`post-${post_id}-like-count`).innerHTML;
  var new_value = parseInt(post_likes_count) - 1;
  // alert(`new_value: ${new_value}`);
  
  document.getElementById(`post-${post_id}-like-count`).innerHTML = new_value;

  document.querySelector(`#like-${post_id}-a-tag`).setAttribute('onclick', `send_like( ${post_id}, "${url_target}" );`);

  document.querySelector(`#like-${post_id}-button-svg`).setAttribute('fill', 'gray');
  document.querySelector(`#like-${post_id}-button-svg-path-line`).style.display='block'; 
  document.querySelector(`#like-${post_id}-button-svg-path-fill`).style.display='none';
  
  document.querySelector(`#like-${post_id}-button-svg`).setAttribute("onmouseover", `
  document.querySelector("#like-${post_id}-button-svg").setAttribute('fill', 'red');
  document.querySelector("#like-${post_id}-button-svg").className = "bi bi-heart mt-2 w-25 float-right like-button-svg-NOT";
  document.querySelector('#like-${post_id}-button-svg-path-line').style.display='none'; 
  document.querySelector('#like-${post_id}-button-svg-path-fill').style.display='block';`);

  document.querySelector(`#like-${post_id}-button-svg`).setAttribute("onmouseout", `
  document.querySelector('#like-${post_id}-button-svg').setAttribute('fill', 'gray');
  document.querySelector('#like-${post_id}-button-svg-path-line').style.display='block'; 
  document.querySelector('#like-${post_id}-button-svg-path-fill').style.display='none';`);

  // document.querySelector(`#like-${post_id}-button-svg`).setAttribute("onclick", 'like_button()');

}


function edit_post(post_id) {

  const content = document.querySelector(`#post-${post_id}-content-value`).innerHTML;
  document.querySelector(`#edit-post-${post_id}-textarea`).value = content;
  
  document.querySelector(`#post-${post_id}-content`).style.display = "none";
  document.querySelector(`#post-${post_id}-form`).style.display = "block";
}


function cancel_edit_post(post_id) {
  console.log('cancel edit post:', post_id);

  document.querySelector(`#post-${post_id}-content`).style.display = "block";
  document.querySelector(`#post-${post_id}-form`).style.display = "none";
}


function send_edit(post_id) {

  // Taking the new value and put to show the new content in the user's browser
  const new_content = document.querySelector(`#edit-post-${post_id}-textarea`).value;
  document.querySelector(`#post-${post_id}-content-value`).innerHTML = new_content;

  // Closing the form, redisplaying content
  document.querySelector(`#post-${post_id}-content`).style.display = "block";
  document.querySelector(`#post-${post_id}-form`).style.display = "none";

}

// $(function () {
//   $(`post-${post.id}-form`).submit(function(event) {
//     event.preventDefault();
//     var new_content = $(this);
//     // saving new_content
//     var editing = $.post( new_content.attr(), new_content.serialize() );
//     // if success
//     editing.done(function(data) {
//       console.log(data);
//     })
//     // if fails
//     editing.fail(function(data) {
//       console.log('edit fail')
//     })
//   })
// })

// $(document).on('submit', `#post-${post.id}-form`, function(e){
//   e.preventDefault();
//   $.ajax({
//     type: 'POST',
//     url: '{% url "edit" post.id %}',
//     data: {
//       content: $(`#edit-post-${post_id}-textarea`).val(),
//       csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
//     },
//     success: function(){
//       alert('Saved!');
//     }
//   })
// });

/* <script type="text/javascript">
    $(document).ready(function() {
        $('#form_id').submit(function() { // On form submit event
            $.ajax({ // create an AJAX call...
                data: $(this).serialize(), // get the form data
                type: $(this).attr('method'), // GET or POST
                url: $(this).attr('action'), // the file to call
                success: function(response) { // on success..
                    $('#success_div').html(response); // update the DIV
                },
                error: function(e, x, r) { // on error..
                    $('#error_div').html(e); // update the DIV
                }
            });
            return false;
        });
    });
</script> */