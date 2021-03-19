from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import requests


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 10
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def get_latest_kubernetes_version():
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[413, 429, 500, 502, 503, 504])
    req_session = requests.Session()
    adapter = TimeoutHTTPAdapter(max_retries=retries)
    req_session.mount("https://", adapter)
    req_session.mount("http://", adapter)

    url = "https://api.github.com/repos/kubernetes/kubernetes/releases/latest"

    payload = {}
    headers = {'Accept': 'application/vnd.github.v3+json'}
    try:
        response = req_session.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            latest_release = json.loads(response.text)
            print(latest_release["tag_name"].split('.')[0][1:])
        else:
          pass
            # logger.warning("Couldn't fetch the latest kubernetes stable release information. Response status code: {}".format(response.status_code))
    except Exception as e:
      pass
        # kubernetes_exception_handler(e, consts.Kubernetes_Latest_Version_Fetch_Fault, "Couldn't fetch latest kubernetes release info", error_message="Error while fetching the latest stable kubernetes release", raise_error=False)

get_latest_kubernetes_version()


# def get_latest_kubernetes_version():
#     retries = Retry(total=3, backoff_factor=1, status_forcelist=[413, 429, 500, 502, 503, 504])
#     req_session = requests.Session()
#     adapter = TimeoutHTTPAdapter(max_retries=retries)
#     req_session.mount("https://", adapter)
#     req_session.mount("http://", adapter)

#     url = consts.Kubernetes_Github_Latest_Release_Uri

#     payload = {}
#     headers = {'Accept': 'application/vnd.github.v3+json'}
#     try:
#         response = req_session.request("GET", url, headers=headers, data=payload)
#         if response.status_code == 200:
#             latest_release = json.loads(response.text)
#             return latest_release["tag_name"]
#         else:
#             logger.warning("Couldn't fetch the latest kubernetes stable release information. Response status code: {}".format(response.status_code))
#     except Exception as e:
#         logger.warning("Couldn't fetch the latest kubernetes stable release information. Error: " + str(e))

#     return None
