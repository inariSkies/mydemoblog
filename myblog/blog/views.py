from django.http import HttpResponse, HttpResponseRedirect 
from .models import Post, Author
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_object_or_404,render
from django.utils import timezone

#loads the home page, with the newest dated post at the top
def index(request):
    latest_post_list=Post.objects.order_by('-pub_date')[:30] 
    template=loader.get_template('blog/index.html')
    new_pk = Post.objects.order_by('-id')[0] #getting a new post pk in case a new post is created
    new_pk_id=new_pk.id
    new_pk_id += 1 
    context = {
        'latest_post_list':latest_post_list,
        'new_pk_id':new_pk_id,
    }
    new_pk=Post.objects.order_by('-id')[0]
    return HttpResponse(template.render(context, request))

#calls post.html passing post id
def post(request, post_id):
    postdex=get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post.html', {'post':postdex})

#calls edit.html passing post id
def edit(request, post_id):
    editpost=get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/edit.html', {'post':editpost})

#calls new.html passing post id
def new(request, post_id):
    template=loader.get_template('blog/new.html')
    context ={
        'post_id':post_id
    }
    return HttpResponse(template.render(context, request))

#calls author.html passing post id
def author(request, post_id):
    author_post=get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/author.html', {'post':author_post})


#used to persit and edit, and a new post. Creates an author if one does not exist
def publish(request, post_id):
    try:
        select_post=Post.objects.get(pk=post_id) #check to see if post id exists
    except (KeyError, Post.DoesNotExist): #post doesn't exist
        try:
            A=Author.objects.filter(author_name=request.POST['author']).get()#check to see if author id exists
        except (KeyError, Author.DoesNotExist):#author doesn't exist
            A=Author.objects.create(author_name=request.POST['author'],author_bio=request.POST['bio']) #creates author
            A.save()
            return publish(request, post_id) #recalls function with the author now added to the datebase
        else: #author does exist
            newpost=Author.objects.get(pk=A.id)
            newpost.post_set.all()
            newpost.post_set.create(post_title =request.POST['title'],post_desc=request.POST['desc'], pub_date=timezone.now())
            newpost.save() #new post is saved
            return HttpResponseRedirect(reverse('blog:index'))
    else: #post does exist
        select_post.post_title =request.POST['title']
        select_post.post_desc =request.POST['desc']
        select_post.pub_date=timezone.now()
        select_post.save() #edited post is saved
        return HttpResponseRedirect(reverse('blog:index'))