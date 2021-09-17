from bes.auth.base import BESAuth

TEST_CONFIG = {
    "oauth2basic": dict(username="product_shelter@datawiz.io", password="1qazxcvb")
}


def get_oauth2basic() -> BESAuth:
    auth = BESAuth.oauth2basic()
    auth.oauth2client.fetch_token(**TEST_CONFIG["oauth2basic"])
    auth.initial()
    check_default_initial(auth)
    return auth


def check_default_initial(auth: BESAuth):
    assert auth.user is not None, "User must by not None"
    assert auth.selected_client is not None, "Has not set default selected oauth2client"


def test_initial_oauth2basic():
    get_oauth2basic()


def test_initial_access_token():
    basic = get_oauth2basic()
    auth = BESAuth.access_token(access_token=basic.oauth2client.token["access_token"])
    auth.initial()

    check_default_initial(auth)


def test_use_auth():
    auth = get_oauth2basic()
    user = auth.user
    if len(user.clients) > 1:
        auth2 = auth.use(user.clients[1])
        assert auth.user is auth2.user, "User of to oauth2client is not same"

        assert auth._request_headers != auth2._request_headers, "Headers of new oauth2client is the same to copy oauth2client"
