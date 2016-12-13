from django import template
from Core.BLL import *
from bs4 import BeautifulSoup
from lxml import html
import re

register = template.Library()


@register.filter(name='get_avatar')
def get_avatar(userId):
    return PostBLL.GetAvatar(userId)


@register.filter(name='get_fullname')
def get_fullname(userId):
    return PostBLL.GetFullName(userId)


@register.filter(name='get_first_image')
def get_first_image(content):
    tree = BeautifulSoup(content)
    return (tree.find_all('img')[0]['src'])


@register.filter(name='has_image')
def has_image(content):
    tree = BeautifulSoup(content)
    img = tree.find('img')
    if img is not None:
        return "1"
    return "0"


@register.filter(name='convert_content')
def convert_content(content):
    p = re.compile(r'<img.*?/>')
    content_no_image = p.sub('', content)
    doc = html.fromstring(content_no_image)
    return doc.text_content()


@register.filter(name='get_followers')
def get_followers(subcribers):
    if (str(subcribers) == "" or subcribers is None):
        return 0
    else:
        return len(str(subcribers).split(','))


@register.filter(name='get_answers')
def get_answers(postId):
    return CommentBLL.GetCommentsByPostId(postId)


@register.filter(name='get_replies')
def get_replies(cmtParentsId):
    return CommentBLL.GetReply(cmtParentsId)


@register.filter(name='liked')
def liked(arg):
    arr = arg.split(',')
    return CommentBLL.Liked(arr[1], arr[0])


@register.filter(name='disliked')
def disliked(arg):
    arr = arg.split(',')
    return CommentBLL.Disliked(arr[1], arr[0])


@register.filter(name='count_upvote')
def count_upvote(arg):
    return CommentBLL.CountUpvote(arg)


@register.filter(name='count_downvote')
def count_downvote(arg):
    return CommentBLL.CountDownvote(arg)


@register.filter(name='upvote_post_count')
def upvote_post_count(arg):
    return PostBLL.GetUpvoteCount(arg)


@register.filter(name='upvoted_post')
def upvoted_post(arg):
    arr = arg.split(',')
    return PostBLL.Upvoted(arr[1], arr[0])
