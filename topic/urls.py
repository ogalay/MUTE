from django.conf.urls import url
from django.urls import path

from topic.views import *

app_name = 'topic'
urlpatterns = [
    path('', index, name='topic-index'),
    path('<int:topic_id>/', topic, name='topic-detail'),
    path('forum/<int:forum_id>/', forum, name='forum-detail'),
    path('reply/<int:forum_id>/', post_reply, name='reply'),
    path('newforum/<int:topic_id>/', new_forum, name='new-forum'),
    path('post_delete/<int:post_id>/', post_delete, name='post-delete'),
    path('forum_delete/<int:forum_id>/', forum_delete, name='forum-delete'),
    path('topic_delete/<int:topic_id>/', topic_delete, name='topic-delete'),
    path('post_edit/<int:post_id>/', post_edit, name='post-edit'),
    path('forum_edit/<int:forum_id>/', forum_edit, name='forum-edit'),
    path('topic_edit/<int:topic_id>/', topic_edit, name='topic-edit'),
    path('new_topic/', new_topic, name='new_topic'),
    path('like/<int:post_id>/', like, name='like')
]
