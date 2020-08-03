from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

class NewPage(forms.Form):
    title = forms.CharField(label="title")
    text = forms.CharField(label="text", widget=forms.Textarea)
    # title.widget.attrs.update(size='40')

class EditPage(forms.Form):
    text = forms.CharField(label="text", widget=forms.Textarea)
    
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "text": util.get_entry(title)
    })

def search(request):
    return 1


def edit(request, title):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "form": EditPage(initial={'text': util.get_entry(title)}),
            "title": title
        })
    else:
        form = EditPage(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            util.save_entry(title,text)
            # return HttpResponseRedirect(reverse('page', title))
            return redirect('page', title)
        else:
            return render(request, "encyclopedia/edit.html", {
                'title': title,
                'form': form
            })

def new(request):
    form = NewPage(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        title = form.cleaned_data['title']
        text = form.cleaned_data['text']
        util.save_entry(title, text)
        return redirect('page', title)
    return render(request, "encyclopedia/new.html", {
        'form': NewPage()
    })