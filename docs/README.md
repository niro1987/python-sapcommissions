# SAP Commissions

A Python wrapper for the SAP Commissions API.

- [SAP Commissions](#sap-commissions)
  - [Installation](#installation)
    - [REST API](#rest-api)
    - [Terminology](#terminology)
  - [Usage](#usage)
  - [Endpoints](#endpoints)
  - [Methods](#methods)
  - [Legal Disclaimer](#legal-disclaimer)

If you like this project, please consider to [BuyMeACoffee](https://www.buymeacoffee.com/niro1987) or
[contact me](mailto:niels.perfors1987@gmail.com) directly.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/niro1987)

## Installation

To install the project, run the following command:

```text
pip install python-sapcommissions
```

### REST API

This project mimics the usage of the SAP Commissions REST API. Visit
`https://{CALD}-{ENV}.callidusondemand.com/APIDocument` to read the full specification, replacing `CALD` with your
tenant name, and `ENV` with your environment name.

### Terminology

Things to keep in mind while reading the documentation.

| Keyword  | Description                                                                       |
| -------- | --------------------------------------------------------------------------------- |
| Endpoint | A type of object that you can interact with, like `Participants` and `Positions`. |
| Method   | An action to perform on an endpoint, like `list()` and `get_id()`.                |
| Resource | An instance of an endpoint, like `Participant` and `Position`.                    |

## Usage

To get started, import `Connection` and an endpoint of your choosing. In this example, we'll use `Participants` as the
endpoint.

```py
from sapcommissions import Connection
from sapcommissions.endpoints import Participants
```

Initialize a Connection by providing the tenant, environment, username, and password. Optionally, you can disable ssl
verification, if you have problems connecting to the API from your corporate network.

```python
prod = Connection("CALD", "PRD", "MyUserName", "MySuperSecretPassword", verify_ssl=False)
```

We'll use the `Participants` endpoint to get a list of all participants in the environment. The `list()` method returns
a `generator`, to retrieve all `Participants`, you can convert the generator to a `list` or processes the `Participants`
one-by-one.

```py
# List all Participants
all_users = list(Participants(prod).list())

# Process Participants one-by-one
for participant in Participants(prod).list():
  ...  # Do something
```

## Endpoints

Endpoints are the objects you can interact with, like `Participants`, `Positions`, `Credits` or `Pipelines`. For a full
list of endpoints and their associated methods, please read the [Endpoints documentation](ENDPOINTS.md).

## Methods

Methods are the actions you can perform on an endpoint, like `list()`, `get()` and `create()`. You'll find links to the
associated methods in the [Endpoints documentation](ENDPOINTS.md). For a full list of available methods, please read the
[Methods documentation](METHODS.md).

## Legal Disclaimer

This software is designed for use with SAP® Commissions.

SAP Commissions is the trademark or registered trademark of SAP SE or its affiliates in Germany and in other countries.

The developers take no legal responsibility for the functionality or security of your SAP Commissions environment.
