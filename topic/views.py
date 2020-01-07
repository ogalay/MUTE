from django.contrib.auth.decorators import login_required
from django.forms import models as forms_models
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template.context_processors import csrf
from django.urls import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from MUTE.settings import FORUMS_PER_PAGE, REPLIES_PER_PAGE
from account.models import CustomUser
from .models import Forum, Topic, Post
from .forms import PostForm, ForumForm, TopicForm
from django.template import RequestContext
from django.conf import settings


def index(request):
    """Main listing."""
    topics = Topic.objects.all()
    return render_to_response("../templates/list.html", {'topics': topics,
                                            'user': request.user}, RequestContext(request))


def add_csrf(request, **kwargs):
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d


def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items


def topic(request, topic_id):
    """Listing of topics in a forum."""
    forums = Forum.objects.filter(topic=topic_id).order_by("-created")
    forums = mk_paginator(request, forums, FORUMS_PER_PAGE)

    topic = get_object_or_404(Topic, pk=topic_id)

    return render_to_response("topic.html",
                              add_csrf(request, forums=forums, pk=topic_id, topic=topic), RequestContext(request))


def forum(request, forum_id):
    """Listing of posts in a topic."""
    posts = Post.objects.filter(forum=forum_id).order_by("created")
    posts = mk_paginator(request, posts, REPLIES_PER_PAGE)
    forum = Forum.objects.get(pk=forum_id)
    return render_to_response("forum.html", add_csrf(request, posts=posts, pk=forum_id,
                                                     forum=forum), RequestContext(request))


@login_required
def post_reply(request, forum_id):
    form = PostForm()
    forum = Forum.objects.get(pk=forum_id)
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = Post()
            post.forum = forum
            post.body = request.POST['body']
            post.creator = request.user
            post.user_ip = request.META['REMOTE_ADDR']

            post.save()

            return HttpResponseRedirect(reverse('topic:forum-detail', args=(forum.id,)), RequestContext(request))

    return render_to_response('reply.html', add_csrf(request, form=form, pk=forum_id, forum=forum),
                              RequestContext(request))


@login_required
def new_forum(request, topic_id):
    form = ForumForm()
    topic1 = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        form = ForumForm(request.POST)

        if form.is_valid():
            forum1 = Forum()
            forum1.title = form.cleaned_data['title']
            forum1.description = form.cleaned_data['description']
            forum1.topic = topic1
            forum1.creator = request.user

            forum1.save()

            return HttpResponseRedirect(reverse('topic:topic-detail', args=(topic_id,)), RequestContext(request))

    return render_to_response('new-forum.html', add_csrf(request, form=form, pk=topic_id, topic=topic1),
                              RequestContext(request))


def post_delete(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        a = post.forum.pk
        post.delete()
        return HttpResponseRedirect(reverse('topic:forum-detail', args=(a,)), RequestContext(request))
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Post's not found</h2>")


def forum_delete(request, forum_id):
    try:
        forum = Forum.objects.get(pk=forum_id)
        a = forum.topic.pk
        forum.delete()
        return HttpResponseRedirect(reverse('topic:topic-detail', args=(a,)), RequestContext(request))
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Topic's not found</h2>")


def topic_delete(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
        topic.delete()
        return HttpResponseRedirect(reverse('topic:topic-index'), RequestContext(request))
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Topic's not found</h2>")


def post_edit(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)

        if request.method == "POST":
            post.body = request.POST.get("body")
            post.save()
            return HttpResponseRedirect(reverse('topic:forum-detail', args=(post.forum.pk,)), RequestContext(request))
        else:
            return render_to_response("post-edit.html", add_csrf(request, post=post, pk=post_id))
    except Post.DoesNotExist:
        return HttpResponseNotFound("<h2>Post not found</h2>")


def forum_edit(request, forum_id):
    try:
        forum = Forum.objects.get(pk=forum_id)

        if request.method == "POST":
            forum.title = request.POST.get("title")
            forum.description = request.POST.get("description")
            forum.save()
            return HttpResponseRedirect(reverse('topic:topic-detail', args=(forum.topic.pk,)), RequestContext(request))
        else:
            return render_to_response("forum-edit.html", add_csrf(request, forum=forum, pk=forum_id))
    except Forum.DoesNotExist:
        return HttpResponseNotFound("<h2>Forum not found</h2>")


def new_topic(request):
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():
            topic = Topic()
            topic.title = form.cleaned_data['title']
            topic.save()
        return HttpResponseRedirect(reverse('topic:topic-index'), RequestContext(request))

    return render_to_response("new_topic.html", add_csrf(request, form=form),
                              RequestContext(request))


def topic_edit(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)

        if request.method == "POST":
            topic.title = request.POST.get("title")
            topic.save()
            return HttpResponseRedirect(reverse('topic:topic-index'), RequestContext(request))
        else:
            return render_to_response("topic-edit.html", add_csrf(request, topic=topic, pk=topic_id),
                                      RequestContext(request))
    except Topic.DoesNotExist:
        return HttpResponseNotFound("<h2>Topic not found</h2>")


def like(request, post_id):
    post = Post.objects.get(pk=post_id)
    creator = CustomUser.objects.get(pk=post.creator.pk)
    user = CustomUser.objects.get(pk=request.user.pk)
    if user.rating < 5:
        if user.hated_mus_genre == creator.hated_mus_genre:
            creator.rating += 1
            post.rating += 1
        else:
            creator.rating -= 1

            post.rating -= 1
    elif user.rating >= 5 & user.rating < 25:
        if user.hated_mus_genre == creator.hated_mus_genre:
            creator.rating += 3
            post.rating += 3
        else:
            creator.rating -= 3
            post.rating -= 3
    elif user.rating >= 25 & user.rating < 50:
        if user.hated_mus_genre == creator.hated_mus_genre:
            creator.rating += 5
            post.rating += 5
        else:
            creator.rating -= 5
            post.rating -= 5
    elif user.rating >= 50 & user.rating < 75:
        if user.hated_mus_genre == creator.hated_mus_genre:
            creator.rating += 7
            post.rating += 7
        else:
            creator.rating -= 7
            post.rating -= 7
    elif user.rating >= 75:
        if user.hated_mus_genre == creator.hated_mus_genre:
            creator.rating += 10
            post.rating += 10
        else:
            creator.rating -= 1
            post.rating -= 1
    creator.save()
    post.save()
    return HttpResponseRedirect(reverse('topic:forum-detail', args=(post.forum.pk,)), RequestContext(request))
