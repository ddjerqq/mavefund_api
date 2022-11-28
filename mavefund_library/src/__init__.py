"""MaveFund API Client

Examples:
    >>> from mavefund import Client, DataType
    >>> client = Client(api_key="YOUR_API_KEY")
    >>> records = client.get_records(
    >>>     "AAPL",
    >>>     data_type=DataType.GrowthProfitability,
    >>>     start_date="2020-01-01",
    >>>     end_date="2020-01-31",
    >>> )
"""

from .record import Record
from .client import Client
from .async_client import AsyncClient
from .data_type import DataType

__all__ = [
    "Record",
    "Client",
    "DataType",
]
