from django.shortcuts import render
from . import util
import markdown2
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, title):
    if title in util.list_entries():
        entry = util.get_entry(title)
        convert = markdown2.markdown(entry)
        return render(request, "encyclopedia/title.html", {
            "title": title,
            "content": convert
        })
    return HttpResponse("Page not found")

def search(request):
    if request.method == "POST":
        title = request.POST['q']
        if title in util.list_entries():
            entry = util.get_entry(title)
            convert = markdown2.markdown(entry)
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "content": convert
            })
        else:
            list = []
            for word in util.list_entries():
                if title in word:
                    list.append(word)
            return render(request, "encyclopedia/search.html", {
                "list": list
            })
    return HttpResponse("No match item")

def newpage(request):
    return render(request, "encyclopedia/new.html")

def save(request):
    if request.method == "POST":
        title = request.POST["text"]
        content = request.POST["Content"]
        if title in util.list_entries():
            return HttpResponse("Title is exist")
        else:
            saved = util.save_entry(title, content)
            return HttpResponseRedirect(reverse("title", args=(title,)))
        
def edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = util.get_entry(title) 
        return render(request, "encyclopedia/edit.html", {
                    "title": title,
                    "content": content
                })
    
def saveedit(request):
    if request.method == "POST":
        title = request.POST["text"]
        content = request.POST["Content"]
        saved = util.save_entry(title, content)
        return HttpResponseRedirect(reverse("title", args=(title,)))

def rand(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("title", args=(title,)))
