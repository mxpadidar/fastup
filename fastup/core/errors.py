class BaseErr(Exception):
    """Base class for all Fastup exceptions."""

    pass


class NotFoundErr(BaseErr): ...


class ValidationErr(BaseErr): ...
