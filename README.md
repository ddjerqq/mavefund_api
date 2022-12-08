# MaveFund API 

![logo](/static/images/mavefund.png)

## Introduction
This is an API and a backend system for [mavefund.com](https://mavefund.com). 
It is built using the FastAPI framework and is hosted on IONOS VPS.

## MaveFund library

The MaveFund library is a python library that is used to interact with the MaveFund API. 
It is available on [PyPI](https://pypi.org/ddjerqq/mavefund/).

## Installation
    
    pip install mavefund

## Usage
```python
from mavefund import Client, DataType

client = Client(api_key="YOUR_API_KEY")

df = client.get_records_as_df(
    "AAPL",
    data_type=DataType.GROWTH_PROFITABILITY,
    start_date="2000-01-01",
    end_date="2023-01-01",
)
```

# TODO
> * [ ] Add payment
> * [x] Deploy
> * [x] Migrate to postgres
> * [x] Add tests
> * [x] Add routes
> * [x] Add docker
> * [x] Add the actual data
> * [x] Add a README.md
> * [x] Add a .gitignore
