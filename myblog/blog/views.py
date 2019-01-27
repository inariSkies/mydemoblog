from django.http import HttpResponse, HttpResponseRedirect 
from .models import Post, Author
from django.urls import reverse
from django.template import loader
from django.shortcuts import get_object_or_404,render
from django.utils import timezone

def index(request):
    latest_post_list=Post.objects.order_by('-pub_date')[:30]
    template=loader.get_template('blog/index.html')
    new_pk = Post.objects.order_by('-id')[0]
    new_pk_id=new_pk.id
    new_pk_id += 1
    context = {
        'latest_post_list':latest_post_list,
        'new_pk_id':new_pk_id,
    }
    new_pk=Post.objects.order_by('-id')[0]
    return HttpResponse(template.render(context, request))

def post(request, post_id):
    postdex=get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post.html', {'post':postdex})

def edit(request, post_id):
    editpost=get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/edit.html', {'post':editpost})

def new(request, post_id):
    #newpost=get_object_or_404(Post, pk=post_id)
    template=loader.get_template('blog/new.html')
    context ={
        'post_id':post_id
    }
    return HttpResponse(template.render(context, request))

def author(request, author_id):
   return HttpResponse("Author: %s" %author_id)

def publish(request, post_id):
    try:
        select_post=Post.objects.get(pk=post_id)
    except (KeyError, Post.DoesNotExist):
        try:
            A=Author.objects.filter(author_name=request.POST['author']).get()
        except (KeyError, Author.DoesNotExist):
            A=Author.objects.create(author_name=request.POST['author'],author_bio="enter a bio")
            A.save()
            return publish(request, post_id)
        else:
            newpost=Author.objects.get(pk=A.id)
            newpost.post_set.all()
            newpost.post_set.create(post_title =request.POST['title'],post_desc=request.POST['desc'], pub_date=timezone.now())
            newpost.save()
            return HttpResponseRedirect(reverse('blog:index'))
    else:
        select_post.post_title =request.POST['title']
        select_post.post_desc =request.POST['desc']
        select_post.pub_date=timezone.now()
        select_post.save()
        return HttpResponseRedirect(reverse('blog:index'))