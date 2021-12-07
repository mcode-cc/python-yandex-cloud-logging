[![PyPI](https://img.shields.io/pypi/v/python-yandex-cloud-logging)](https://pypi.org/project/python-yandex-cloud-logging/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-yandex-cloud-logging)
[![PyPI - License](https://img.shields.io/pypi/l/python-yandex-cloud-logging)](https://github.com/mcode-cc/python-yandex-cloud-logging/blob/main/LICENSE)


# Python Client for Yandex Cloud Logging
 


## Installation

    pip3 install python-yandex-cloud-logging

## Creating a Yandex Cloud Logging Group

    yc logging group create --name=group --retention-period=1h

Result

    done (1s)
    id: af3flf29t8**********
    folder_id: aoek6qrs8t**********
    cloud_id: aoegtvhtp8**********
    created_at: "2021-06-24T09:56:38.970Z"
    name: group
    status: ACTIVE
    retention_period: 3600s

https://cloud.yandex.com/en/docs/logging/quickstart

## Credentials

There are several options for authorization your requests - OAuth Token, Metadata Service (if you're executing code inside VMs or Functions running in Yandex.Cloud) and Service Account Keys

### OAuth Token
    yc config get token

Result

    AQA....


```python
from pyclm.logging import Logger 

log = Logger(
    log_group_id="....",
    credentials={"token": "AQA...."}
)
```

### Service Account Keys


```python
from pyclm.logging import Logger 

log = Logger(
    log_group_id="....",
    credentials={
        "service_account_key": {
            "service_account_id": "....",
            "id": "....",
            "private_key": "<PEM>"
        }
    }
)
```

### Use Yandex SDK

```python
sdk = yandexcloud.SDK(...)

log = Logger(
    sdk=sdk, log_group_id="....",
    resource_type="....", resource_id="....",
    elements=1, period=0
)

```

_resource_type_ - Resource type, serverless.function, hostname.
Value must match the regular expression ([a-zA-Z][-a-zA-Z0-9_.]{0,63})?.

_resource_id_ - Resource ID, i.e., ID of the function producing logs.
Value must match the regular expression ([a-zA-Z0-9][-a-zA-Z0-9_.]{0,63})?.

_elements_ - The number of elements before writing, must be in the range 1-100.

_period_ -  Number of seconds to wait for new log entries before writing.

