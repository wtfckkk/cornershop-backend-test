from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth import views as auth_views

from slack_sdk.oauth import AuthorizeUrlGenerator
from slack_sdk.oauth.state_store import FileOAuthStateStore

from backend_test.settings import SLACK_CLIENT_ID, SLACK_OAUTH_REDIRECT_URI


class LoginView(auth_views.LoginView):
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        state_store = FileOAuthStateStore(expiration_seconds=300, base_dir="./data")
        state = state_store.issue()
        authorize_url_generator = AuthorizeUrlGenerator(
            client_id=SLACK_CLIENT_ID,
            user_scopes=["identity.basic"],
            redirect_uri=SLACK_OAUTH_REDIRECT_URI
        )
        login_slack_url = authorize_url_generator.generate(state)
        context.update({
            'slack_url': login_slack_url,
        })

        return context


class LogoutView(auth_views.LogoutView):
    next_page = "login"


