from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, List, Bid, Comment

from django import forms

lis = []
def index(request):
    list = List.objects.filter(is_sold=False)
    return render(request, "auctions/index.html", {
        "list" : list
    })

def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html", {
        "categories": categories
    })
    
def catlist(request, pk):
    categories = Category.objects.filter(pk = pk)
    name = categories[0]
    list = name.list.all()
    return render(request, "auctions/catlist.html", {
        "list": list
        })
    #return HttpResponse("No entry")

class NewItem(forms.ModelForm):
    class Meta:
        model = List
        fields = ('name', 'category', 'description', 'price', 'image')
        
@login_required
def newlist(request):
    if request.method == "POST":
        form = NewItem(request.POST, request.FILES)
        if form.is_valid:
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect("index")
    else:
        form = NewItem()
    return render(request, "auctions/form.html", {
        "form": form
    })

def listing(request, id):
    detail = List.objects.filter(pk = id)
    return render(request, "auctions/detail.html", {
        "detail": detail
    })



@login_required
def watchlist(request):
    
    if request.method == "POST":
        id = request.POST["name"]
        items = get_object_or_404(List, pk=id)
        items.watchlist.add(request.user)
        return render(request, "auctions/watch.html")
    else: 

        return render(request, "auctions/watch.html")
     
@login_required
def remove(request):
    if request.method == "POST":
        id = request.POST["name"]
        items = get_object_or_404(List, pk=id)
        request.user.watch.remove(items)
        return render(request, "auctions/watch.html")

@login_required      
def bid(request, id):
    if request.method == "POST":
        bid = request.POST["number"]
        item = List.objects.filter(pk = id)
        auction = Bid.objects.filter(item = item[0])
        for i in item:
            if float(bid) < i.price:
                return HttpResponse("Bid must bigger than price")
        for  auc in auction:
            if float(bid) < auc.bid:
                return HttpResponse("Bid must be bigger than other bids")
        biding = Bid(user= request.user, item = item[0], bid = bid)
        biding.save()
        return HttpResponseRedirect(reverse("index"))
        
    else: 
        return HttpResponse("No entry")
    
@login_required
def close(request):
    if request.method == "POST":
        id = request.POST["name"]
        item = List.objects.filter(pk = id)
        auction = Bid.objects.filter(item = item[0]).order_by('-bid')
        user = auction[0].user

        close = List.objects.get(pk = id)
        close.is_sold = True
        close.save()


        return render(request, "auctions/close.html", {
        "user": user
        })

        """return render(request, "auctions/detail.html", {
        "user": user
        })"""
@login_required    
def comment(request, id):
    if request.method == "POST":
        comment = request.POST["textarea"]
        item = List.objects.filter(pk = id)
        c = Comment(name= request.user, item = item[0], comment = comment)
        c.save()
        
    return render(request, "auctions/detail.html", {
        "comment": comment
    })

    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
