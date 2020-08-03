from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import random
from markdown2 import Markdown


class NewPage(forms.Form):
    title = forms.CharField(label="title")
    text = forms.CharField(label="text", widget=forms.Textarea)
    # title.widget.attrs.update(size='40')

class EditPage(forms.Form):
    text = forms.CharField(label="text", widget=forms.Textarea)

class SearchForm(forms.Form):
    query = forms.CharField(label='search')
    
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    markdowner = Markdown()
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "text": markdowner.convert(util.get_entry(title))
    })

def search(request, query=None):
    form = SearchForm(request.POST or None)
    if query is not None:
        form.query = query
    if request.method == "POST" and form.is_valid():
        query = form.cleaned_data['query']
        if query in util.list_entries():
            return redirect('page', query)
        else:
            matching = [s for s in util.list_entries() if query in s]
            return render(request, 'encyclopedia/search.html', {
                'form': SearchForm(initial={'query': query}),
                'found': matching
            })
    else:
        return render(request, "encyclopedia/search.html", {
            'form': SearchForm()
        })



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

def random_page(request):
    return redirect('page', random.choice(util.list_entries()))