# mssql-dba-notifier

Simple notification script for SQL Server DBA's.

## Features

* Multiple hosts
* Currently support only disk free space alert
* Currently support only [Telegram](https://telegram.org/) messenger
* Currently support **only Windows Authentication** (`Trusted_Connection=yes`)

## Prerequisites

1. Python 3.7+
2. [Microsoft ODBC Driver 17 for SQL Server](https://www.microsoft.com/en-US/download/details.aspx?id=56567)

## Installation

1. Install all requirements: `pip install -r requirements.txt` 
2. Add servers in config file (`config.toml`), for example:
    ```
    [[servers]]
    host_name = "my-server-1"

    [[servers]]
    host_name = "my-server-2"

    [[servers]]
    host_name = "..."
    ```
3. Add Telegram `api_token` and `chat_id` in config file (`config.toml`)
4. Run the script `main.py` periodically on your server via SQL Server Agent Job or Windows Scheduler