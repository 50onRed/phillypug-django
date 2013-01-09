import json
from django.shortcuts import render
from phillypug.background import redis_client

def index(request):
    if request.user.is_anonymous():
        repos = None
    else:
        github_id = request.user.get_profile().github_user.github_id
        repos_key = 'repos:{}'.format(github_id)

        repos = redis_client.get(repos_key)
        if repos:
            repos = json.loads(repos)

    return render(request, 'index.html', {'repos': repos})
