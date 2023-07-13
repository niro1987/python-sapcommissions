# SAP Commissions

A Python wrapper for the SAP Commissions API.

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
`https://{TENANT}.callidusondemand.com/APIDocument` to read the full specification, replacing `TENANT` with your
tenant-id.

### Terminology

Things to keep in mind while reading the documentation.

| Keyword  | Description                                                                       |
| -------- | --------------------------------------------------------------------------------- |
| Endpoint | A type of object that you can interact with, like `Participants` and `Positions`. |
| Method   | An action to perform on an endpoint, like `list()` and `get_id()`.                |
| Resource | An instance of an endpoint, like `Participant` and `Position`.                    |

## Usage

To get started, import `Connection` and an endpoint of your choosing. In this example, we'll use `Participants`.

```py
from sapcommissions import Connection
from sapcommissions.endpoints import Participants
```

Initialize a Connection by providing the tenant, username, and password. Optionally, you can disable ssl verification,
if you are having problems connecting to the API from your network.

```python
prod = Connection("CALD-PRD", "MyUserName", "MySuperSecretPassword", verify_ssl=True)
```

In this example we will use the `Participants` endpoint to get a list of all participants from the system. The `list()`
method returns a `generator` object, to retrieve all `Participants`, you can convert the generator to a `list`,
processes the `Participants` one-by-one in a `for-loop` or use a list comprehension to extract neccecery properties.

```py
participants = Participants(prod).list()

# Convert to list
all_users = list(participants)

# For loop
for participant in participants:
  ...  # Do something

# List Comprehension
participant_ids = [participant.payeeId for participant in participants]
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
