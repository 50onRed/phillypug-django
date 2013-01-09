import github3
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import RedirectView, TemplateView
from phillypug.background import redis_client, worker_queue
from phillypug.workers import update_user_repos
from requests_oauth2 import OAuth2

class OAuthMixin(object):
    @property
    def oauth2_handler(self):
        """Returns an OAuth2 client that can deal with authorization and token
        exchange.
        """
        return OAuth2(client_id=settings.GITHUB_CLIENT_ID,
                client_secret=settings.GITHUB_CLIENT_SECRET,
                site=settings.GITHUB_OAUTH_PREFIX,
                redirect_uri=self.request.build_absolute_uri(reverse('oauth:callback')),
                authorization_url=settings.GITHUB_AUTHORIZE_PATH,
                token_url=settings.GITHUB_ACCESS_TOKEN_PATH)

class OAuthLoginView(OAuthMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        """Simply redirects the browser to the gitub authorize url.
        """
        return self.oauth2_handler.authorize_url()

class OAuthCallbackView(OAuthMixin, TemplateView):
    template_name = 'oauth/error.html'

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')

        if code:
            access_token = self._get_access_token(code)
            user = authenticate(github_access_token=access_token)

            if user:
                login(request, user)
                worker_queue.enqueue(update_user_repos, access_token)
                return redirect(reverse('index'))

        return super(OAuthCallbackView, self).get(request, *args, **kwargs)

    def _get_access_token(self, code):
        """Exchanges a code for an access token.
        """
        token = self.oauth2_handler.get_token(code)
        return token['access_token'][0]
