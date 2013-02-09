class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, dflt):
        from django.conf import settings
        return getattr(settings, self.prefix + name, dflt)

    @property
    def QUERY_EMAIL(self):
        """
        Request e-mail address from 3rd party account provider? 
        E.g. using OpenID AX
        """
        from allauth.account import app_settings as account_settings
        return self._setting("QUERY_EMAIL", 
                             account_settings.EMAIL_REQUIRED)

    @property
    def AUTO_SIGNUP(self):
        """
        Attempt to bypass the signup form by using fields (e.g. username,
        email) retrieved from the social account provider. If a conflict
        arises due to a duplicate e-mail signup form will still kick in.
        """
        return self._setting("AUTO_SIGNUP", True)


    @property
    def AVATAR_SUPPORT(self):
        """
        Enable support for django-avatar. When enabled, the profile image of
        the user is copied locally into django-avatar at signup.

        Deprecated
        """
        from django.conf import settings
        return self._setting("AVATAR_SUPPORT",
                             'avatar' in settings.INSTALLED_APPS)

    @property
    def PROVIDERS(self):
        """
        Provider specific settings
        """
        return self._setting("PROVIDERS", {})

    @property
    def ADAPTER(self):
        return self._setting \
            ('ADAPTER', 
             'allauth.socialaccount.adapter.DefaultSocialAccountAdapter')

# Ugly? Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
import sys
app_settings = AppSettings('SOCIALACCOUNT_')
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
