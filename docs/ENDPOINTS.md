# Endpoints

- [Endpoints](#endpoints)
  - [List of Endpoints](#list-of-endpoints)
  - [Run Pipelines](#run-pipelines)
    - [Generate Reports](#generate-reports)
    - [Classify](#classify)
    - [Allocate](#allocate)
    - [Reward](#reward)
    - [Pay](#pay)
    - [Summarize](#summarize)
    - [Compensate](#compensate)
    - [Compensate and Pay](#compensate-and-pay)
    - [Post](#post)
    - [Undo Post](#undo-post)
    - [Finalize](#finalize)
    - [Undo Finalize](#undo-finalize)
    - [Reset From Classify](#reset-from-classify)
    - [Reset From Allocate](#reset-from-allocate)
    - [Reset From Reward](#reset-from-reward)
    - [Reset From Pay](#reset-from-pay)
    - [Cleanup Deffered Results](#cleanup-deffered-results)
    - [Approve Calculated Data](#approve-calculated-data)
    - [Purge Approved Data](#purge-approved-data)
    - [Update Analytics](#update-analytics)
    - [Validate](#validate)
    - [Transfer](#transfer)
    - [Transfer If All Valid](#transfer-if-all-valid)
    - [Validate and Transfer](#validate-and-transfer)
    - [Validate and Transfer If All Valid](#validate-and-transfer-if-all-valid)
    - [Reset From Validate](#reset-from-validate)
    - [Purge](#purge)
    - [XML Import](#xml-import)

## List of Endpoints

| Endpoint               | Methods                                                                                                                                                                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AppliedDeposits        | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| AuditLogs              | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| Balances               | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| BusinessUnits          | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update]                                                                                                                                                                       |
| Calendars              | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update]                                                                                                                                                                       |
| Categories             | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| CategoryClassifiers    | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update]                                                                                                                                                                       |
| CategoryTrees          | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| Commissions            | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| Credits                | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update]                                                                                                                                                                       |
| CreditTypes            | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| Customers              | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| Deposits               | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| EarningCodes           | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| EarningGroupCodes      | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| EarningGroups          | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| EventTypes             | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| FixedValues            | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| FixValueTypes          | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| FixedValueVariables    | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| Formulas               | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| GenericClassifiers     | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| GenericClassifierTypes | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| GlobalFieldNames       | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| Groups                 | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| Incentives             | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| LookUpTables           | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| LookUpTableVariables   | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| Measurements           | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| MessageLogs            | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| Messages               | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| Participants           | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| PaymentMappings        | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| Payments               | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| PatmentSummarys        | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| Periods                | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| Pipelines              | [`Get`][get], [`List`][list], [Run Pipelines](#run-pipelines) (see below)                                                                                                                                                                  |
| Plans                  | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| PositionGroups         | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| PositionRelations      | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| PositionRelationTypes  | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| Positions              | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| PrimaryMeasurements    | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| ProcessingUnits        | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update]                                                                                                                                                                       |
| Products               | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| Quotas                 | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| RateTables             | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| RateTableVariables     | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| Reasons                | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| SalesOrders            | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| SalesTransactions      | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| SecondaryMeasurements  | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| StatusCodes            | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| Territories            | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| TerritoryVariables     | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| Titles                 | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |
| UnitTypes              | [`Get`][get], [`List`][list]                                                                                                                                                                                                               |
| Users                  | [`Create`][create], [`Get`][get], [`List`][list], [`Update`][update], [`Delete`][delete]                                                                                                                                                   |
| Variables              | [`Create`][create], [`Create Versions`][create-versions], [`Get`][get], [`Get Versions`][get-versions], [`List`][list], [`Update`][update], [`Update Versions`][update-versions], [`Delete`][delete], [`Delete Versions`][delete-versions] |

## Run Pipelines

Apart from the [`Get`][get] and [`List`][list] methods, you can also run various pipelines.

### Generate Reports

Run Reports Generation pipeline.

```py
# Generate Payments Report for Admin Group.
from sapcommissions import Connection, ReportFormat
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).generate_reports(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
  formats=[ReportFormat.NATIVE],
  reports=["Payments Report"],
  groups=["CALD Compensation Reports Admin Group"],
)
```

| Argument          | Type                 | Required | Description                                                             |
| ----------------- | -------------------- | -------- | ----------------------------------------------------------------------- |
| calendarSeq       | `str`                | True     | Calendar system identifier                                              |
| periodSeq         | `str`                | True     | Period system identifier                                                |
| formats           | `list[ReportFormat]` | True     | List of report formats                                                  |
| reports           | `list[str]`          | True     | List of report names                                                    |
| groups            | `list[str]`          | False    | List of BO group names. Use either groups or positionSeqs parameter.    |
| positionSeqs      | `list[str]`          | False    | List of position system identifiers. Use either groups or positionSeqs. |
| runStats          | `bool`               | False    | Run statistics, default is True.                                        |
| processingUnitSeq | `str`                | False    | Processing Unit system identifier, required if enabled.                 |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Classify

Run Classify pipeline.

```py
# Classify new and modified transactions.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).classify(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
  incremental=True,
)
```

| Argument          | Type   | Required | Description                                                   |
| ----------------- | ------ | -------- | ------------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                                    |
| periodSeq         | `str`  | True     | Period system identifier                                      |
| incremental       | `bool` | False    | Only process new and modified transactions. Default is False. |
| runStats          | `bool` | False    | Run statistics, default is True.                              |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled.       |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Allocate

Run Allocate pipeline.

```py
# Allocate all credits and calculate primary measurements.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).allocate(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type        | Required | Description                                                |
| ----------------- | ----------- | -------- | ---------------------------------------------------------- |
| calendarSeq       | `str`       | True     | Calendar system identifier                                 |
| periodSeq         | `str`       | True     | Period system identifier                                   |
| incremental       | `bool`      | False    | Only process new and modified credits. Default is False.   |
| positionSeqs      | `list[str]` | False    | Run for specific positions. Provide a list of positionSeq. |
| runStats          | `bool`      | False    | Run statistics, default is True.                           |
| processingUnitSeq | `str`       | False    | Processing Unit system identifier, required if enabled.    |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Reward

Run Reward pipeline.

```py
# Calculate secondary measurements, incentives and deposit values.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).reward(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type        | Required | Description                                                |
| ----------------- | ----------- | -------- | ---------------------------------------------------------- |
| calendarSeq       | `str`       | True     | Calendar system identifier                                 |
| periodSeq         | `str`       | True     | Period system identifier                                   |
| positionSeqs      | `list[str]` | False    | Run for specific positions. Provide a list of positionSeq. |
| runStats          | `bool`      | False    | Run statistics, default is True.                           |
| processingUnitSeq | `str`       | False    | Processing Unit system identifier, required if enabled.    |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Pay

Run Pay pipeline.

```py
# Calculate payments and balances.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).pay(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Summarize

Run Summarize pipeline, combination of [classify](#classify) and [allocate](#allocate).

```py
# Run calculations up to primary measurements.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).classify(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type        | Required | Description                                                   |
| ----------------- | ----------- | -------- | ------------------------------------------------------------- |
| calendarSeq       | `str`       | True     | Calendar system identifier                                    |
| periodSeq         | `str`       | True     | Period system identifier                                      |
| incremental       | `bool`      | False    | Only process new and modified transactions. Default is False. |
| positionSeqs      | `list[str]` | False    | Run for specific positions. Provide a list of positionSeq.    |
| runStats          | `bool`      | False    | Run statistics, default is True.                              |
| processingUnitSeq | `str`       | False    | Processing Unit system identifier, required if enabled.       |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Compensate

Run Compensate pipeline, combination of [classify](#classify), [allocate](#allocate) and [reward](#reward).

```py
# Run calculations up to deposit values, processing only new and modified transactions
# and credits and remove stale results.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).compensate(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
  incremental=True,
  removeStaleResults-True,
)
```

| Argument           | Type        | Required | Description                                                   |
| ------------------ | ----------- | -------- | ------------------------------------------------------------- |
| calendarSeq        | `str`       | True     | Calendar system identifier                                    |
| periodSeq          | `str`       | True     | Period system identifier                                      |
| incremental        | `bool`      | False    | Only process new and modified transactions. Default is False. |
| positionSeqs       | `list[str]` | False    | Run for specific positions. Provide a list of positionSeq.    |
| removeStaleResults | `bool`      | False    | Enable remove stale results. Default is False.                |
| runStats           | `bool`      | False    | Run statistics, default is True.                              |
| processingUnitSeq  | `str`       | False    | Processing Unit system identifier, required if enabled.       |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Compensate and Pay

Run Compensate and Pay pipeline, full calculation pipeline.

```py
# Run Compensate and Pay for specified positions.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines, Positions

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")
positions = Positions(env).list(filter="positionGroup/name eq 'A-Team'")
positions_seq = [position.ruleElementOwnerSeq for position in positions]

pipeline = Pipelines(env).comp_and_pay(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
  positionSeqs=positions_seq,
)
```

| Argument           | Type        | Required | Description                                                   |
| ------------------ | ----------- | -------- | ------------------------------------------------------------- |
| calendarSeq        | `str`       | True     | Calendar system identifier                                    |
| periodSeq          | `str`       | True     | Period system identifier                                      |
| incremental        | `bool`      | False    | Only process new and modified transactions. Default is False. |
| positionSeqs       | `list[str]` | False    | Run for specific positions. Provide a list of positionSeq.    |
| removeStaleResults | `bool`      | False    | Enable remove stale results. Default is False.                |
| runStats           | `bool`      | False    | Run statistics, default is True.                              |
| processingUnitSeq  | `str`       | False    | Processing Unit system identifier, required if enabled.       |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Post

Run Post pipeline.

```py
# Post payments and calculate balances.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).post(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Undo Post

Run Undo Post pipeline.

```py
# Undo Last Post Run.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).undo_post(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Finalize

Run Finalize pipeline.

```py
# Finalize payments for a period.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).finalize(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Undo Finalize

Run Undo Finalize pipeline.

```py
# Undo Last Finalize Run.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).undo_finalize(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Reset From Classify

Run Reset From Classify pipeline.

```py
# Reset all data from classification and forward.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).reset_from_classify(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Reset From Allocate

Run Reset From Allocate pipeline.

```py
# Reset all data from credit and forward.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).reset_from_allocate(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Reset From Reward

Run Reset From Reward pipeline.

```py
# Reset all data from deposit and forward.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).reset_from_reward(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Reset From Pay

Run Reset From Pay pipeline.

```py
# Reset all data from payment and forward.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).reset_from_pay(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Cleanup Deffered Results

Run Cleanup Deffered Results pipeline.

```py
# Clean up deferred results for all periods in 2023.
from sapcommissions import Connection
from sapcommissions.endpoints import Calendars, Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
calendar = Calendars(env).get_id("Monthly Calendar")
periods = Periods(env).list(
  filter=(
    f"calendar eq {calendar.calendarSeq}"
    f" and periodType eq {calendar.minorPeriodType.periodTypeSeq}"
    f" and startDate ge '1/1/2023' and endDate le '1/1/2024'"
  )
)

for period in periods:
  Pipelines(env).cleanup_deferred_results(
    calendarSeq=calendar.calendarSeq,
    periodSeq=period.periodSeq,
  )
```

| Argument          | Type  | Required | Description                                             |
| ----------------- | ----- | -------- | ------------------------------------------------------- |
| calendarSeq       | `str` | True     | Calendar system identifier                              |
| periodSeq         | `str` | True     | Period system identifier                                |
| processingUnitSeq | `str` | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Approve Calculated Data

Run Approve Calculated Data pipeline.

```py
# Approve calculated data.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).approve_calculated_data(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type  | Required | Description                                             |
| ----------------- | ----- | -------- | ------------------------------------------------------- |
| calendarSeq       | `str` | True     | Calendar system identifier                              |
| periodSeq         | `str` | True     | Period system identifier                                |
| processingUnitSeq | `str` | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Purge Approved Data

Run Purge Approved Data pipeline.

```py
# Purge approved data.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).purge_approved_data(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type  | Required | Description                                             |
| ----------------- | ----- | -------- | ------------------------------------------------------- |
| calendarSeq       | `str` | True     | Calendar system identifier                              |
| periodSeq         | `str` | True     | Period system identifier                                |
| processingUnitSeq | `str` | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Update Analytics

Run Update Analytics pipeline.

```py
# Update Analytics.
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

pipeline = Pipelines(env).update_analytics(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Validate

Validate data from stage.

```py
# Revalidate an entire batch.
from sapcommissions import Connection, Revalidate
from sapcommissions.endpoints import Calendars, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
calendar = Calendars(env).get_id("Monthly Calendar")

pipeline = Pipelines(env).validate(
  calendarSeq=calendar.calendarSeq,
  batchName="CALD_ENV_OGPO_20230101_123456_positions_file.txt",
  revalidate=Revalidate.ALL,
)
```

| Argument          | Type            | Required | Description                                                                          |
| ----------------- | --------------- | -------- | ------------------------------------------------------------------------------------ |
| calendarSeq       | `str`           | True     | Calendar system identifier                                                           |
| batchName         | `str`           | True     | Batch name.                                                                          |
| runMode           | `ImportRunMode` | False    | Import all or only new and modified data. Default: ALL.                              |
| revalidate        | `Revalidate`    | False    | Revalidate all or only errors if provided. Do not revalidate if None. Default: None. |
| runStats          | `bool`          | False    | Run statistics, default is True.                                                     |
| processingUnitSeq | `str`           | False    | Processing Unit system identifier, required if enabled.                              |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Transfer

Transfer data from stage, leave invalid data.

```py
# Transfer new and modified data.
from sapcommissions import Connection, ImportRunMode
from sapcommissions.endpoints import Calendars, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
calendar = Calendars(env).get_id("Monthly Calendar")

pipeline = Pipelines(env).transfer(
  calendarSeq=calendar.calendarSeq,
  batchName="CALD_ENV_OGPO_20230101_123456_positions_file.txt",
  runMode=ImportRunMode.NEW,
)
```

| Argument          | Type            | Required | Description                                             |
| ----------------- | --------------- | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`           | True     | Calendar system identifier                              |
| batchName         | `str`           | True     | Batch name.                                             |
| runMode           | `ImportRunMode` | False    | Import all or only new and modified data. Default: ALL. |
| runStats          | `bool`          | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`           | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Transfer If All Valid

Transfer data from stage only if all data is valid.

```py
# Transfer data, but only if the entire file is valid.
from sapcommissions import Connection
from sapcommissions.endpoints import Calendars, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
calendar = Calendars(env).get_id("Monthly Calendar")

pipeline = Pipelines(env).transfer_if_all_valid(
  calendarSeq=calendar.calendarSeq,
  batchName="CALD_ENV_OGPO_20230101_123456_positions_file.txt",
)
```

| Argument          | Type            | Required | Description                                             |
| ----------------- | --------------- | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`           | True     | Calendar system identifier                              |
| batchName         | `str`           | True     | Batch name.                                             |
| runMode           | `ImportRunMode` | False    | Import all or only new and modified data. Default: ALL. |
| runStats          | `bool`          | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`           | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Validate and Transfer

Validate and Transfer data from stage, leave invalid data.

```py
# Validate and transfer data from stage, leave invalid data.
from sapcommissions import Connection
from sapcommissions.endpoints import Calendars, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
calendar = Calendars(env).get_id("Monthly Calendar")

pipeline = Pipelines(env).validate_and_transfer(
  calendarSeq=calendar.calendarSeq,
  batchName="CALD_ENV_OGPO_20230101_123456_positions_file.txt",
)
```

| Argument          | Type            | Required | Description                                                                          |
| ----------------- | --------------- | -------- | ------------------------------------------------------------------------------------ |
| calendarSeq       | `str`           | True     | Calendar system identifier                                                           |
| batchName         | `str`           | True     | Batch name.                                                                          |
| runMode           | `ImportRunMode` | False    | Import all or only new and modified data. Default: ALL.                              |
| revalidate        | `Revalidate`    | False    | Revalidate all or only errors if provided. Do not revalidate if None. Default: None. |
| runStats          | `bool`          | False    | Run statistics, default is True.                                                     |
| processingUnitSeq | `str`           | False    | Processing Unit system identifier, required if enabled.                              |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Validate and Transfer If All Valid

Validate and Transfer data from stage, if all data is valid.

```py
# Validate and transfer data from stage, if all data is valid.
from sapcommissions import Connection
from sapcommissions.endpoints import Calendars, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
calendar = Calendars(env).get_id("Monthly Calendar")

pipeline = Pipelines(env).validate_and_transfer_if_all_valid(
  calendarSeq=calendar.calendarSeq,
  batchName="CALD_ENV_OGPO_20230101_123456_positions_file.txt",
)
```

| Argument          | Type            | Required | Description                                                                          |
| ----------------- | --------------- | -------- | ------------------------------------------------------------------------------------ |
| calendarSeq       | `str`           | True     | Calendar system identifier                                                           |
| batchName         | `str`           | True     | Batch name.                                                                          |
| runMode           | `ImportRunMode` | False    | Import all or only new and modified data. Default: ALL.                              |
| revalidate        | `Revalidate`    | False    | Revalidate all or only errors if provided. Do not revalidate if None. Default: None. |
| runStats          | `bool`          | False    | Run statistics, default is True.                                                     |
| processingUnitSeq | `str`           | False    | Processing Unit system identifier, required if enabled.                              |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Reset From Validate

Run Reset From Validate.

```py
from sapcommissions import Connection
from sapcommissions.endpoints import Periods, Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")
period = Periods(env).get_id("January 2023")

# Remove a batch from a period.
pipeline = Pipelines(env).reset_from_validate(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
  batchName="CALD_ENV_OGPO_20230101_123456_positions_file.txt",
)

# Remove all batches from a period.
pipeline = Pipelines(env).reset_from_validate(
  calendarSeq=period.calendar.calendarSeq,
  periodSeq=period.periodSeq,
)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| batchName         | `str`  | False    | Batch name. Remove all batches if None.                 |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Purge

Run Purge import data.

```py
# Remove a batch from stage.
from sapcommissions import Connection
from sapcommissions.endpoints import Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")

pipeline = Pipelines(env).purge(
  batchName="CALD_ENV_OGPO_20230101_123456_positions_file.txt",
)
```

| Argument  | Type  | Required | Description          |
| --------- | ----- | -------- | -------------------- |
| batchName | `str` | True     | Batch name to purge. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### XML Import

Run XML Import.

```py
# Import plan data, allow updates on existing objects.
import os

from sapcommissions import Connection
from sapcommissions.endpoints import Pipelines

env = Connection("CALD", "ENV", "MyUserName", "MySuperSecretPassword")

filename = "path/to/plan.xml"
with open(filename, "r") as file:
  pipeline = Pipelines(env).xml_import(
    xmlFileName=os.path.basename(filename),
    xmlFileContent=file.read(),
    updateExistingObjects=True,
  )
```

| Argument              | Type   | Required | Description                                 |
| --------------------- | ------ | -------- | ------------------------------------------- |
| xmlFileName           | `str`  | True     | Filename of imported file.                  |
| xmlFileContent        | `str`  | True     | File content of imported file.              |
| updateExistingObjects | `bool` | False    | Update existing opbjects. Default is False. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

<!-- Links -->

[create]: README.md#create
[create-versions]: README.md#create-versions
[get]: README.md#get
[get-versions]: README.md#get-versions
[list]: README.md#list
[update]: README.md#update
[update-versions]: README.md#update-versions
[delete]: README.md#delete
[delete-versions]: README.md#delete-versions
