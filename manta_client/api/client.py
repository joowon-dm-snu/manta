import json
import time
from typing import Dict

import requests

import manta_client as mc
import manta_client.env as env
from manta_client.base.settings import Settings


class _BaseClient(object):
    def __init__(self, settings, timeout=None):
        self._settings = settings
        self.timeout = timeout or env.get_http_timeout()
        self._client = None
        self.reset_client()

    def reset_client(self):
        _api_key = self._settings.api_key
        self._client = requests.Session()
        self._client.timeout = self.timeout
        self._client.headers.update(
            {
                "User-Agent": self.user_agent,
                "Authorization": "manta-apikey {}".format(_api_key)
                # TODO: custom headers here
                #   ex) username, user-email
            }
        )

    @property
    def base_url(self):
        return self._settings.base_url

    @property
    def user_agent(self):
        return "Manta-Python-SDK-v{}".format(mc.__version__)

    def get(self, endpoint, kwargs=None):
        return self._client.get(endpoint, params=kwargs)

    def post(self, endpoint, kwargs=None):
        return self._client.post(endpoint, data=kwargs)

    def delete(self, endpoint):
        return self._client.delete(endpoint)

    def request(self, request_type, endpoint, kwargs=None):
        if request_type not in ["get", "post", "patch", "delete"]:
            raise AttributeError("wrong request_type")

        req_func = getattr(self._client, request_type)

        url = self.base_url + endpoint
        if request_type == "get":
            res = req_func(url, params=kwargs)
        else:
            res = req_func(url, data=kwargs)
        return res


class MantaClient:
    def __init__(
        self, settings: Settings = None, retry_timedelta: int = None, num_retries: int = 0, timeout: int = None
    ) -> None:
        """ """
        self._settings = settings or Settings()
        self.retry_timedelta = retry_timedelta
        self.num_retries = num_retries
        self.timeout = timeout

        self._client = _BaseClient(self._settings, timeout=timeout)

    @property
    def base_url(self):
        return self._client.base_url

    def request(self, request_type, endpoint, params=None) -> requests.Response:
        """TODO: retrying request implementation"""
        # TODO: raise error if response is 4xx 5xx
        return self._client.request(request_type, endpoint, kwargs=params)
        while True:
            try:
                res = self._client.request(request_type, endpoint, kwargs=params)
                return res
            except Exception:
                pass

            time.sleep(1.5)
            break

    def request_json(self, request_type, endpoint, params=None) -> Dict:
        kwargs = locals()
        kwargs.pop("self")
        res = self.request(**kwargs)

        try:
            return res.json()
        except json.JSONDecodeError:
            return res.text


if __name__ == "__main__":
    c = MantaClient()
    res = c.request("get", "team/my")
    print(res)
