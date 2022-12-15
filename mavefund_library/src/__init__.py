"""MaveFund API Client

Examples:
    >>> from mavefund import Client, DataType
    >>> client = Client(api_key="YOUR_API_KEY")
    >>> records = client.get_records(
    >>>     "AAPL",
    >>>     data_type=DataType.GROWTH_PROFITABILITY,
    >>>     start_date="2020-01-01",
    >>>     end_date="2020-01-31",
    >>> )
"""

from .record import Record
from .client import Client
from .async_client import AsyncClient
from .data_type import DataType

# test_python_api
# 1Password
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDUyMjY3NDY5NDAyNzE2NzAiLCJleHAiOjE2NzA5NTQxMzZ9.Fc2kno3-y6ZDSOtITXtatz-RWFSQ8CRw1sbGTznBT70

__all__ = [
    "Record",
    "Client",
    "DataType",
    "AsyncClient",
]
