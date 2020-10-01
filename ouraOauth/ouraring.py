"""
Author: Martin Karlsson
Email: mrtn.karlsson@gmail.com
"""
import json

from requests_oauthlib import OAuth2Session


class OuraAuth:
    """Construct a Oauth2 Oura session.

    :param client_id: your oura app id.
    :param client_secret: your oura app secret.
    :param redirect_uri: Your registered callback address.
    :param auth_url: oura oauth authorize url.
    :param token_url: oura oauth token url.
    :param scopes: list of scopes to access.

    """

    def __init__(self, redirect_uri, client_id, client_secret, auth_url, token_url, scopes=None):
        self.redirect_uri = redirect_uri  # 'http://127.0.0.1:5353/callback'
        self.client_id = client_id  # os.getenv('OURA_CLIENT_ID')
        self.client_secret = client_secret  # os.getenv('OURA_CLIENT_SECRET')
        self.AUTH_URL = auth_url  # 'https://cloud.ouraring.com/oauth/authorize'
        self.TOKEN_URL = token_url  # 'https://api.ouraring.com/oauth/token'
        self.SCOPE = scopes  # ['email', 'personal', 'daily']

        self.session = OAuth2Session(
            client_id=self.client_id, redirect_uri=self.redirect_uri)

    def oura_authorize(self, scope=None):
        self.session.scope = scope or self.SCOPE
        print(self.session.scope)

        return self.session.authorization_url(self.AUTH_URL)

    def get_token(self, auth_response=None, code=None):
        if auth_response is not None and code is None:
            token = self.session.fetch_token(self.TOKEN_URL, authorization_response=auth_response,
                                             client_secret=self.client_secret)
            return token

        elif code is not None and auth_response is None:
            token = self.session.fetch_token(self.TOKEN_URL, code=code,
                                             client_secret=self.client_secret)

            return token


# class for interacting with Ouras API
class OuraClient:
    def __init__(self, client_id, client_secret, token, token_saver, refresh_url, base_api_url):
        self.client_id = client_id  # os.getenv('OURA_CLIENT_ID')
        self.client_secret = client_secret  # os.getenv('OURA_CLIENT_SECRET')

        self.refresh_url = refresh_url  # 'https://api.ouraring.com/oauth/token'
        self.api_url = base_api_url  # 'https://api.ouraring.com'

        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        self.client_session = OAuth2Session(client_id=self.client_id, token=token, auto_refresh_url=self.refresh_url,
                                            auto_refresh_kwargs=extra, token_updater=token_saver)

    def get_user_info(self):
        """
        :returns: JSON User information
        """
        url = f'{self.api_url}/v1/userinfo'
        return self._make_request(url=url)

    def get_sleep(self, start=None, end=None):
        """
        :param start: Beginning of date range, if omitted it will be set to one week ago
        :type start: date YYYY-MM-DD

        :param end: End of date range, or omit this to get current day
        :type end: date YYYY-MM-DD
        """
        url = f'{self._make_summary(start=start, end=end, summary_type="sleep")}'
        return self._make_request(url=url)

    def get_activity(self, start=None, end=None):
        """
        :param start: Beginning of date range, if omitted it will be set to one week ago
        :type start: date YYYY-MM-DD

        :param end: End of date range, or omit this to get current day
        :type end: date YYYY-MM-DD
        """
        url = f'{self._make_summary(start=start, end=end, summary_type="activity")}'
        return self._make_request(url=url)

    def get_readiness(self, start=None, end=None):
        """
        :param start: Beginning of date range, if omitted it will be set to one week ago
        :type start: date YYYY-MM-DD

        :param end: End of date range, or omit this to get current day
        :type end: date YYYY-MM-DD

        :returns: Json
        """
        url = f'{self._make_summary(start=start, end=end, summary_type="readiness")}'
        return self._make_request(url=url)

    def _make_summary(self, start=None, end=None, summary_type=None):
        if start is None and end is None:
            raise ValueError('Summary needs start date or end date')

        url = f'{self.api_url}/v1/{summary_type}?'

        if start is not None and end is None:
            # return day
            return f'{url}start={start}'
        elif end is not None and start is None:
            # return week
            return f'{url}end={end}'
        else:
            return f'{url}start={start}?end={end}'

    def _make_request(self, url, method=None, data=None, **kwargs):
        data = data or {}
        method = method or 'GET'
        response = self.client_session.request(
            method=method, url=url, data=data, **kwargs)

        if response.status_code == 401:
            print(f'Error {response.status_code}')

        payload = json.loads(response.content.decode('utf8'))
        return payload
