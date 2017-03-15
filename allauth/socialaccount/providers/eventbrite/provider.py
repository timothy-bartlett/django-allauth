"""Customise Provider classes for Eventbrite API v3."""
from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


PROFILE_URL = 'https://www.eventbriteapi.com/v3/users/me/'


class EventbriteAccount(ProviderAccount):

    """ProviderAccount subclass for Eventbrite."""

    def get_avatar_url(self):
        """Return avatar url."""
        return self.account.extra_data['image_id']

    def get_profile_url(self):
        """Return profile URL (same for EventbriteOAuth2Adapter)."""
        return PROFILE_URL

    def to_str(self):
        """A wrapper method for __str__ for python 2 compatibility."""
        dflt = super(EventbriteAccount, self).to_str()
        return self.account.extra_data.get('name', dflt)


class EventbriteProvider(OAuth2Provider):

    """OAuth2Provider subclass for Eventbrite."""

    id = 'eventbrite'
    name = 'Eventbrite'
    account_class = EventbriteAccount

    def extract_uid(self, data):
        """Extract uid ('id') and ensure it's a str."""
        return str(data['id'])

    def extract_common_fields(self, data):
        """Extract fields from PROFILE_URL."""
        return dict(
            emails=data.get('emails'),
            id=data.get('id'),
            name=data.get('name'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            image_url=data.get('image_url')
        )

    def extract_email_addresses(self, data):
        """Extract email addresses if verified."""
        ret = []
        emails = data.get('emails')
        for email in emails:
            ret.append(EmailAddress(email=email['email'],
                                    verified=email['verified'],
                                    primary=email['primary']))
        return ret


provider_classes = [EventbriteProvider]
