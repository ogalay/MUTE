from .models import Forum, Post, Topic
from django import forms


class ForumForm(forms.ModelForm):
    #title = forms.CharField(max_length=60, required=True)

    class Meta:
        model = Forum
        exclude = ('creator', 'updated', 'created', 'closed', 'topic')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('creator', 'updated', 'created', 'user_ip', 'forum', 'rating')


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('description', 'updated', 'created')

