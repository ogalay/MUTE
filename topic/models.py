from django.db import models
from django.conf import settings

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from pytz import unicode


class Topic(models.Model):
    title = models.CharField('Название',max_length=60)
    description = models.TextField(blank=True, default='')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

    # creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.title

    def num_posts(self):
        return sum([t.num_posts() for t in self.forum_set.all()])

    def last_post(self):
        if self.forum_set.count():
            last = None
            for t in self.forum_set.all():
                l = t.last_post()
                if l:
                    if not last:
                        last = l
                    elif l.created > last.created:
                        last = l
            return last


class Forum(models.Model):
    title = models.CharField('Название',max_length=60)
    description = models.TextField('Описание',max_length=10000, blank=True, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(blank=True, default=False)

    def num_posts(self):
        return self.post_set.count()

    def num_replies(self):
        return max(0, self.post_set.count() - 1)

    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by("created")[0]

    def __unicode__(self):
        return unicode(self.creator) + " - " + self.title


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    body = models.TextField('Текст сообщения', max_length=10000)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    rating = models.IntegerField(blank=True, default=0, null=True)


class ProfaneWord(models.Model):
    word = models.CharField(max_length=60)

    def __unicode__(self):
        return self.word
