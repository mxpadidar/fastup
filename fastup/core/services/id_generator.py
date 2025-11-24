import typing


class IDGenerator(typing.Protocol):
    """Protocol for integer ID generators."""

    async def next_id(self) -> int:
        """
        Produce the next unique integer identifier.

        :return: unique integer id
        """
        ...
