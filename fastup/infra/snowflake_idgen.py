from snowflakekit import SnowflakeConfig, SnowflakeGenerator

from fastup.config import get_config

config = get_config()


class SnowflakeIDGenerator:
    """A generator for creating 64-bit, time-sortable, unique IDs.

    This follows the classic Twitter Snowflake design.
    """

    time_bits = 41  # 41 bits gives you ~69 years of timestamps from the epoch
    node_bits = 5  # Allows for 2^5 = 32 unique nodes
    worker_bits = 5  # Allows for 2^5 = 32 unique workers per node
    sequence_bits = 12  # Allows for 2^12 = 4096 IDs per millisecond, per worker
    total_bits = 64  # Creates a 64-bit integer (BIGINT in PostgreSQL)

    def __init__(
        self,
        epoch: int = config.snowflake_epoch,
        node_id: int = config.snowflake_node_id,
        worker_id: int = config.snowflake_worker_id,
        **kwargs,
    ) -> None:
        """Initialize the Snowflake ID generator with unique identifiers.

        :param epoch: Custom epoch timestamp in milliseconds
        :param node_id: The unique ID for the physical machine or data center (0-31)
        :param worker_id: The unique ID for the running process on that node (0-31)
        :param kwargs: Optional configuration overrides (time_bits, node_bits, ...)

        >> Each instance must have a unique `node_id` and `worker_id` combination to prevent ID collisions.
        """
        config = SnowflakeConfig(
            epoch=epoch,
            node_id=node_id,
            worker_id=worker_id,
            time_bits=kwargs.get("time_bits", self.time_bits),
            node_bits=kwargs.get("node_bits", self.node_bits),
            worker_bits=kwargs.get("worker_bits", self.worker_bits),
            sequence_bits=kwargs.get("sequence_bits", self.sequence_bits),
            total_bits=kwargs.get("total_bits", self.total_bits),
        )
        self.gen = SnowflakeGenerator(config=config)

    async def next_id(self) -> int:
        """Generate and return the next unique 64-bit ID.

        :returns: A unique 64-bit integer ID
        """
        return await self.gen.generate()
