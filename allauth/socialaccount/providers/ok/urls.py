from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import OKProvider

urlpatterns = default_urlpatterns(OKProvider)
