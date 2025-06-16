import pathlib


class BaseErr(BaseException):
    def __init__(self, msg: str, context: dict | None = None) -> None:
        super().__init__(msg)
        self.msg = msg
        self.context = context


class FileDoesNotExistErr(BaseErr):
    def __init__(self, path: pathlib.Path, context: dict | None = None) -> None:
        super().__init__(
            msg=f"file does not exist in: {path.as_posix()}", context=context
        )
