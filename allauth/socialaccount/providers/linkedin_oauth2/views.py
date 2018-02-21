import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import LinkedInOAuth2Provider


class LinkedInOAuth2Adapter(OAuth2Adapter):
    provider_id = LinkedInOAuth2Provider.id
    access_token_url = 'https://api.linkedin.com/uas/oauth2/accessToken'
    authorize_url = 'https://www.linkedin.com/uas/oauth2/authorization'
    profile_url = 'https://api.linkedin.com/v1/people/~'
    # See:
    # http://developer.linkedin.com/forum/unauthorized-invalid-or-expired-token-immediately-after-receiving-oauth2-token?page=1 # noqa
    access_token_method = 'GET'

    def complete_login(self, request, app, token, **kwargs):
        extra_data = self.get_user_info(token)
        return self.get_provider().sociallogin_from_response(
            request, extra_data)

    def get_user_info(self, token):
        fields = self.get_provider().get_profile_fields()
        url = self.profile_url + ':(%s)?format=json' % ','.join(fields)
        resp = requests.get(url,
                            headers={'Authorization': ' '.join(('Bearer',
                                     token.token)), 'x-li-src': 'msdk'})
        return resp.json()


oauth2_login = OAuth2LoginView.adapter_view(LinkedInOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(LinkedInOAuth2Adapter)
