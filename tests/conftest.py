import os

import pytest

from manta_client import Settings
from manta_client.sdk.manta_experiment import Experiment
from tests.utils.mock_requests import RequestsMock


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


@pytest.fixture
def experiment(request):
    marker = request.node.get_closest_marker("manta_args")
    kwargs = marker.kwargs if marker else dict(env={})
    for k, v in kwargs["env"].items():
        os.environ[k] = v

    # TODO: should be create experiment by manta.init
    s = Settings()
    s.update_envs(kwargs["env"])
    return Experiment(settings=s)
