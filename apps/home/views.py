from contextlib import contextmanager

from django.core import serializers

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.context_processors import csrf
import json

from apps.home import forms

from Core.BLL import *


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    if request.user.is_authenticated():
        user = request.user
        name = user.first_name + " " + user.last_name
        context = {
            'name': name
        }
        return render(request, 'home/index.html', context)
    return render(request, 'home/index.html', "")


def login(request):
    return render(request, 'home/login.html', "")


def inactive(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        UserStatusBLL.Insert(user)


@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def question(request):
    user = request.user
    name = user.first_name + " " + user.last_name
    context = {
        'name': name
    }
    return render(request, 'home/question.html', context)


@login_required(login_url='/login/')
def detail(request, pid):
    user = request.user
    name = user.first_name + " " + user.last_name
    topics = [
        'Python',
        'Django',
        'Open source',
        'Pycharm'
    ]
    postOrQuestion = PostBLL.SelectById(pid)
    answers = CommentBLL.GetCommentsByPostId(pid)
    context = {
        'name': name,
        'topics': topics,
        'post': postOrQuestion,
        'count_answer': len(answers),
        'answers': answers
    }
    return render(request, 'home/detail.html', context)


@login_required(login_url='/login/')
def question_insert(request):
    title = str(request.POST['question_title'])
    isAnonymous = False
    if request.POST.get('is_anonymous', True) == "on":
        isAnonymous = True
    isExpand = request.POST['is_expand']
    content = request.POST['question_detail']
    userId = request.user.id
    if (isExpand == "1"):
        PostBLL.Insert(1, [], title, content, userId, isAnonymous)
    else:
        PostBLL.Insert(1, [], title, "", userId, isAnonymous)

    # NotificationBLL.create_notification(userId)

    return redirect('/detail/' + str(PostBLL.SelectLastQuestion(userId).id))


def schedule(request):
    return render(request, "home/schedule.html", "")


@login_required(login_url='/login/')
def post(request):
    user = request.user
    name = user.first_name + " " + user.last_name
    context = {
        'name': name,
        'form': forms.PostForm
    }
    return render(request, "home/post.html", context)


@login_required(login_url='/login/')
def post_insert(request):
    title = request.POST['title']
    content = request.POST['content']
    # value get from templates
    topics = request.POST['topics']
    # get all topics
    arr = topics.split(',')
    # array contain topics ID
    listTopics = []
    # TopicBLL.Insert(topic) will:
    #   - return id of exist topic
    #   - insert new topic then return id of recent added topic
    for topic in arr:
        listTopics.append(TopicBLL.Insert(topic))
    userId = request.user.id
    PostBLL.Insert(2, listTopics, title, content, userId, 0)

    # NotificationBLL.create_notification(userId)

    return redirect('/detail/' + str(PostBLL.SelectLastPost(userId).id))


@login_required(login_url='/login/')
def ajax_load_more(request):
    if request.is_ajax():
        total = 5
        offset = int(request.GET.get('offset', '0'))
        end = offset + total
        template = 'home/appends/load_more_items.html'
        if (offset < len(PostBLL.SelectAll())):
            feeds = PostBLL.SelectWithoutDownvotePost(request.user.id)[offset:end]
            data = {
                'logged_user_id': request.user.id,
                'posts': feeds,
            }
            data.update(csrf(request))
            return render_to_response(template, data)
        else:
            return render_to_response(template, None)


@login_required(login_url='/login/')
def ajax_delete_post(request):
    if request.is_ajax():
        PostBLL.Delete(request.GET.get('id', '0'))
    return HttpResponse()


@login_required(login_url='/login/')
def ajax_downvote_post(request):
    if request.is_ajax():
        PostBLL.IncreaseDownVote(request.GET.get('id', '0'), request.user.id)
    return HttpResponse()


@login_required(login_url='/login/')
def ajax_undo_downvote_post(request):
    if request.is_ajax():
        PostBLL.DecreaseDownvote(request.GET.get('id', '0'), request.user.id)
    return HttpResponse()


@login_required(login_url='/login/')
def ajax_upvote_post(request):
    if request.is_ajax():
        res = PostBLL.Upvoted(request.GET.get('id', '0'), str(request.user.id))
        if (res == "0"):
            PostBLL.IncreaseUpvote(request.GET.get('id', '0'), request.user.id)
            data = {"status": "up", "count": PostBLL.GetUpvoteCount(request.GET.get('id', '0'))}
            return HttpResponse(json.dumps(data))
        else:
            PostBLL.DecreaseUpvote(request.GET.get('id', '0'), str(request.user.id))
            data = {"status": "unup", "count": PostBLL.GetUpvoteCount(request.GET.get('id', '0'))}
            return HttpResponse(json.dumps(data))
    return HttpResponse()


@login_required(login_url='/login/')
def ajax_answer_question(request):
    if request.is_ajax():
        is_update = request.POST.get('is_update', '0')
        if (is_update == "0"):
            cmt = CommentBLL.InsertComment(request.POST.get('post_id', '0'), request.POST.get('parentid', '0'),
                                           request.user.id, request.POST.get('content', ''))
            template = 'home/appends/parent_comment.html'
            data = {
                'logged_user_id': request.user.id,
                'answer': cmt,
                'post_id': request.POST.get('post_id', '0'),
            }
            data.update(csrf(request))
            return render_to_response(template, data)
        else:
            cmt = CommentBLL.UpdateComment(is_update, request.POST.get('content', ''))
            template = 'home/appends/parent_comment.html'
            data = {
                'logged_user_id': request.user.id,
                'answer': cmt,
                'post_id': request.POST.get('post_id', '0'),
            }
            data.update(csrf(request))
            return render_to_response(template, data)


# def ajax_load_user_info(request):
#     if request.is_ajax():
#         template = 'home/appends/info_hover.html'
#         data = {}
#         return render_to_response(template, data)


@login_required(login_url='/login/')
def welcome(request):
    s = UserStatusBLL.SelectById(request.user.id).status
    if (s == True):
        return redirect('/')
    else:
        user = request.user
        name = user.first_name + " " + user.last_name
        context = {
            'name': name,
            'topics': TopicBLL.SelectAll(),
        }
        return render(request, "home/welcome.html", context)


@login_required(login_url='/login/')
def welcome_save(request):
    try:
        UserStatusBLL.Active(request.user.id)
        return redirect('/')
    except:
        redirect('/')


@login_required(login_url='/login/')
def ajax_reply_comment(request):
    if request.is_ajax():
        rep = CommentBLL.InsertComment(request.POST.get('post_id', '0'), request.POST.get('parent_id', '0'),
                                       request.user.id, request.POST.get('reply_content', ''))
        template = 'home/appends/reply_comment.html'
        data = {
            'reply': rep
        }
        return render_to_response(template, data)


@login_required(login_url='/login/')
def ajax_delete_comment(request):
    if request.is_ajax():
        CommentBLL.DeleteParentComment(request.GET.get('id', '0'))
    return HttpResponse()


@login_required(login_url='/login/')
def ajax_upvote_comment(request):
    if request.is_ajax():
        res = CommentBLL.Liked(request.GET.get('id', '0'), str(request.user.id))
        if (res == "0"):
            CommentBLL.IncreaseUpvote(request.GET.get('id', '0'), str(request.user.id))
            if (CommentBLL.Disliked(request.GET.get('id', '0'), str(request.user.id)) == "1"):
                CommentBLL.DecreaseDownvote(request.GET.get('id', '0'), str(request.user.id))
            data = {"status": "up", "up_count": CommentBLL.CountUpvote(request.GET.get('id', '0')),
                    "down_count": CommentBLL.CountDownvote(request.GET.get('id', '0'))}
            return HttpResponse(json.dumps(data))
        else:
            CommentBLL.DecreaseUpvote(request.GET.get('id', '0'), str(request.user.id))
            data = {"status": "unup", "up_count": CommentBLL.CountUpvote(request.GET.get('id', '0')),
                    "down_count": CommentBLL.CountDownvote(request.GET.get('id', '0'))}
            return HttpResponse(json.dumps(data))


@login_required(login_url='/login/')
def ajax_downvote_comment(request):
    if request.is_ajax():
        res = CommentBLL.Disliked(request.GET.get('id', '0'), str(request.user.id))
        if (res == "0"):
            CommentBLL.IncreaseDownVote(request.GET.get('id', '0'), str(request.user.id))
            if (CommentBLL.Liked(request.GET.get('id', '0'), str(request.user.id)) == "1"):
                CommentBLL.DecreaseUpvote(request.GET.get('id', '0'), str(request.user.id))
            data = {"status": "down", "up_count": CommentBLL.CountUpvote(request.GET.get('id', '0')),
                    "down_count": CommentBLL.CountDownvote(request.GET.get('id', '0'))}
            return HttpResponse(json.dumps(data))
        else:
            CommentBLL.DecreaseDownvote(request.GET.get('id', '0'), str(request.user.id))
            data = {"status": "undown", "up_count": CommentBLL.CountUpvote(request.GET.get('id', '0')),
                    "down_count": CommentBLL.CountDownvote(request.GET.get('id', '0'))}
            return HttpResponse(json.dumps(data))


@login_required(login_url='/login/')
def ajax_recommend_question(request):
    if request.is_ajax():
        query = request.GET.get("query", "")
        data = PostBLL.SearchByQuestion(query)
        return HttpResponse(json.dumps(list(data)))


@login_required(login_url='/login/')
def ajax_recommend_topics(request):
    if request.is_ajax():
        query = request.GET.get("query", "")
        data = TopicBLL.SearchByName(query)
        return HttpResponse(json.dumps(list(data)))
