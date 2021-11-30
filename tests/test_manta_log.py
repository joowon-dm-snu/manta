import pytest

import manta_client as mc


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
