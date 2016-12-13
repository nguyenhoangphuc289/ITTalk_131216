from Core.DAL import *
from django.template.loader import render_to_string


class PostBLL(object):
    @staticmethod
    def Insert(typeId, arrTopics, title, content, userId, isAnonymous):
        topics = ""
        for topic in arrTopics:
            topics = topics + str(topic) + ","
        topics = topics[:len(topics) - 1]
        PostDAL.Insert(typeId, topics, title, content, userId, isAnonymous)

    @staticmethod
    def SelectLastQuestion(userId):
        return PostDAL.SelectQuestionByUserId(userId)[0]

    @staticmethod
    def SelectLastPost(userId):
        return PostDAL.SelectPostByUserId(userId)[0]

    @staticmethod
    def SelectAll():
        return PostDAL.SelectAll().order_by('-id', '-date_created')

    @staticmethod
    def SelectWithoutDownvotePost(userId):
        result = []
        for post in PostDAL.SelectAll().order_by('-id', '-date_created'):
            if (str(userId) not in post.down_votes):
                result.append(post)
        return result

    @staticmethod
    def GetAvatar(userId):
        return "http://graph.facebook.com/%s/picture?type=large" % SocialAuthUsersocialAuthDAL.SelectByUserId(
            userId).uid

    @staticmethod
    def GetFullName(userId):
        user = AuthUserDAL.GetUser(userId)
        return user.first_name + " " + user.last_name

    @staticmethod
    def SelectById(postId):
        return PostDAL.SelectByPostId(postId)

    @staticmethod
    def Delete(postId):
        PostDAL.Delete(postId)

    @staticmethod
    def IncreaseUpvote(postId, userId):
        PostDAL.IncreaseUpvote(postId, userId)

    @staticmethod
    def DecreaseUpvote(postId, userId):
        PostDAL.DecreaseUpvote(postId, userId)

    @staticmethod
    def IncreaseDownVote(postId, userId):
        PostDAL.IncreaseDownVote(postId, userId)
        if (PostDAL.Upvoted(postId, userId) == "1"):
            PostDAL.DecreaseUpvote(postId, userId)

    @staticmethod
    def DecreaseDownvote(postId, userId):
        PostDAL.DecreaseDownvote(postId, userId)

    @staticmethod
    def GetUpvoteCount(postId):
        return PostDAL.GetUpvoteCount(postId)

    @staticmethod
    def Upvoted(postId, userId):
        return PostDAL.Upvoted(postId, userId)

    @staticmethod
    def SearchByQuestion(query):
        return PostDAL.SearchByQuestion(query)


class AuthUserBLL(object):
    @staticmethod
    def GetSubcribers(userId):
        return


#
# class NotificationBLL(object):
#     @staticmethod
#     def create_notification(userId):
#         subscribers = AuthUserDAL.GetSubcribers(userId)
#         context = {
#             'model': AuthUserDAL.GetUser(userId),
#             'frontend_uri': '/app/#/posts'
#         }
#         notification_markup = render_to_string('home/notifications/post_notification.html', context)
#
#         NotificationDAL.send_notifications(subscribers, notification_markup)


class CommentBLL(object):
    @staticmethod
    def InsertComment(postId, parentCmtId, userId, content):
        return CommentDAL.InsertComment(postId, parentCmtId, userId, content)

    @staticmethod
    def UpdateComment(cmtId, content):
        return CommentDAL.UpdateComment(cmtId, content)

    @staticmethod
    def GetCommentsByPostId(postId):
        return CommentDAL.GetCommentsByPostId(postId).order_by('-id')

    @staticmethod
    def GetReply(cmtParentsId):
        return CommentDAL.GetReply(cmtParentsId).order_by('-id')

    @staticmethod
    def GetCommentById(cmtId):
        return CommentDAL.GetCommentById(cmtId)

    @staticmethod
    def DeleteParentComment(cmtId):
        CommentDAL.DeleteParentComment(cmtId)

    @staticmethod
    def DeleteComment(cmtId):
        CommentDAL.DeleteComment(cmtId)

    @staticmethod
    def IncreaseUpvote(cmtId, userId):
        CommentDAL.IncreaseUpvote(cmtId, userId)

    @staticmethod
    def DecreaseUpvote(cmtId, userId):
        CommentDAL.DecreaseUpvote(cmtId, userId)

    @staticmethod
    def IncreaseDownVote(cmtId, userId):
        CommentDAL.IncreaseDownVote(cmtId, userId)

    @staticmethod
    def DecreaseDownvote(cmtId, userId):
        CommentDAL.DecreaseDownvote(cmtId, userId)

    @staticmethod
    def Liked(cmtId, userId):
        return CommentDAL.Liked(cmtId, userId)

    @staticmethod
    def Disliked(cmtId, userId):
        return CommentDAL.Disliked(cmtId, userId)

    @staticmethod
    def CountUpvote(cmtId):
        return CommentDAL.CountUpvote(cmtId)

    @staticmethod
    def CountDownvote(cmtId):
        return CommentDAL.CountDownvote(cmtId)


class TopicBLL(object):
    @staticmethod
    def SelectAll():
        return TopicDAL.SelectAll()

    @staticmethod
    def GetTopicByName(name):
        return TopicDAL.GetTopicByName(name)

    @staticmethod
    def Insert(name):
        t = TopicDAL.GetTopicByName(name)
        if t == None or len(t) == 0:
            return TopicDAL.Insert(name)
        else:
            return t[0].id

    @staticmethod
    def SearchByName(query):
        return TopicDAL.SearchByName(query)


class UserStatusBLL(object):
    @staticmethod
    def Insert(user):
        if (UserStatusDAL.IsExist(user.id) == False):
            UserStatusDAL.Insert(user)

    @staticmethod
    def SelectById(userId):
        return UserStatusDAL.SelectById(userId)

    @staticmethod
    def Active(userId):
        UserStatusDAL.Active(userId)
