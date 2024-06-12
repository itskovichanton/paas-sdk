from time import sleep
import requests
from requests import Session

from src.paassdk.cherkizon import parse_response


class EurekaSession(requests.Session):

    def __init__(self, cherkizon_url: str):
        super().__init__()
        self._cherkizon_url = cherkizon_url
        self._cache: dict[str, str] = {}
        self._cherkizon_session = Session()

    def _resolve_url(self, url) -> (str, bool):

        cached = False

        if url.startswith("eureka"):
            try:
                eureka_host = url[:url.index("]/") + 1]
            except:
                eureka_host = url
            redirected_host = self._cache.get(eureka_host)
            if not redirected_host:
                cherkizon_request = self._cherkizon_session.get(f"{self._cherkizon_url}/deploy-url/get_internal_url",
                                                                params={"url": eureka_host})
                redirected_host = parse_response(cherkizon_request)
                self._cache[eureka_host] = redirected_host
                cached = True
                url = url.replace(eureka_host, redirected_host)

        return url, cached

    def request(self, method, url, *args, **kwargs):

        last_ex = None

        for attempt in range(1, 5):
            url, cached = self._resolve_url(url)
            try:
                return super().request(method, url, *args, **kwargs)
            except BaseException as ex:
                last_ex = ex
                sleep(0.3)
                if cached:
                    self._cache.pop(url)

        raise last_ex
