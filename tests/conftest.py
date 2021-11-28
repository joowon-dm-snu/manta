from tests.utils.mock_requests import InjectRequestsParse, RequestsMock


def default_ctx():
    return {
        "experiments": {},
        "files": {},
    }


def mock_server(mocker):
    ctx = default_ctx()
    # TODO: (kjw) add flask app
    mock = RequestsMock(ctx)
    mocker.patch("manta_client.api.client.request", mock)
    return mock
