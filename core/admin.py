from django.contrib import admin

from core.models import Post, Tag, PostLike

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(PostLike)
