from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

class GithubUserManager(models.Manager):
    def create_user(self, github_user):
        user = User(username=github_user.login, first_name=github_user.name)
        user.save()

        github_user = GithubUser(user=user, github_id=github_user.id,
                login=github_user.login, name=github_user.name,
                avatar_url=github_user.avatar_url)
        github_user.save()

        user_profile = UserProfile(user=user, github_user=github_user)
        user_profile.save()

        return github_user

class GithubUser(models.Model):
    user = models.ForeignKey(User, unique=True)
    github_id = models.IntegerField(unique=True)
    access_token = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255)

    objects = GithubUserManager()

    def __unicode__(self):
        return self.login

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    github_user = models.ForeignKey(GithubUser, unique=True)

    def __unicode__(self):
        return unicode(self.user)

admin.site.register(GithubUser)
admin.site.register(UserProfile)
