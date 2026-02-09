class BESError(Exception):
    code = "bes.error"
    msg_template = "BES error"

    def __init__(self, **ctx):
        super().__init__()
        self.ctx = ctx

    def __str__(self) -> str:
        try:
            return self.msg_template.format(**self.ctx)
        except Exception:
            return self.msg_template


class BESTypeError(TypeError):
    code = "bes.type_error"
    msg_template = "BES type error"

    def __init__(self, **ctx):
        super().__init__()
        self.ctx = ctx

    def __str__(self) -> str:
        try:
            return self.msg_template.format(**self.ctx)
        except Exception:
            return self.msg_template


class BESValueError(ValueError):
    code = "bes.value_error"
    msg_template = "BES value error"

    def __init__(self, **ctx):
        super().__init__()
        self.ctx = ctx

    def __str__(self) -> str:
        try:
            return self.msg_template.format(**self.ctx)
        except Exception:
            return self.msg_template


class BESBadRequestError(BESError):
    code = "bes.client.bad_request"
    msg_template = "Invalid request {response.content}"


class BESSelectedClientError(BESValueError):
    code = "bes.server.selected_client.value_error"
    msg_template = "Invalid selected client. ClientRequest({request_client_id}) != ClientResponse({response_client_id})"


class BESRetryError(BESError):
    code = "bes.retry.error"


class BESServerError(BESRetryError):
    code = "bes.server.error"
    msg_template = "Server error {response}"
