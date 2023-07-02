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
Pipelines(env).generate_reports(...)
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
Pipelines(env).classify(...)
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
Pipelines(env).allocate(...)
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

### Reward

Run Reward pipeline.

```py
Pipelines(env).reward(...)
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
Pipelines(env).pay(...)
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
Pipelines(env).summarize(...)
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
Pipelines(env).compensate(...)
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
Pipelines(env).comp_and_pay(...)
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
Pipelines(env).post(...)
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
Pipelines(env).undo_post(...)
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
Pipelines(env).finalize(...)
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
Pipelines(env).undo_finalize(...)
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
Pipelines(env).reset_from_classify(...)
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
Pipelines(env).reset_from_allocate(...)
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
Pipelines(env).reset_from_reward(...)
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
Pipelines(env).reset_from_pay(...)
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
Pipelines(env).cleanup_deferred_results(...)
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
Pipelines(env).approve_calculated_data(...)
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
Pipelines(env).purge_approved_data(...)
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
Pipelines(env).update_analytics(...)
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
Pipelines(env).validate(...)
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
Pipelines(env).transfer(...)
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

### Transfer If All Valid

Transfer data from stage only if all data is valid.

```py
Pipelines(env).transfer_if_all_valid(...)
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

### Validate and Transfer

Validate and Transfer data from stage, leave invalid data.

```py
Pipelines(env).validate_and_transfer(...)
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

Validate and Transfer data from stage, leave invalid data.

```py
Pipelines(env).validate_and_transfer_if_all_valid(...)
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
Pipelines(env).reset_from_validate(...)
```

| Argument          | Type   | Required | Description                                             |
| ----------------- | ------ | -------- | ------------------------------------------------------- |
| calendarSeq       | `str`  | True     | Calendar system identifier                              |
| periodSeq         | `str`  | True     | Period system identifier                                |
| batchName         | `str`  | True     | Batch name.                                             |
| runStats          | `bool` | False    | Run statistics, default is True.                        |
| processingUnitSeq | `str`  | False    | Processing Unit system identifier, required if enabled. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### Purge

Run Purge import data.

```py
Pipelines(env).purge(...)
```

| Argument  | Type  | Required | Description |
| --------- | ----- | -------- | ----------- |
| batchName | `str` | True     | Batch name. |

| Returns    | Description                                             |
| ---------- | ------------------------------------------------------- |
| `Pipeline` | `Pipeline` instance containing only the pipelineRunSeq. |

### XML Import

Run XML Import.

```py
Pipelines(env).xml_import(...)
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
