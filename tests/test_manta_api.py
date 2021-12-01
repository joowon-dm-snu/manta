import pytest

import manta_client as mc
from manta_client.api.api import MantaAPI
from manta_client.base.settings import Settings

"""
TODO: server to mock server

create teams/projects/experiments should be created in mock not server

refactor all tests here
"""


@pytest.fixture
def api():
    return MantaAPI()


def delete_team(api, team_id):
    api.client.request("delete", f"team/{team_id}")


def test_base_functions():
    s = Settings(api_key="")
    api = MantaAPI(s)

    print(api.profile())
    print(api.team_detail())
    team_id = api.create_team(mc.util.generate_id())["Id"]
    api._team_id = team_id
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
    pass
    # assert api._client.user_agent == "Manta-Python-SDK-v{}".format(mc.__version__)


def test_bad_request_type_reject(api):
    with pytest.raises(AttributeError):
        api._client.request("wrong", "type")


def test_client_no_retry_for_404(api):
    pass


def test_client_no_retry_for_timeout(api):
    pass


def test_api_with_real_server(api):
    pass


def test_team_functions(api):
    api.teams()
    team_id = api.get_team_by_name("manta-test-api-temporal-team")
    if team_id:
        api.delete_team(team_id)
    team_id = api.create_team(name="manta-test-api-temporal-team")
    api.delete_team(team_id)


def test_project_functions(api):
    team_id = api.get_team_by_name("manta-test-api-temporal-team")
    if not team_id:
        team_id = api.create_team(name="manta-test-api-temporal-team")
    else:
        api.team_id = team_id

    project_id = api.create_project(name="test", description="desc")
    project_id = api.create_project(name="test2", description="desc2")

    assert len(api.projects()) == 2

    api.get_project(project_id)
    api.get_project()
    api.delete_team(team_id)


def test_experiments(api):
    team_id = api.get_team_by_name("manta-test-api-temporal-team")
    if not team_id:
        team_id = api.create_team(name="manta-test-api-temporal-team")
    else:
        api.team_id = team_id

    project_id = api.create_project(name="test", description="desc")
    api.create_experiment()
    # api.create_experiment(name="exp1", tags=["tag1", "tag2"], memo="testmemo")

    api.send_experiment_record()

    api.delete_team(team_id)


def test_experiment_logging_flow(api):
    print(api.projects())
    api.create_project("")
    api.create_experiment("yeERJmLWXZHzN02vErq9", name="test-experiment")

    hist = []
    api.send_experiment_record(hist)
    stats = []
    api.send_experiment_record(stats=stats)
    logs = []
    api.send_experiment_record(logs=logs)
