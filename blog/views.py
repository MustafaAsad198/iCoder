from turtle import pos
from django.shortcuts import redirect, render,HttpResponse
from .models import Post,Blogcomment
from django.contrib import messages
from blog.templatetags import extras
from .forms import PostCreateForm
from datetime import datetime
# Create your views here.
def bloghome(request):
    if request.method == 'POST':
        form=PostCreateForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.author=request.user.username
            instance.timestamp=datetime.now()
            instance.save()
            return redirect('bloghome')
    else:
        form=PostCreateForm()
    allposts=Post.objects.all()
    user=request.user
    context={'allposts':allposts,'form':form,'user':user}
    return render(request,'blog/bloghome.html',context)
def blogpost(request,slug):
    post=Post.objects.filter(slug=slug).first()
    post.views=post.views+1
    post.save()
    comments=Blogcomment.objects.filter(post=post,parent=None)
    replies=Blogcomment.objects.filter(post=post).exclude(parent=None)
    print(comments,replies)
    repdict={}
    for reply in replies:
        if reply.parent.sno not in repdict.keys():
            repdict[reply.parent.sno]=[reply]
        else:
            repdict[reply.parent.sno].append(reply)
    print(repdict)
    context={'post':post,'comments':comments,'user':request.user,'repdict':repdict}
    return render(request,'blog/blogpost.html',context)
def postcomment(request):
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=request.user
        postsno=request.POST.get('postsno')
        post=Post.objects.get(sno=postsno)
        parentsno=request.POST.get('parentsno')
        if parentsno=='':
            comment=Blogcomment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,'Your comment has been posted successfully')
        else:
            parent=Blogcomment.objects.get(sno=parentsno)
            comment=Blogcomment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,'Your reply has been posted successfully')
    return redirect(f'/blog/{post.slug}')