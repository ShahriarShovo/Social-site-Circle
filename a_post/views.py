from django.shortcuts import render,redirect,get_object_or_404
from a_post.models import Post,Tags, Comment, Reply
from django.forms import ModelForm
from django import forms
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.

def index(request,tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag=get_object_or_404(Tags,slug=tag)
    else:
        posts = Post.objects.all()
        
    categories = Tags.objects.all()
   
        
    context={
        'posts':posts,
        'categories':categories,
        'tag':tag,
    }
    return render(request, 'a_post/home.html',context)

    

#-------------------------------------------------------------
################### Forms ####################################
class PostCreateForm(ModelForm):
    class Meta:
        model=Post
        fields=['url','body','tags']
        labels={
            'body': 'Caption',
            'tags':'Category',
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows':3, 'placeholder':'Add a caption ...', 'class':'font1 text-4xl'}),
            'url': forms.TextInput(attrs={'placeholder':'Add url ...'}),
            'tags':forms.CheckboxSelectMultiple(),
        }
        
        
class PostEditForm(ModelForm):
    class Meta:
        model=Post
        fields=['body','tags']
        labels={
            'body': '',
            'tags':'Category',
        }
        
        widgets = {
            'body' : forms.Textarea(attrs={'rows':3, 'placeholder':'Edit caption ...', 'class':'font1 text-4xl'}),
            'tags':forms.CheckboxSelectMultiple(),
        }
        
class CommentCreateForm(ModelForm):
    class Meta:
        model=Comment
        fields=['body']
        
        labels={
            'body': '',
        }
        
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder':'Add comment ...'}),
        }
        
class ReplyCreateForm(ModelForm):
    class Meta:
        model=Reply
        fields=['body']
        
        labels={
            'body': '',
        }
        
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder':'Add reply ...','class':"!text-sm"}),
        }
        


        
###################################################################
        
        
        
        
@login_required
def post_create_view(request):
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')
            find_image=sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            image =find_image[0]['content']
            post.image = image
            
            find_title =sourcecode.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title=title
            
            find_artist = sourcecode.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist=artist
            post.author = request.user
            
            post.save()
            form.save_m2m()
            
        
            return redirect('index')
    return render(request,'a_post/post_create.html',{'form':form})

@login_required
def post_delete_view(request,pk):
    post = get_object_or_404(Post,id=pk, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post Deleted')
        return redirect('index')
    
    return render(request, 'a_post/post_delete.html',{'post':post})

@login_required
def post_edit_view(request,pk):
    post = get_object_or_404(Post,id=pk)
    form = PostEditForm(instance=post)
    
    
    if request.method == 'POST':
        form = PostEditForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'Post updated')
            return redirect('index')
    
    context={
        'post':post,
        'form':form
        }
        
    return render(request,'a_post/post_edit.html',context)


def post_page_view(request,pk):
    post = get_object_or_404(Post,id=pk)
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()
    
    context={
        'post':post,
        'commentform' :commentform,
        'replyform': replyform
    }
    return render(request, 'a_post/post_page.html', context)

@login_required
def comment_sent(request,pk):
    
    post = get_object_or_404(Post, id=pk)
    replyform = ReplyCreateForm()
    
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            
    context={
        'comment': comment,
        'post':post,
        'replyform':replyform
    }
            
    return render(request,'snippets/add_comment.html',context)


@login_required
def comment_delete_view(request,pk):
    post = get_object_or_404(Comment,id=pk, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Comment Deleted')
        return redirect('post', post.parent_post.id)
    
    return render(request, 'a_post/comment_delete.html',{'comment':post})


# @login_required
# def reply_sent(request,pk):
#     comment = get_object_or_404(Comment, id=pk)
#     replyform = ReplyCreateForm()
#     if request.method == 'POST':
#         form = ReplyCreateForm(request.POST)
#         if form.is_valid():
#             reply = form.save(commit=False)
#             reply.author = request.user
#             reply.parent_comment = comment
#             reply.save()
            
#     context= {
#         'comment': comment,
#         'reply':reply,
#         'replyform':replyform,
#         }
            
#     return render(request,'snippets/add_reply.html',context)

@login_required 
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replyform = ReplyCreateForm()
    
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment            
            reply.save()
            
    context = {
        'reply' : reply,
        'comment': comment,
        'replyform': replyform
    }

    return render(request, 'snippets/add_reply.html', context)


@login_required
def reply_delete_view(request,pk):
    reply = get_object_or_404(Reply,id=pk, author=request.user)
    
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply Deleted')
        return redirect('post', reply.parent_comment.parent_post.id)
    
    return render(request, 'a_post/reply_delete.html',{'reply':reply})


def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            # print('kwargs++++++++++++++++++', kwargs)
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exist= post.likes.filter(username=request.user.username).exists()
            if post.author != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
            return func(request, post)
        return wrapper
    return inner_func
            
    
@login_required
@like_toggle(Post)
def like_post(request, post):
    return render(request, 'snippets/likes.html', {'post':post} )

@login_required
@like_toggle(Comment)
def like_comment(request, post):
    return render(request, 'snippets/like_comment.html', {'comment':post} )

@login_required
@like_toggle(Reply)
def like_reply(request, post):
    return render(request, 'snippets/like_reply.html', {'reply':post} )


    
