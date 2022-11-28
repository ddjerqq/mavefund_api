from __future__ import annotations

import pandas as pd
import aiohttp

from . import DataType
from . import Record


class AsyncClient:
    """MaveFund API Client
    """

    def __init__(
            self,
            api_key: str,
            *,
            __base_url: str = "https://api.mavefund.com",
    ) -> None:
        """Create a new instance of the async API client.

        :param api_key: The API key to use for authentication. get yours at #TODO link
        :param __base_url: override the api link
        """
        self.__api_key = api_key
        self.__base_url = __base_url

        self.__session = aiohttp.ClientSession(cookies={"token": self.__api_key})

    async def get_records(
            self,
            symbol: str,
            *,
            data_type: DataType = DataType.ALL,
            start_date: str,
            end_date: str,
    ) -> list[Record]:
        """Get records for a given company.

        :param symbol: The stock ticker symbol for the company.
        :param data_type: The type of data to return.
        :param start_date: The start date of the records to return.
        :param end_date: The end date of the records to return.
        :return: A list of records.
        """
        response = await self.__session.get(
            f"{self.__base_url}/api/v1/records/{symbol}",
            params={
                "data_type" : data_type.value,
                "start_date": start_date,
                "end_date"  : end_date,
            },
        )
        response.raise_for_status()
        return [
            Record.from_json(record)
            for record in await response.json()
        ]

    async def get_records_as_df(
            self,
            symbol: str,
            *,
            data_type: DataType = DataType.ALL,
            start_date: str,
            end_date: str,
    ) -> pd.DataFrame:
        """Get records for a given company as a pandas DataFrame.

        :param symbol: The stock ticker symbol for the company.
        :param data_type: The type of data to return.
        :param start_date: The start date of the records to return.
        :param end_date: The end date of the records to return.
        :return: A pandas DataFrame.
        """
        records = await self.get_records(
            symbol,
            data_type=data_type,
            start_date=start_date,
            end_date=end_date,
        )
        return pd.DataFrame([record.flat_dict() for record in records])

    async def close(self) -> None:
        """Close the API client.

        alternatively use the context manager:
            >>> async with AsyncClient(api_key="YOUR_API_KEY") as client:
            >>>     records = await client.get_records(...)
        """
        await self.__session.close()

    def __aenter__(self) -> AsyncClient:
        return self

    def __aexit__(self, exc_type: type, exc_val: Exception, exc_tb: ...) -> None:
        await self.close()
