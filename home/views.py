import imp
from operator import le
from turtle import title
from unicodedata import name
from xml.sax import make_parser
from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from .jwt_utils import generate_jwt_token
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    allposts=Post.objects.all()
    context={'allposts':allposts}
    return render(request,'home/home.html',context)
def about(request):
    return render(request,'home/about.html')
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        if len(name)<2 or len(email)<6 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Please fill up the form correctly')
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,'Your Details have been submitted successfully')
    return render(request,'home/contact.html')
def search(request):
    query=request.GET['query']
    if len(query)>50:
        allposts=Post.objects.none()
    else:
        allpoststitle=Post.objects.filter(title__icontains=query)
        allpostscontent=Post.objects.filter(content__icontains=query)
        allposts=allpoststitle.union(allpostscontent)
    if allposts.count()==0:
        messages.warning(request, 'No Search Results')
    params={'allposts':allposts,'query':query}
    return render(request,'home/search.html',params)
def handlesignup(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if len(username)>20:
            messages.error(request,'Your Username length limit is exceeding 20 characters.')
            return redirect('home')
        if not username.isalnum():
            messages.error(request,'Your Username should contain only letters or numbers or both (no special characters).')
            return redirect('home')
        if pass1!=pass2:
            messages.error(request,'Your set password and confirmation password do not match.')
            return redirect('home')
        if User.objects.filter(username=username):
            messages.error(request,'Username already exists')
            return redirect('home')
        

        myuser=User.objects.create_user(username,email,pass1)
        token = generate_jwt_token(myuser.id)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,'Congratulations! Your iCoder account has been successfully created! 🎉')
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')
def handlelogin(request):
    if request.method=='POST':
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpass']
        user=authenticate(username=loginusername,password=loginpass)
        if user is not None:
            token = generate_jwt_token(user.id)
            login(request,user)
            messages.success(request,'You have successfully logged in!')
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials. Please try again.')
            return redirect('home')
    return HttpResponse('404 - Not Found')
def handlelogout(request):
    logout(request)
    messages.success(request,'You have successfully logged out!')
    return redirect('home')
