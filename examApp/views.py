from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import*
import bcrypt

def index(request):
    return render (request, "index.html")

def register(request):
    print(request.POST)
    errors = User.objects.basic_validator(request.POST)
    if errors:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        print(messages.error)
        return redirect('/')

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)

    this_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'], password=pw_hash)
    request.session['user_id'] = this_user.id
    return redirect('/quotes')


def quotes(request):
    
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "quotes": Quote.objects.all()
    }
    return render(request, "main.html", context)


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/quotes')

    messages.error(request, "invalid login")

    return redirect('/')


def logout(request):
    del request.session['user_id']
    return redirect('/')


def addQuote(request):
    
    errors = Quote.objects.basic_validator(request.POST)
    if errors:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        print(messages.error)
        return redirect('/quotes')
    
    if "user_id" not in request.session:
        return redirect('/')
    this_user = User.objects.get(id = request.session['user_id'])
    this_quote = Quote.objects.create(author = request.POST['author'], quote = request.POST['quote'], uploaded_by = this_user)
    print(request.POST)
    return redirect('/quotes')

def delete(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    deleteMe = Quote.objects.get(id = id)
    if deleteMe.uploaded_by.id != request.session['user_id']:
        return redirect('/quotes')
    deleteMe.delete()
    return redirect('/quotes')

def posterQuotes(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id = id),
        "quotes": Quote.objects.all()
    }
    return render (request, "allPosts.html", context)

def likeQuote(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    this_quote = Quote.objects.get(id = id)
    this_user = User.objects.get(id = request.session ['user_id'])
    
    this_quote.liked_quote.add(this_user)
    return redirect('/quotes')

def updatePage(request, id):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id = id)
    }
    return render(request, "editMyAccount.html", context)

def editMyAccount(request, id):
    errors = User.objects.update_validator(request.POST)
    if errors:
        print(errors)
        for key, value in errors.items():
            messages.error(request, value)
        print(messages.error)
        return redirect('/quotes')
    
    if "user_id" not in request.session:
        return redirect('/')
    this_user = User.objects.get(id = id)
    this_user.first_name = request.POST['first_name']
    this_user.last_name = request.POST['last_name']
    this_user.email = request.POST['email']
    this_user.save()
    return redirect(f'/quotes')