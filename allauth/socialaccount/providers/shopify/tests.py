from django.test.utils import override_settings

from allauth.compat import reverse
from allauth.socialaccount.tests import create_oauth2_tests
from allauth.tests import MockedResponse, mocked_response
from allauth.socialaccount.providers import registry
from allauth.compat import parse_qs, urlparse

from .provider import ShopifyProvider


class ShopifyTests(create_oauth2_tests(registry.by_id(ShopifyProvider.id))):

    def _complete_shopify_login(self, q, resp, resp_mock, with_refresh_token):
        complete_url = reverse(self.provider.id + '_callback')
        self.assertGreater(q['redirect_uri'][0]
                           .find(complete_url), 0)
        response_json = self \
            .get_login_response_json(with_refresh_token=with_refresh_token)
        with mocked_response(
                MockedResponse(
                    200,
                    response_json,
                    {'content-type': 'application/json'}),
                resp_mock):
            resp = self.client.get(complete_url,
                                   {'code': 'test',
                                    'state': q['state'][0],
                                    'shop': 'test',
                                    })
        return resp

    def login(self, resp_mock, process='login', with_refresh_token=True):
        resp = self.client.get(reverse(self.provider.id + '_login'),
                               {'process': process, 'shop': 'test'})
        self.assertEqual(resp.status_code, 302)
        p = urlparse(resp['location'])
        q = parse_qs(p.query)
        resp = self._complete_shopify_login(q, resp, resp_mock, with_refresh_token)
        return resp

    def get_mocked_response(self):
        return MockedResponse(200, """
        {
            "shop": {
                "id": "1234566",
                "name": "Test Shop",
                "email": "email@example.com"
            }
        }
        """)


@override_settings(SOCIALACCOUNT_PROVIDERS={'shopify': {'IS_EMBEDDED': True}})
class ShopifyEmbeddedTests(ShopifyTests):
    """
    Shopify embedded apps (that run within an iFrame) require a JS (not server)
    redirect for starting the oauth2 process.

    See Also: https://help.shopify.com/api/sdks/embedded-app-sdk/getting-started#oauth
    """

    def login(self, resp_mock, process='login', with_refresh_token=True):
        resp = self.client.get(reverse(self.provider.id + '_login'),
                               {'process': process, 'shop': 'test'})
        self.assertEqual(resp.status_code, 200)  # No re-direct, JS must do it
        actual_content = resp.content.decode('utf8')
        self.assertTrue('script' in actual_content, 'Content missing script tag. [Actual: {}]'.format(actual_content))
        self.assertTrue(resp.xframe_options_exempt, 'Redirect JS must be allowed to run in Shopify iframe')
        p = urlparse(actual_content.split(";</script>")[0].split('location.href = "')[1])
        q = parse_qs(p.query)
        resp = self._complete_shopify_login(q, resp, resp_mock, with_refresh_token)
        return resp
