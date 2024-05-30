from django.urls import path
from a_post.views import (index,post_create_view, post_delete_view, post_edit_view,post_page_view, comment_sent,
                        comment_delete_view, reply_sent, reply_delete_view,
                        like_post, like_comment, like_reply)
urlpatterns = [
    path('',index, name='index'),
    path('category/<tag>/',index, name='category'),
    path('post/create/',post_create_view,name='post-create'),
    path('post/delete/<pk>/',post_delete_view,name='post-delete'),
    path('post/edit/<pk>/',post_edit_view,name='post-edit'),
    path('post/page/view/<pk>/',post_page_view,name='post'),
    path('commentsent/<pk>/', comment_sent, name='comment-sent'),
    path('comment/delete/<pk>', comment_delete_view, name='comment-delete'),
    path('reply-sent/<pk>/', reply_sent, name='reply-sent'),
    path('reply/delete/<pk>/', reply_delete_view, name='reply-delete'),
    path('post/like/<pk>/',like_post,name='like-post'),
    path('comment/like/<pk>/',like_comment,name='like-comment'),
    path('reply/like/<pk>/',like_reply,name='like-reply'),
]
