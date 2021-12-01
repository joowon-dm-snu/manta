import pytest

import manta_client as mc
from manta_client.sdk.manta_experiment import Experiment


def test_experiment_basic():
    s = mc.Settings()
    c = dict(param1=2, param2=4)
    experiment = Experiment(settings=s, config=c)
    assert dict(experiment.config) == dict(param1=2, param2=4)


@pytest.mark.manta_args(env={"MANTA_EXPERIMENT_ID": "experimentid"})
def test_experiment_id(experiment):
    assert experiment.id == "experimentid"


@pytest.mark.manta_args(env={"MANTA_NAME": "experimentname"})
def test_experiment_name(experiment):
    assert experiment.name == "experimentname"


@pytest.mark.manta_args(env={"MANTA_MEMO": "test memo"})
def test_experiment_memo(experiment):
    assert experiment.memo == "test memo"


def test_experiment_setmemo(experiment):
    experiment.memo = "test memo"
    assert experiment.memo == "test memo"


@pytest.mark.manta_args(env={"MANTA_TAGS": "test-tag1, test-tag2"})
def test_experiment_tags(experiment):
    pass  # pending for settings.update_envs implementation
    # assert experiment.tags == ("tag1", "tag2")


def test_experiment_settags(experiment):
    experiment.tags = ["test-tag1", "test-tag2"]
    assert experiment.tags == ("test-tag1", "test-tag2")


def test_experiment_mode(experiment):
    assert experiment.mode == "online"


@pytest.mark.manta_args(env={"MANTA_ENTITY": "entity"})
def test_experiment_entity(experiment):
    assert experiment.entity == "entity"


@pytest.mark.manta_args(env={"MANTA_PROJECT": "test_proj"})
def test_experiment_project(experiment):
    assert experiment.project == "test_proj"


@pytest.mark.manta_args(env={"MANTA_GROUP": "test_group"})
def test_experiment_group(experiment):
    assert experiment.group == "test_group"


@pytest.mark.manta_args(env={"MANTA_JOB_TYPE": "test_job"})
def test_experiment_jobtype(experiment):
    assert experiment.job_type == "test_job"


@pytest.mark.manta_args(env={"MANTA_ENTITY": "entity", "MANTA_PROJECT": "project", "MANTA_EXPERIMENT_ID": "exp_id"})
def test_experiment_path(experiment):
    assert experiment.path == "entity/project/exp_id"


def test_experiment_add_history(experiment):
    experiment.log({"test": 123})
    assert experiment.history["test"] == 123
