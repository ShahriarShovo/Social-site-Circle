from django.contrib import admin
from a_post.models import Post, Tags, Comment, Reply, LikedPost,LikedComment,LikedReply

# Register your models here.
admin.site.register(Post)
admin.site.register(Tags)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(LikedPost)
admin.site.register(LikedReply) 
