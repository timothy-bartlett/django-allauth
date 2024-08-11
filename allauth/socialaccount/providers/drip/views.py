"""Views for Drip API."""

from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class DripOAuth2Adapter(OAuth2Adapter):
    """OAuth2Adapter for Drip API v3."""

    provider_id = "drip"

    authorize_url = "https://www.getdrip.com/oauth/authorize"
    access_token_url = "https://www.getdrip.com/oauth/token"
    profile_url = "https://api.getdrip.com/v2/user"

    def complete_login(self, request, app, token, **kwargs):
        """Complete login, ensuring correct OAuth header."""
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        response = (
            get_adapter().get_requests_session().get(self.profile_url, headers=headers)
        )
        response.raise_for_status()
        extra_data = response.json()["users"][0]
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(DripOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DripOAuth2Adapter)
