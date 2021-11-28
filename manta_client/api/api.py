import os
from typing import Any, Dict, List, Optional

import manta_client.env as env
import manta_client.util as util
from manta_client.api.client import MantaClient
from manta_client.base.settings import Settings

PROJECT_ENDPOINT = ""
EXPERIMENT_ENDPOINT = ""
USER_ENDPOINT = ""
TEAM_ENDPOINT = ""


class MantaAPI(object):
    def __init__(self, settings: Settings = None, environ: os.environ = None):
        self._settings = settings or Settings()
        self._environ = environ or os.environ

        self._client = MantaClient(self._settings)
        self._team_id = None
        self.setup()

    @property
    def api_key(self):
        return env.get_api_key(self._settings.base_url)

    @property
    def client(self):
        return self._client

    @property
    def team_id(self):
        # TODO: delete
        return "2pWGwX1WgqTEVnvLax2K"
        return self._team_id

    def setup(self):
        """
        Project creation need team_id, so set team id here
        """
        # teams are not working now, fix this later on
        return "donghyung.ko"

        # TODO: (kjw) fix profile ??
        team_name = self._settings.team_name or self.profile()["name"]

        for team in self.teams():
            if team["name"] == team_name:
                self._client.set_team(team_name)
                self._team_id = team["id"]

        # TODO: (kjw) back propagate to settings
        self._settings.team = team_name

    def profile(self):
        return self.client.request("get", "user/profile")

    def teams(self):
        return self.client.request("get", "team/my")

    def team_detail(self, team_id: str = None):
        team_id = team_id or self.team_id
        return self.client.request("get", f"team/{team_id}")

    def create_project(
        self, name: str, description: str, thumbnail: Optional[str] = None, tags: Optional[List[str]] = None
    ):
        """
        Return upsert project
        """
        kwargs = locals()
        kwargs.pop("self")
        return self.client.request("post", f"team/{self.team_id}/project", kwargs)

    def projects(self, team_id: str = None) -> List[Dict[str, Any]]:
        """
        Return projects list
        """
        team_id = team_id or self.team_id
        return self.client.request("get", f"team/{team_id}/project/my")

    def get_project(self, project_id: str):
        """
        Return project detail
        """
        return self.client.request("get", f"project/{project_id}")

    def delete_project(self, project_id: str):
        """
        Return delete project
        """
        return self.client.request(
            "delete",
            f"project/{project_id}",
        )

    def experiments(self, project_id: str):
        """
        Return experiments list
        """
        return self.client.request("get", f"project/{project_id}/experiment")

    def get_experiment(self, project_id: str, experiment_id: str):
        """
        Return experiment detail
        """
        return self.client.request("get", f"project/{project_id}/experiment/{experiment_id}")

    def create_experiment(self, project_id, name: str = None):
        """
        Return experiment upsert
        """
        name = name or util.generate_id()
        kwargs = locals()
        kwargs.pop("self")
        return self.client.request("post", f"project/{project_id}/experiment", kwargs)

    def delete_experiment(self, *args, **kwargs):
        """
        Return experiment delete
        """
        return {}

    def artifacts(self, *args, **kwargs):
        """
        Return artifacts list
        """
        return {}

    def get_artifact(self, *args, **kwargs):
        """
        Return artifact detail
        """
        return {}

    def upsert_artifact(self, *args, **kwargs):
        """
        Return artifact upsert
        """
        return {}

    def delete_artifact(self, *args, **kwargs):
        """
        Return artifact delete
        """
        return {}

    # DO WE NEED THIS?
    def get_artifact_manifest(self, *args, **kwargs):
        """
        Return artifact manifest detail
        """
        return {}

    def upsert_artifact_manifest(self, *args, **kwargs):
        """
        Return artifact manifest upsert
        """
        return {}

    # DO WE NEED THIS?
    def delete_artifact_manifest(self, *args, **kwargs):
        """
        Return artifact manifest delete
        """
        return {}

    def reports(self, *args, **kwargs):
        """
        Return reports list
        """
        return {}

    def get_report(self, *args, **kwargs):
        """
        Return report detail
        """
        return {}

    def upsert_report(self, *args, **kwargs):
        """
        Return report upsert
        """
        return {}

    def delete_report(self, *args, **kwargs):
        """
        Return report delete
        """
        return {}


if __name__ == "__main__":
    from pprint import pprint

    from manta_client.base.settings import Settings

    s = Settings(api_key="EmTes.585ReFy4pI40i5")
    api = MantaAPI(s)
    #
    # print(api.profile())
    # print(api.team_detail())
    # print(api.create_project("test2", "project"))
    pprint(api.projects())
    pprint(api.teams())
    print(api.get_project("yeERJmLWXZHzN02vErq9"))
    print(api.create_experiment("yeERJmLWXZHzN02vErq9", name="test-experiment"))
    print(api.create_experiment("yeERJmLWXZHzN02vErq9"))
    print(api.experiments("yeERJmLWXZHzN02vErq9"))
