from Core.models import *
from django.db.models import *
from django.db.models.functions import *
from django.db.models.query import *
from datetime import datetime
from firebase import firebase
from django.conf import settings


# FIREBASE_URL = settings.FIREBASE_URL


class PostDAL(object):
    @staticmethod
    def SelectAll():
        return Post.objects.all()

    @staticmethod
    def SelectByPostId(postId):
        return Post.objects.get(pk=postId)

    @staticmethod
    def SelectByTypeId(typeId):
        return Post.objects.filter(type_id=typeId)

    @staticmethod
    def SelectByTopic(topicId):
        return Post.objects.filter(topics__contains=topicId)

    @staticmethod
    def SelectQuestionByUserId(userId):
        return Post.objects.filter(user_id=userId).filter(type_id=1).order_by('-id')

    @staticmethod
    def SelectPostByUserId(userId):
        return Post.objects.filter(user_id=userId).filter(type_id=2).order_by('-id')

    @staticmethod
    def IncreaseUpvote(postId, userId):
        p = Post.objects.get(pk=postId)
        if (p.up_votes == ""):
            p.up_votes += str(userId)
        else:
            p.up_votes += "," + str(userId)
        p.save()

    @staticmethod
    def DecreaseUpvote(postId, userId):
        p = Post.objects.get(pk=postId)
        arr = p.up_votes.split(',')
        p.up_votes = ""
        arr.remove(userId)
        for str in arr:
            p.up_votes += str + ','
        p.up_votes = p.up_votes[:-1]
        p.save()

    @staticmethod
    def IncreaseDownVote(postId, userId):
        p = Post.objects.get(pk=postId)
        if (p.down_votes == ""):
            p.down_votes += str(userId)
        else:
            p.down_votes += "," + str(userId)
        p.save()

    @staticmethod
    def DecreaseDownvote(postId, userId):
        p = Post.objects.get(pk=postId)
        if ("," not in p.down_votes and p.down_votes != ""):
            p.down_votes = ""
        else:
            arr = p.down_votes.split(',')
            p.down_votes = ""
            arr.remove(userId)
            for str in arr:
                p.down_votes += str
            p.down_votes = p.down_votes[:-1]
        p.save()

    @staticmethod
    def IncreaseView(postId):
        p = Post.objects.get(pk=postId)
        p.view_count += 1
        p.save()

    @staticmethod
    def Insert(typeId, topics, title, content, userId, isAnonymous):
        p = Post(type_id=typeId, topics=topics, title=title, content=content, user_id=userId, view_count=0, up_votes=0,
                 down_votes=0, date_created=datetime.now(), is_anonymous=isAnonymous)
        p.save()

    @staticmethod
    def Update(postId, content):
        p = Post.objects.get(pk=postId)
        p.content = content
        p.save()

    @staticmethod
    def Delete(postId):
        p = Post.objects.get(pk=postId)
        p.delete()

    @staticmethod
    def Upvoted(postId, userId):
        p = Post.objects.get(pk=postId)
        if (p.up_votes == ""):
            return "0"
        elif ("," not in p.up_votes and p.up_votes != userId):
            return "0"
        elif (p.up_votes == userId):
            return "1"
        else:
            arr = p.up_votes.split(',')
            for str in arr:
                if str == userId:
                    return "1"
        return "0"

    @staticmethod
    def GetUpvoteCount(postId):
        p = Post.objects.get(pk=postId)
        if (p.up_votes == ""):
            return 0
        elif ("," not in p.up_votes):
            return 1
        else:
            arr = p.up_votes.split(',')
            return len(arr)

    @staticmethod
    def SearchByQuestion(query):
        return Post.objects.filter(type_id=1).filter(title__contains=query).values('id', 'title')


class PostTypeDAL(object):
    @staticmethod
    def SelectAll():
        return PostType.objects.all()

    @staticmethod
    def SelectById(typeId):
        return PostType.objects.get(pk=typeId)


class SocialAuthUsersocialAuthDAL(object):
    @staticmethod
    def SelectByUserId(userId):
        return SocialAuthUsersocialauth.objects.get(user_id=userId)


class AuthUserDAL(object):
    @staticmethod
    def GetUser(userId):
        return AuthUser.objects.get(id=userId)

    @staticmethod
    def GetSubcribers(userId):
        return UserFollower.objects.all().exclude(followed_user_id=userId)


# class NotificationDAL(object):
#     @staticmethod
#     def send_notifications(subscribers, notification_markup):
#         context = {'markup': notification_markup}
#         fb = firebase.FirebaseApplication(FIREBASE_URL, None)
#
#         for user in subscribers:
#             url = '/' + user.id + '/'
#
#             try:
#                 fb.post(url, context)
#
#             except Exception as e:
#                 print e
#                 print 'Firebase Notification not sent'

