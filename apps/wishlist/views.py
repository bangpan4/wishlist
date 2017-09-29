from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Wishlist
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'wishlist/index.html')

def create(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            newuser = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=password, date=request.POST['hire_date'])
            newuser.save()
    return redirect('/')

def login(request):
    user_check = User.objects.filter(username=request.POST['username'])
    for user in user_check:
        if user.username == request.POST['username'] and bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/dashboard')
        else:
            messages.add_message(request, messages.ERROR, "Invalid username or password")
            return redirect('/')

def dashboard(request):
    if 'user_id' in request.session:
        loginuser = User.objects.get(id=request.session['user_id'])
        items = Wishlist.objects.filter(creator=loginuser)
        otheritems = Wishlist.objects.exclude(creator=loginuser) 
        context = {
            'user': loginuser,
            'items': items,
            'otheritems': otheritems,

        }
        return render(request,"wishlist/dashboard.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def additem(request):
    return render(request, 'wishlist/add.html')

def createitem(request):
    if request.method == 'POST':
        errors = User.objects.wish_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/wishlist/add')
        else:
            newitem = Wishlist.objects.create(item=request.POST['item'], creator = User.objects.get(id=request.session['user_id']))
            newitem.save()
    return redirect('/dashboard')

def item(request, item_id):
    item = Wishlist.objects.get(id=item_id)
    users = Wishlist.objects.filter(item=item.item)
    for user in users:
        print user.creator.name
    context = {
        'item': item,
        'users': users
    }
    return render(request, 'wishlist/item.html', context)

def delete(request, item_id):
    itemtodelete = Wishlist.objects.get(id=item_id).item
    Wishlist.objects.filter(item=itemtodelete).delete()
    return redirect('/dashboard')

def addlist (request, item_id):
    the_item = Wishlist.objects.get(id = item_id)
    the_user = User.objects.get(id = request.session['user_id'])
    the_item.want.add(the_user)
    return redirect('/dashboard')
    print item.item