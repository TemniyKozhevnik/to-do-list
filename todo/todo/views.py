from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from todo.models import ToDo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method=='POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('email')
        pwd = request.POST.get('pwd')
        my_user = User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
        return redirect('/login')
    return render(request, 'signup.html')


def loginn(request):
    if request.method=='POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request, userr)
            return redirect('/todopage')
        else:
            return redirect('/login')
    return render(request, 'login.html')


@login_required(login_url='/login')
def todo(request):
    if request.method=='POST':
        title = request.POST.get('title')
        todo = ToDo(user=request.user, title=title)
        todo.save()
        res = ToDo.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage', {'res': res})
    res = ToDo.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})


@login_required(login_url='/login')
def edit_todo(request, srno):
    user = request.user
    if request.method=='POST':
        title = request.POST.get('title')
        obj = ToDo.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todopage', {'obj': obj})
    obj = ToDo.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})


@login_required(login_url='/login')
def delete_todo(request, srno):
    obj = ToDo.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')


def signout(request):
    logout(request)
    return redirect('/login')
