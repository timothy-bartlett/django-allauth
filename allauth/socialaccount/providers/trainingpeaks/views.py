import requests

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import TrainingPeaksProvider


class TrainingPeaksOauth2Adapter(OAuth2Adapter):
    # https://github.com/TrainingPeaks/PartnersAPI/wiki/OAuth
    provider_id = TrainingPeaksProvider.id

    def get_settings(self):
        """ Provider settings """
        return app_settings.PROVIDERS.get(self.provider_id, {})

    def get_hostname(self):
        """ Return hostname depending on sandbox seting """
        settings = self.get_settings()
        if (settings.get('USE_PRODUCTION')):
            return 'trainingpeaks.com'
        return 'sandbox.trainingpeaks.com'

    @property
    def access_token_url(self):
         return "https://oauth." + self.get_hostname() + "/oauth/token"

    @property
    def authorize_url(self):
        return "https://oauth." + self.get_hostname() + "/OAuth/Authorize"

    @property
    def profile_url(self):
        return "https://api." + self.get_hostname() + "/v1/athlete/profile"
    
    # https://oauth.sandbox.trainingpeaks.com/oauth/deauthorize


    scope_delimiter = " "

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "Bearer {0}".format(token.token)}
        response = requests.get(self.profile_url, headers=headers)
        extra_data = response.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(TrainingPeaksOauth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(TrainingPeaksOauth2Adapter)
