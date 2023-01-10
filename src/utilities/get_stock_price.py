import asyncio as aio
import datetime
import pytest
import yfinance as yf


async def get_stock_price(ticker: str) -> dict[datetime.date, float]:
    """get the stock prices for a given ticker

    get back a dictionary mapping of the previous 10 years for this ticker and the
    stock prices for the opening price of this company.

    return type is dictionary with keys of `datetime.date` and values of floats the
    opening of the stocks
    """
    ticker = yf.Ticker("MSFT")

    loop = aio.get_event_loop()

    df = await loop.run_in_executor(
        None,
        lambda: ticker.history(period="10y", interval="1mo")
    )

    timestamp_open_slice = df.iloc[::13, 0:1]
    data = timestamp_open_slice.to_dict()["Open"]
    return {
        timestamp.date(): price
        for timestamp, price in data.items()
    }


@pytest.mark.asyncio
async def test_it_works():
    prices = await get_stock_price("MSFT")
    print(prices)
