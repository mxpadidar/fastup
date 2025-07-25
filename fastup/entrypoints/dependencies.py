from fastup.adapters.builtin_logger import BuiltInLogger
from fastup.domain.logger import Logger, LoggerFactory


def provide_logger_factory() -> LoggerFactory:
    """returns a factory function for creating logger instances."""

    from fastup.adapters.settings import LOG_CONFIG

    def factory(name: str) -> Logger:
        """creates a logger instance with the given name and configuration."""
        return BuiltInLogger(name=name, **LOG_CONFIG)

    return factory


get_logger = provide_logger_factory()
