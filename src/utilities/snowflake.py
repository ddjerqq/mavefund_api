from __future__ import annotations

import random
import time
from datetime import datetime

__all__ = (
    "Snowflake",
)

DISCORD_EPOCH = 142007040000


class Snowflake:
    """
    Snowflakes
    Discord utilizes Twitter's snowflake format for uniquely identifiable descriptors (IDs).
    These IDs are guaranteed to be unique across all of Discord, except in some unique scenarios in which child objects share their parent's ID.
    Because Snowflake IDs are up to 64 bits in size (e.g. an uint64), they are always returned as strings in the HTTP API to prevent integer overflows in some languages.
    See Gateway ETF/JSON for more information regarding Gateway encoding.
    Snowflake ID Broken Down in Binary:
    111111111111111111111111111111111111111111 11111 11111 111111111111
    64                                         22    17    12          0
    Snowflake ID Format Structure (Left to Right):
    FIELD | BITS | NUMBER OF BITS | DESCRIPTION | RETRIEVAL
    Timestamp | 63 to 22 | 42 bits | Milliseconds since Discord Epoch, the first second of 2015 or 1420070400000. | (snowflake >> 22) + 1420070400000
    Internal worker ID | 21 to 17 | 5 bits | | (snowflake & 0x3E0000) >> 17
    Internal process ID | 16 to 12 | 5 bits | | (snowflake & 0x1F000) >> 12
    Increment | 11 to 0 | 12 bits | For every ID that is generated on that process, this number is incremented | snowflake & 0xFFF
    source: https://discord.com/developers/docs/reference#snowflakes
    """

    def __new__(cls) -> int:
        id = time.time_ns() // 10_000_000
        id -= DISCORD_EPOCH
        id <<= 5

        # internal worker id simulation
        worker_id = random.randrange(0, 32)  # 5 bits
        id += worker_id
        id <<= 5

        # internal process id simulation
        id += random.randrange(0, 32)  # 5 bits
        id <<= 12

        # for every ID that is generated on a process, this number is incremented
        id += random.randrange(0, 4096)  # 12 bits
        return id

    @classmethod
    def created_at(cls, id: int) -> datetime:
        ts = ((id >> 22) + DISCORD_EPOCH) // 100
        return datetime.fromtimestamp(ts)
