# SAP Commissions

A Python wrapper for the SAP Commissions API.

- [SAP Commissions](#sap-commissions)
  - [Installation](#installation)
    - [REST API](#rest-api)
    - [Terminology](#terminology)
  - [Usage](#usage)
  - [Methods](#methods)
    - [List](#list)
    - [Get](#get)
    - [Get ID](#get-id)
    - [Get Versions](#get-versions)
    - [Create](#create)
    - [Create Versions](#create-versions)
    - [Update](#update)
    - [Update Versions](#update-versions)
    - [Delete](#delete)
    - [Delete Versions](#delete-versions)

## Installation

To install the project, run the following command:

```text
pip install python-sapcommissions
```

### REST API

This project mimics the usage of the SAP Commissions REST API. Visit
`https://{CALD}-{ENV}.callidusondemand.com/APIDocument` to read the full specification,
replacing `CALD` with your tenant name, and `ENV` with your environment name.

### Terminology

In this documentation, we talk about endpoints and resources, here is what that means.

| Keyword  | Description                                                                      |
| -------- | -------------------------------------------------------------------------------- |
| Endpoint | A type of object that we can interact with, like `Participants` and `Positions`. |
| Method   | An action to perform on an endpoint. See [Methods](#methods) below.              |
| Resource | An instance of an endpoint, a single `Participant` or `Position` for example.    |

## Usage

To get started, import `Connection` and an endpoint of your choosing. In this
example, we'll use `Participants` as the endpoint.

```py
from sapcommissions import Connection
from sapcommissions.endpoints import Participants
```

Initialize a Connection by providing the tenant, environment, username,
and password. Optionally, you can disable ssl verification, if you have problems
connecting to the API from your corporate network.

```python
prod = Connection("CALD", "PRD", "MyUserName", "MySuperSecretPassword", verify_ssl=False)
```

We'll use the `Participants` endpoint to get a list of all participants in the environment.

```py
all_users = Participants(prod).list()
```

## Methods

Every endpoint exposes a number of methods. The most common are `list()` and `get()`.
Some endpoints also expose `create()`, `update()`, and `delete()` methods. Versioned
endpoints like `Participants` also expose `get_versions()`, `create_versions()`, `update_versions()`
and `delete_versions()` methods.

### List

The `list()` method is used to retrieve multiple resources from the endpoint. By default, it returns
the current effective version of the resource (if the endpoint is versioned). To retrieve a
different effective version, you must provide both `startDate` and `endDate` parameters.

In most cases, you will want to apply some kind of filter. For a complete list of available filter
options please visit the [REST API Documentation](#rest-api).

You can limit the number of results returned by providing a `limit`, this is usefull if you want to
explore the data if the endpoint holds a lot of instances. Provide the `raw = True` parameter to
return the json response from the API without converting it to a Python object.

Provide `filter_kwargs` keyword arguments to apply a quick filter. For example
`Positions(prod).list(name='John Doe')` is equivalent to
`Positions(prod).list(filter="name eq 'John Doe'")`. Providing `filter` and `filter_kwargs` will
combine the arguments using the `and` operator, as will multiple `filter_kwargs` arguments.

```py
# Get a list of all positions in the environment.
positions = Positions(prod).list()

# Get a list of all positions with title 'Sales Manager'.
sales_managers = Positions(prod).list(filter="title/name eq 'Sales Manager'")
```

| Argument      | Type   | Required                   | Description                                      |
| ------------- | ------ | -------------------------- | ------------------------------------------------ |
| filter        | `str`  | False                      | A filter string to apply to the list             |
| startDate     | `date` | False if endDate is None   | Filter list of resources effective for startDate |
| endDate       | `date` | False if startDate is None | Filter list of resources effective for endDate   |
| limit         | `int`  | False                      | Limit the number of returned resources           |
| raw           | `bool` | False                      | Return the raw json response from the API        |
| filter_kwargs | `dict` | False                      | Keyword arguments to apply to the filter         |

| Returns          | Description                               |
| ---------------- | ----------------------------------------- |
| `list[Resource]` | A list of resources, single valid version |

### Get

The `get()` method is used to retrieve an existing resource, single (latest) version.
The method takes a single parameter, `seq` (system unique identifier) of the object to
retrieve. The `seq` value for a resource is stored in the first attribute, for
simplicity, it can also be read from the `_seq` property.

| Argument | Type  | Required | Description                                   |
| -------- | ----- | -------- | --------------------------------------------- |
| seq      | `int` | True     | The system unique identifier for the resource |

| Returns    | Description                              |
| ---------- | ---------------------------------------- |
| `Resource` | Requested resource, single valid version |

```py
# Let's say we retrieve a list of positions from the API. The manager attribute refers to a
# position, but does not contain any meaningfull information about the manager yet.
# We can use the `get()` method to enrich the manager data.
positions = Positions(prod).list()

for position in positions:
  if position.manager:
    position.manager = Positions(prod).get(position.manager._seq)
```

### Get ID

`get_id()` is a helper method to simplify the retrieval of a resource by its ID (user
unique identifier). The method takes a single parameter, `id`. If the resource does not provide an
id, or the specified `id` could not be found, it returns `None`.

| Argument | Type  | Required | Description                                 |
| -------- | ----- | -------- | ------------------------------------------- |
| id       | `str` | True     | The user unique identifier for the resource |

| Returns    | Description                                        |
| ---------- | -------------------------------------------------- |
| `Resource` | Requested resource, single valid version           |
| `None`     | Resource does not have an id or could not be found |

```py
position = Positions(prod).get_id('John Doe')

# What would have been required without this method.
position_id_attr = Position._id_attr  # returns 'name'
positions = Positions(prod).list(filter=f"{position_id_attr} eq 'John Doe'")
position = positions[0] if positions else None
```

### Get Versions

The `get_versions()` method is simmilar to the [Get](#get) method, it returns a list
of all versions of the resource.

| Argument | Type  | Required | Description                                   |
| -------- | ----- | -------- | --------------------------------------------- |
| seq      | `int` | True     | The system unique identifier for the resource |

| Returns          | Description                             |
| ---------------- | --------------------------------------- |
| `list[Resource]` | A list of all versions for a  resources |

```py
# Get all versions for a position.
positions = Positions(prod).list()
position = positions[0]

position_versions = Positions(prod).get_versions(first_position._seq)
```

### Create

With the `create()` method, you can create a new instance of the resource. Unlike the
REST API, the `create()` method accepts only a single resource as a parameter.
If successful, the created resource will be returned.

| Argument | Type       | Required | Description                     |
| -------- | ---------- | -------- | ------------------------------- |
| instance | `Resource` | True     | The resource instance to create |

| Returns    | Description             |
| ---------- | ----------------------- |
| `Resource` | Created resource object |

Make sure to provide all required attributes for the resource. Check the documentation
for the resource to see which attributes are required.

```py
# Create a new position, with title 'Account Manager'.
new_position = Position(
  name="John Doe",
  effectiveStartDate=date(2020, 1, 1),
  effectiveEndDate=date(2200, 1, 1),
  title=Title(name="Account Manager"),
)
created_position = Positions(prod).create(new_position)
```

### Create Versions

The `create_versions()` method is used to create new versions of an existing resource.
It is imperative that you provide all versions of the resource, as this method will
overwrite all pre-existing versions with the ones provide. This method can also be used
to end-date an existing resource. All pre-existing versions of the resource will be
overwritten.

| Argument  | Type             | Required | Description                                   |
| --------- | ---------------- | -------- | --------------------------------------------- |
| seq       | `int`            | True     | The system unique identifier for the resource |
| instances | `list[Resource]` | True     | The list of resource instances to create      |

| Returns          | Description                       |
| ---------------- | --------------------------------- |
| `list[Resource]` | List of created resource versions |

```py
# Let's create a new version of the position that we just created.
first_version = Position(
  name="John Doe",
  effectiveStartDate=date(2020, 1, 1),
  effectiveEndDate=date(2020, 12, 31),
  title=Title(name="Account Manager"),
)
second_version = Position(
  name="John Doe",
  effectiveStartDate=date(2021, 1, 1),
  effectiveEndDate=date(2200, 1, 1),
  title=Title(name="Sales Manager"),
)
versions = [first_version, second_version]

created_versions = Positions(prod).create_versions(created_position._seq, versions)
```

### Update

With the `update()` method, you can update an existing resource. If the endpoint is
versioned, this methid only updates a single valid version, matching the effective date
range provided.

| Argument | Type       | Required | Description                   |
| -------- | ---------- | -------- | ----------------------------- |
| update   | `Resource` | True     | The updated resource instance |

| Returns    | Description                                   |
| ---------- | --------------------------------------------- |
| `Resource` | Updated resource object, single valid version |

```py
#  Say that you want to assign all positions with title 'Account Manager' or 'Sales Manager'
# to a position group 'Sales'. We'll assume that the position group already exists.

# Get a list of all positions with title 'Account Manager' or 'Sales Manager'.
positions = (
  Positions(prod)
  .list(filter="title/name eq 'Account Manager' or title/name eq 'Sales Manager'")
)

# Now update the position group and update the position.
for position in positions
  position.positionGroup = PositionGroup(name="Sales")
  Positions(prod).update(position)
```

### Update Versions

The `update_versions()` method is used to update the versions of an existing resource.
It is important to understand the differance between `update()` and `update_versions()`.
[Update](#update) allows a single valid version of the resource to be updated, it must
pre-exist in the environment. With `update_versions()`, you can update multiple versions
at once, and even apply an update without any prior knowledge of pre-existing versions.
The provided versions will be applied to the current existing versions in the
environment.

| Argument | Type             | Required | Description                                   |
| -------- | ---------------- | -------- | --------------------------------------------- |
| seq      | `int`            | True     | The system unique identifier for the resource |
| versions | `list[Resource]` | True     | The list of resource version update to apply  |

| Returns          | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| `list[Resource]` | List of all resource versions after the update was applied |

**Example:**

```py
# Let's revisit our previous example where a position is promoted to a different title. Our position
# already has two versions, the first with a title of 'Account Manager', the second with a title of
# 'Sales Manager' and position group 'Sales'. We can update the position without any pre-existing
# knowledge of these versions.

# We'll need to seq number for the position that we are going to update.
positions = Positions(prod).list(filter="name eq 'John Doe'")
position = positions[0]

# Now we can update the position
updated_position = Position(
  name="John Doe",
  effectiveStartDate=date(2022, 1, 1),
  effectiveEndDate=date(2200, 1, 1),
  title=Title(name="Director"),
  positionGroup=PositionGroup(name="Management"),
)

Positions(prod).update_versions(position_seq, [updated_position])

# [
#   Position(
#     name="John Doe",
#     effectiveStartDate=date(2020, 1, 1),
#     effectiveEndDate=date(2020, 12, 31)
#     title=Title(name="Account Manager"),
#   ),
#   Position(
#     name="John Doe",
#     effectiveStartDate=date(2021, 1, 1),
#     effectiveEndDate=date(2021, 12, 31)
#     title=Title(name="Sales Manager"),
#     positionGroup=PositionGroup(name="Sales"),
#   ),
#   Position(
#     name="John Doe",
#     effectiveStartDate=date(2022, 1, 1),
#     effectiveEndDate=date(2200, 1, 1)
#     title=Title(name="Director"),
#     positionGroup=PositionGroup(name="Management"),
#   ),
# ]
```

### Delete

With the `delete()` method, you can fully delete a resource from the environment, all
effective versions of the resource will be deleted.

| Argument | Type  | Required | Description                                   |
| -------- | ----- | -------- | --------------------------------------------- |
| seq      | `int` | True     | The system unique identifier for the resource |

| Returns | Description                                                |
| ------- | ---------------------------------------------------------- |
| `str`   | Confirmation message `The record is successfully deleted.` |

```py
# Delete a position with the name 'John Doe'.
positions = Positions(prod).list(filter="name eq 'John Doe'")
position = positions[0]

message = Positions(prod).delete(position._seq)
assert message == "The record is successfully deleted."
```

### Delete Versions

The `delete_versions()` method deletes the given versions of the resource. The resulting
gap will either be filled from the previous or next available version of the resource.
The effective dates provided must match an existing version of the resource.

| Argument           | Type   | Required | Description                                          |
| ------------------ | ------ | -------- | ---------------------------------------------------- |
| seq                | `int`  | True     | The system unique identifier for the resource        |
| effectiveStartDate | `date` | True     | The start date of the version to delete              |
| effectiveEndDate   | `date` | True     | The end date of the version to delete                |
| fillFromRight      | `bool` | False    | Default `True`, fill from the next available version |

| Returns | Description                                                                  |
| ------- | ---------------------------------------------------------------------------- |
| `str`   | Confirmation message `All versions in given range are deleted successfully.` |

```py
# Remove the latest version of a position with the name 'John Doe' and fill the gap from the
# previous version.
positions = Positions(prod).list(filter="name eq 'John Doe'")
position = positions[0]

message = (
  Positions(prod)
  .delete_versions(
    seq=position._seq,
    effectiveStartDate=position.effectiveStartDate,
    effectiveEndDate=position.effectiveEndDate,
    fillFromRight=False
  )
)
```
