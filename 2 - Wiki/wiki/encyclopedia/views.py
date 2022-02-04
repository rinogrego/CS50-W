from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import markdown2
import html

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", required=True, widget=forms.TextInput(attrs={
        "placeholder": "your title",
        'class': 'new-title',
    }))
    entry = forms.CharField(label="Content", required=True, widget=forms.Textarea(attrs={
        "placeholder": "your entry",
        'class': 'new-entry',
    }))

class editForm(forms.Form):
    title = forms.CharField(label="Title", disabled=True, widget=forms.TextInput(attrs={
        "placeholder": "your title",
    }))
    entry = forms.CharField(label="Content", required=False, widget=forms.Textarea(attrs={
        "placeholder": "your entry",
    }))

# I don't understand why the attrs for forms.CharField doesn't work.
# Since no specific criteria for that I will just skip it.

"""
    Note:
    
    'randent' variable in every function so that the 'Random Page' button redirects to the
    correct link/website path that correspond to the appropriate entry instead of a single 
    entry path that display different entry and content.

    Used in layout.html template.
"""

def index(request):
    randent = random.choice(list(util.list_entries()))
    
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            newTitle = form.cleaned_data['title']
            newContent = form.cleaned_data['entry']
            if newTitle in list(util.list_entries()):
                return render(request, "encyclopedia/new-entry-error.html", {
                    "newTitle": newTitle,
                    "randent": randent,
                })
            else:
                util.save_entry(newTitle, newContent)
                return HttpResponseRedirect(f'wiki/{newTitle}')

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "randent": randent,
    })

def title(request, entry):
    randent = random.choice(list(util.list_entries()))

    if request.method == "POST":
        form = editForm(request.POST)
        if not form.is_valid():
            # I use "if not" because title form clashed with what is already exist and form.is_valid()
            # don't give a True value if the data is already exists, in this case, title, because I just
            # make it only able to edit the content and not the title.
            newContent = form.cleaned_data['entry']
            util.save_entry(entry, newContent)            
            return HttpResponseRedirect(reverse('title', args=[entry]))
            #return HttpResponseRedirect(f'{entry}')

    else:
        if util.get_entry(entry):
            # content variable was put here because somehow if I put it 
            # in the beginning of the function it won't work
            # error message: "decoding to str: need a bytes-like object, NoneType found"
            content = markdown2.markdown(util.get_entry(entry))
            return render(request, "encyclopedia/entry.html", {
                "entry": entry,
                "content": content,
                "randent": randent,
            })
        else:
            return render(request, "encyclopedia/PageNotFound.html", {
                "entry": entry,
                "randent": randent,
            })

def edit(request, entry):
    randent = random.choice(list(util.list_entries()))

    content = markdown2.markdown(util.get_entry(entry))
    rawcontent = util.get_entry(entry)
    form = editForm(initial={'title': entry, 'entry': rawcontent})
    return render(request, "encyclopedia/edit-entry.html", {
        "entry": entry,
        "content": content,
        "randent": randent,
        "editForm": form,
        "rawcontent": rawcontent,
    })

def createNewEntry(request):
    randent = random.choice(list(util.list_entries()))

    return render(request, "encyclopedia/CreateNewEntry.html", {
        "titleForm": NewEntryForm(),
        "randent": randent,
    })

def randomPage(request):
    randent = random.choice(list(util.list_entries()))

    randcont = markdown2.markdown(util.get_entry(randent))
    return render(request, "encyclopedia/entry.html", {
        "entry": randent,
        "content": randcont,
        "randent": randent,
    })

def search(request):
    randent = random.choice(list(util.list_entries()))

    searchentry = request.GET.get('q')
    searchentries = []
    for entry in list(util.list_entries()):
        if searchentry.lower() in entry.lower():
            if searchentry.lower() == entry.lower():
                return HttpResponseRedirect(reverse('title', args=[entry]))
            searchentries.append(entry)
    check = True
    if searchentries == []:
        check = False
    return render(request, "encyclopedia/search.html", {
        "entries": searchentries,
        "check": check,
        "randent": randent,
    })

"""
return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "randent": randent,
    })
"""
# SELF-note:
# HttpResponseRedirect(variable), variable can link 
# to designated website path instead of local path

