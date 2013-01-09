import github3
from django.contrib.auth.models import User
from account.models import GithubUser

class GithubBackend(object):
    def authenticate(self, github_access_token):
        # first try to get the user from github using our access token
        try:
            gh = github3.login(token=github_access_token)
            gh_user = gh.user()
        except:
            return None

        # next, either retrieve or create the user in our system
        try:
            github_user = GithubUser.objects.get(github_id=gh_user.id)
        except GithubUser.DoesNotExist:
            github_user = GithubUser.objects.create_user(gh_user)

        # update the access token
        github_user.access_token = github_access_token
        github_user.save()

        # grab the real User object (that Django basically heavily depends on)
        return github_user.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
