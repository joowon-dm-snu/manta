import os
from typing import Any, Dict, List, Optional, Sequence

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
        print(f"API connected to {self._client.base_url}")
        self._team_id = None
        self._project_id = None
        self._experiment_id = None

    @property
    def api_key(self):
        if self._settings.api_key:
            return self._settings.api_key
        return env.get_api_key(self._settings.base_url)

    @property
    def client(self):
        return self._client

    @property
    def team_id(self):
        return self._team_id

    @property
    def project_id(self):
        return self._project_id

    @property
    def experiment_id(self):
        #
        return self._experiment_id or self._settings.experiment_id

    def setup(self):
        """
        1. set team by using settings.entity
        2. set project by using settings.project
        """
        s = self._settings

        self._team_id = None
        self._project_id = None
        self._experiment_id = None

        # set team
        team_name = s.entity
        if team_name:
            for team in self.teams():
                if team["uid"] == team_name:
                    self._team_id = team["Id"]
                    break
        else:
            # TODO: server API not yet implemented
            self._team_id = self.get_default_team()["Id"]

        # set project
        project_name = s.project
        for proj in self.projects():
            if proj["name"] == project_name:
                self._project_id = proj["Id"]
                break

        if self._project_id is None:
            self.create_project(name=project_name)

    def profile(self):
        return self.client.request_json("get", "user/profile")

    def teams(self):
        return self.client.request_json("get", "team/my")["teams"]

    def get_default_team(self):
        return self.client.request_json("get", "team/personal")

    def get_team(self, team_id: str = None) -> Dict:
        team_id = team_id or self.team_id
        return self.client.request_json("get", f"team/{team_id}")

    def create_team(self, name: str) -> str:
        kwargs = dict(uid=name)
        id = self.client.request_json("post", "team", kwargs)["Id"]
        self._team_id = id
        return id

    def delete_team(self, team_id: str) -> None:
        self.client.request_json("delete", f"team/{team_id}")

    def get_team_by_name(self, name: str):
        """
        Return team id
        """

        for team in self.teams():
            if name == team["name"]:
                return team["Id"]
        return None

    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        thumbnail: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        """
        Return upsert project
        """
        description = description or " "  # TODO: API will change it to optional later, delete here
        kwargs = locals()
        res = self.client.request_json("post", f"team/{self.team_id}/project", kwargs)
        self._project_id = res["Id"]
        return self._project_id

    def projects(self, team_id: str = None) -> List[Dict[str, Any]]:
        """
        Return projects list
        """
        team_id = team_id or self.team_id
        return self.client.request_json("get", f"team/{team_id}/project/my")["projects"]

    def get_project(self, project_id: str = None):
        """
        Return project detail
        """
        project_id = project_id or self.project_id
        return self.client.request_json("get", f"project/{project_id}")

    def get_project_by_name(self, name: str):
        """
        Return project detail
        """

        for project in self.projects():
            if name == project["name"]:
                return project["Id"]
        return None

    def delete_project(self, project_id: str):
        """
        Return delete project
        """
        return self.client.request_json(
            "delete",
            f"project/{project_id}",
        )

    def experiments(self, project_id: str = None):
        """
        Return experiments list
        """
        project_id = project_id or self.project_id
        return self.client.request_json("get", f"project/{project_id}/experiment")["experiments"]

    def get_experiment(self, experiment_id: str = None):
        """
        Return experiment detail
        """
        experiment_id = experiment_id or self.experiment_id

        return self.client.request_json("get", f"experiment/{experiment_id}")

    def create_experiment(
        self,
        name: str = None,
        memo: str = None,
        config: Dict = None,
        metadata: Dict = None,
        hyperparameter: Dict = None,
        tags: Sequence = None,
    ):
        """
        Return experiment upsert
        """
        project_id = self.project_id
        name = name or util.generate_id()

        kwargs = locals()
        res = self.client.request_json("post", f"project/{project_id}/experiment", kwargs)
        self._experiment_id = res["Id"]
        return self._experiment_id

    def delete_experiment(self, *args, **kwargs):
        """
        Return experiment delete
        """
        return {}

    def send_heartbeat(self, **kwargs):
        # TODO: Ask backend need something
        pass

    def send_experiment_record(self, histories: List[Dict] = None, systems: List[Dict] = None, logs: List[Dict] = None):
        kwargs = locals()
        return self.client.request("post", f"experiment/{self.experiment_id}/record", kwargs)

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
