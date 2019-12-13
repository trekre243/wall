from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from the_wall_app.models import User, Message, Comment
import bcrypt
from datetime import datetime, timedelta

def login(request):
    if 'id' in request.session:
        return redirect('/wall')
    return render(request, 'login.html')

def check_login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, 'Not a valid email address')
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['id'] = user.id
        request.session.save()
        return redirect('/wall')
    else:
        messages.error(request, 'Incorrect password')
        return redirect('/')

def register(request):
    errors =User.objects.user_validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        hash_pass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(fname=fname, lname=lname, password=hash_pass, email=email)
        request.session['id'] = user.id
        request.session.save()
        return redirect('/wall')

def wall(request):
    if 'id' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('/')

    user = User.objects.get(id=request.session['id'])

    thirty_min_ago = timezone.now() - timedelta(minutes=30)

    tmessages = Message.objects.all()
    for message in tmessages:
        message.recent = message.created_at >= thirty_min_ago

    context = {
        'messages': tmessages,
        'user': user,
    }
    return render(request, 'wall.html', context)

def create_message(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    message = request.POST['message']
    Message.objects.create(user_id=user, message=message)
    return redirect('/wall')

def post_comment(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    tmessage = Message.objects.get(id=int(request.POST['message_id']))
    comment = request.POST['comment']
    Comment.objects.create(user_id=user, message_id=tmessage, comment=comment)
    return redirect('/wall')

def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)
    if 'id' in request.session:
        if request.session['id'] == message.user_id.id and message.created_at >= timezone.now() - timedelta(minutes=30):
            message.delete()
    return redirect('/wall')

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    context = {
        'fname': user.fname
    }
    return render(request, 'success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')
