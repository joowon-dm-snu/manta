import pytest

import manta_client as mc
from manta_client import Settings
from manta_client.api import MantaAPI
from manta_client.sdk.backend.backend import Backend
from manta_client.sdk.manta_experiment import Experiment


def test_log_wrong_inputs():
    # TODO: can be tested after init to mock, set global vars
    return
    mc.init()
    with pytest.raises(ValueError):
        mc.log({999: 9999})

    with pytest.raises(ValueError):
        mc.log({("test"): 9999})

    with pytest.raises(ValueError):
        mc.log(10)


def test_temporal_prcess():
    team_id = "koqRYzvp25tQBXLpq3BX"
    proj_id = "1pWdEnNyrMINL4oYzPLw"
    exp_id = "EpZGmwoyXZupO5RxNYON"

    s = Settings()
    s.update_envs()
    api = MantaAPI(s)
    api._team_id = team_id
    api._project_id = proj_id
    api._experiment_id = exp_id

    back = Backend(api)
    back.init_internal_process()

    exp = Experiment(s)
    exp.set_backend(back)

    exp.log({"test": 1})
    exp.log({"test": 2})
    exp.log({"test": 3})
    exp.log({"test": 4})
    exp.log({"test": 5})
    exp.log({"test": 6})

    from pprint import pprint

    pprint(api.get_experiment(exp_id))


if __name__ == "__main__":
    test_temporal_prcess()
