from django.contrib import admin
from .models import Forum, Topic, Post, ProfaneWord


class TopicAdmin(admin.ModelAdmin):
    pass


class ForumAdmin(admin.ModelAdmin):
    list_display = ["title", "topic", "creator", "created"]
    list_filter = ["topic", "creator"]


class PostAdmin(admin.ModelAdmin):
    search_fields = ["creator"]
    list_display = ["forum", "creator", "created", "rating"]


class ProfaneWordAdmin(admin.ModelAdmin):
    pass


admin.site.register(Topic, TopicAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ProfaneWord, ProfaneWordAdmin)

