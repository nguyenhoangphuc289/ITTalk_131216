from django.conf.urls import url
from apps.home.views import *
from django.contrib.auth import views

app_name = 'home'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^welcome/$', welcome, name='welcome'),
    url(r'^welcome/save', welcome_save, name='welcome_save'),
    url(r'^login/$', login, name='login'),
    url(r'^accounts/login/$', welcome, name='inactive'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^question/$', question, name='question'),
    url(r'^question/insert/$', question_insert, name='question_insert'),
    url(r'^schedule/$', schedule, name='schedule'),
    url(r'^detail/(?P<pid>[0-9]+)/$', detail, name='detail'),
    url(r'^post/$', post, name='post'),
    url(r'^post/insert/$', post_insert, name='post_insert'),
    url(r'^ajax/feeds/$', ajax_load_more, name='load_more_feeds'),
    url(r'^ajax/delete/$', ajax_delete_post, name='ajax_delete_post'),
    url(r'^ajax/dislike/$', ajax_downvote_post, name='ajax_downvote_post'),
    url(r'^ajax/undislike/$', ajax_undo_downvote_post, name='ajax_undo_downvote_post'),
    url(r'^ajax/answer/$', ajax_answer_question, name='ajax_answer_question'),
    url(r'^ajax/reply/$', ajax_reply_comment, name='ajax_reply_comment'),
    url(r'^ajax/deletecomment/$', ajax_delete_comment, name='ajax_delete_comment'),
    url(r'^ajax/upvotecomment/$', ajax_upvote_comment, name='ajax_upvote_comment'),
    url(r'^ajax/downvotecomment/$', ajax_downvote_comment, name='ajax_downvote_comment'),
    url(r'^ajax/like/$', ajax_upvote_post, name='ajax_upvote_post'),
    url(r'^ajax/recommendquestion/$', ajax_recommend_question, name='ajax_recommend_question'),
    url(r'^ajax/recommendtopics/$', ajax_recommend_topics, name='ajax_recommend_topics'),
    # url(r'^ajax/info/$', ajax_load_user_info, name='ajax_load_user_info'),
]
