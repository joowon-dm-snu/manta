import manta_client as mc
from manta_client.sdk.manta_setup import _MantaGlobalSetup

# TODO: add tests later or delete this file.


def test_basic():
    exp = mc.init(entity="joowon")
    print(_MantaGlobalSetup._instance._settings.entity)
    print(exp._settings.entity)


if __name__ == "__main__":
    test_basic()
