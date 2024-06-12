import requests

ERR_REASON_SERVER_RESPONDED_WITH_ERROR = "ERRCODE_SERVER_RESPONDED_WITH_ERROR"
ERR_REASON_INTERNAL = "INTERNAL"
ERR_REASON_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND = "ERRCODE_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND"
ERR_REASON_SERVER_UNAVAILABLE = "ERRCODE_SERVER_UNAVAILABLE"


class CherkizonException(BaseException):

    def __init__(self, message=None, reason=ERR_REASON_SERVER_RESPONDED_WITH_ERROR, cause: BaseException = None,
                 **kwargs):
        if not message and cause:
            message = str(cause)
        self.reason = reason
        self.message = message
        self.cause = cause
        self.__dict__.update(kwargs)
        super().__init__(self.message)


def parse_response(r: dict | requests.models.Response, reason_mapping: dict[str, str] = None):
    if isinstance(r, requests.models.Response):
        try:
            r = r.json()
        except:
            msg = r.text
            if 200 <= r.status_code <= 300:
                r = {"result": msg}
            else:
                r = {"error": {"message": msg}}

    detail = r.get("detail")
    if detail:
        raise CherkizonException(message=detail, reason=ERR_REASON_INTERNAL)
    error = r.get("error")
    if error:
        reason = error.get("reason")
        if reason_mapping is not None:
            reason = reason_mapping.get(reason) or ERR_REASON_SERVER_RESPONDED_WITH_ERROR
            error["reason"] = reason
        raise CherkizonException(**error)
    return r.get("result")

