from pydantic.v1.errors import PydanticErrorMixin


class BESError(PydanticErrorMixin, Exception):
    pass


class BESTypeError(PydanticErrorMixin, TypeError):
    pass


class BESValueError(PydanticErrorMixin, ValueError):
    pass


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