class CommentDAL(object):
    @staticmethod
    def InsertComment(postId, parentCmtId, userId, content):
        cmt = Comment(post_id=postId, parent_comment_id=parentCmtId, user_id=userId, content=content,
                      up_votes="", down_votes="", created_date=datetime.now(), status=1)
        cmt.save()
        return cmt

    @staticmethod
    def UpdateComment(cmtId, content):
        cmt = Comment.objects.get(pk=cmtId)
        cmt.content = content
        cmt.save()
        return cmt

    @staticmethod
    def GetCommentsByPostId(postId):
        return Comment.objects.filter(post_id=postId).filter(parent_comment_id=0)

    @staticmethod
    def GetReply(cmtParentsId):
        return Comment.objects.filter(parent_comment_id=cmtParentsId)

    @staticmethod
    def GetCommentById(cmtId):
        return Comment.objects.get(pk=cmtId)

    @staticmethod
    def DeleteParentComment(cmtId):
        childs = Comment.objects.filter(parent_comment_id=cmtId)
        for cmt in childs:
            cmt.delete()
        this = Comment.objects.get(pk=cmtId)
        this.delete()

    @staticmethod
    def DeleteComment(cmtId):
        this = Comment.objects.get(pk=cmtId)
        this.delete()

    @staticmethod
    def IncreaseUpvote(cmtId, userId):
        c = Comment.objects.get(pk=cmtId)
        c.up_votes += str(userId) + ","
        c.up_votes = c.up_votes[:-1]
        c.save()

    @staticmethod
    def DecreaseUpvote(cmtId, userId):
        c = Comment.objects.get(pk=cmtId)
        arr = c.up_votes.split(',')
        c.up_votes = ""
        arr.remove(userId)
        for str in arr:
            c.up_votes += str + ','
        c.up_votes = c.up_votes[:-1]
        c.save()

    @staticmethod
    def IncreaseDownVote(cmtId, userId):
        c = Comment.objects.get(pk=cmtId)
        c.down_votes += str(userId) + ","
        c.down_votes = c.down_votes[:-1]
        c.save()

    @staticmethod
    def DecreaseDownvote(cmtId, userId):
        c = Comment.objects.get(pk=cmtId)
        if ("," not in c.down_votes and c.down_votes != ""):
            c.down_votes = ""
        else:
            arr = c.down_votes.split(',')
            c.down_votes = ""
            arr.remove(userId)
            for str in arr:
                c.down_votes += str
            c.down_votes = c.down_votes[:-1]
        c.save()

    @staticmethod
    def Liked(cmtId, userId):
        c = Comment.objects.get(pk=cmtId)
        if (c.up_votes == ""):
            return "0"
        elif ("," not in c.up_votes and c.up_votes != userId):
            return "0"
        elif (c.up_votes == userId):
            return "1"
        else:
            arr = c.up_votes.split(',')
            for str in arr:
                if str == userId:
                    return "1"
        return "0"

    @staticmethod
    def Disliked(cmtId, userId):
        c = Comment.objects.get(pk=cmtId)
        if (c.down_votes == ""):
            return "0"
        elif ("," not in c.down_votes and c.down_votes != userId):
            return "0"
        elif (c.down_votes == userId):
            return "1"
        else:
            arr = c.down_votes.split(',')
            for str in arr:
                if str == userId:
                    return "1"
        return "0"

    @staticmethod
    def CountUpvote(cmtId):
        c = Comment.objects.get(pk=cmtId)
        if (c.up_votes == ""):
            return 0
        elif ("," not in c.up_votes):
            return 1
        else:
            arr = c.up_votes.split(',')
            return len(arr)

    @staticmethod
    def CountDownvote(cmtId):
        c = Comment.objects.get(pk=cmtId)
        if (c.down_votes == ""):
            return 0
        elif ("," not in c.down_votes):
            return 1
        else:
            arr = c.down_votes.split(',')
            return len(arr)


class TopicDAL(object):
    @staticmethod
    def SelectAll():
        return Topic.objects.all()

    @staticmethod
    def GetTopicByName(name):
        return Topic.objects.filter(topic_name=name)

    @staticmethod
    def Insert(name):
        t = Topic(topic_name=name)
        t.save()
        return t

    @staticmethod
    def SearchByName(query):
        return Topic.objects.filter(topic_name__contains=query).values('id', 'topic_name')


class UserStatusDAL(object):
    @staticmethod
    def Insert(user):
        u = UserStatus(user_id=user.id, status=0)
        u.save()

    @staticmethod
    def IsExist(userId):
        obj = UserStatus.objects.filter(user_id=userId)
        if (len(obj) > 0):
            return True
        else:
            return False

    @staticmethod
    def SelectById(userId):
        return UserStatus.objects.get(pk=userId)

    @staticmethod
    def Active(userId):
        u = UserStatus.objects.get(pk=userId)
        u.status = 1
        u.save()
