import markdown2
# import secrets
import random as rand
from django.core.files.base import ContentFile

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util
from markdown2 import Markdown

from django.contrib.auth.models import User
from django.contrib import auth


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title",
                            widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"])
            auth.login(request, user)
            return redirect('')
        return render(request, "encyclopedia/signup.html")
    else:
        return render(request, "encyclopedia/signup.html");



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('')
        else:
            return render(request, 'encyclopedia/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'encyclopedia/login.html')


def logout(request):
    auth.logout(request)
    return redirect('')


def entry(request, entry):
    markdowner = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/notExistingEntry.html", {
            "entries": util.list_entries(),
            "entryTitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(entryPage),
            "entries": util.list_entries(),
            "entryTitle": entry
        })


def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title) is None or form.cleaned_data["edit"] is True:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/newEntry.html", {
                    "form": form,
                    "entries": util.list_entries(),
                    "existing": True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/newEntry.html", {
                "form": form,
                "entries": util.list_entries(),
                "existing": False
            })
    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": NewEntryForm(),
            "entries": util.list_entries(),
            "existing": False
        })


def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/nonExistingEntry.html", {
            "entryTitle": entry,
            "entries": util.list_entries()
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newEntry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial,
            "entries": util.list_entries(),
        })


def random(request):
    entries = util.list_entries()
    randomEntry = rand.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomEntry}))


def search(request):
    value = request.GET.get('q', '')
    if util.get_entry(value) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)

        return render(request, "encyclopedia/notExistingEntry.html", {
            "entries": subStringEntries,
            "search": True,
            "value": value
        })
