import pytest

import manta_client as mc
from manta_client.api.api import MantaAPI
from manta_client.base.settings import Settings


@pytest.fixture
def api():
    return MantaAPI()


def test_base_functions():
    s = Settings(api_key="")
    api = MantaAPI(s)

    print(api.profile())
    print(api.team_detail())
    try:
        print(api.create_project("test2", "project"))
    except Exception:
        pass
    project_id = api.projects()[0]["Id"]
    print(api.get_project(project_id))
    print(api.create_experiment(project_id, name="test-experiment"))
    print(api.create_experiment(project_id))
    print(api.experiments(project_id))


def test_user_agent(api):
    assert api._client.user_agent == "Manta-Python-SDK-v{}".format(mc.__version__)


def test_bad_request_type_reject(api):
    with pytest.raises(AttributeError):
        api._client.request("wrong", "type")


def test_client_no_retry_for_404(api):
    pass


def test_client_no_retry_for_timeout(api):
    pass


def test_api_with_real_server(api):
    pass
