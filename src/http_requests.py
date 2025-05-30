import dataclasses

import requests
from requests import Response

REQUEST_TIMEOUT_SECONDS = 1200
MAX_RETRY_ATTEMPTS = 3
SINGLE_RETRY_ATTEMPT = 10
RETRY_WAIT_SECONDS = 20


def post_with_retry(url, data=None, json=None, **kwargs):
    return _retry(
        func=lambda: requests.post(url, data=data, json=json,**kwargs))

def _retry(func):
    ex = None
    response = None
    # apply retry mechanism

    try:
        response = func()
    except BaseException as exception:
        ex = exception
        print("An error occurred during the request:")
        response = None

    status_code = response.status_code if response else 0

    return HttpResponse(
        response=response,
        error=ex,
        iteration=0,
        max_retry=MAX_RETRY_ATTEMPTS,
        status_code=status_code
    )

@dataclasses.dataclass
class HttpResponse:
    response: Response
    error: BaseException
    iteration: int
    max_retry: int
    status_code:int