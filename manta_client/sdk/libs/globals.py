import manta_client as mc


def set_globals(
    # global vars
    experiment=None,
    config=None,
    meta=None,
    summary=None,
    # global function
    log=None,
    save=None,
    alarm=None,
    use_artifact=None,
    log_artifact=None,
):
    kwargs = locals()
    for k, v in kwargs.items():
        if v:
            setattr(mc, k, v)


def unset_globals():
    mc.experiment = None
    mc.config = None
    mc.meta = None
    mc.summary = None
    mc.log = None
    mc.save = None
    mc.alarm = None
    mc.use_artifact = None
    mc.log_artifact = None
