Model
=====

.. autosummary:: sapimclient.model

.. admonition:: Read the API Documentation

    Visit :code:`https://{TENANT}.callidusondemand.com/APIDocument`
    to read the full specification, replacing :code:`TENANT` with your
    tenant-id.

    Most of these models are undocumented. For a complete list of attributes,
    refer to the API documentation. Attribute names are converted to snake_case
    to follow standard python conventions.

    All models support the `read` methods of :py:class:`Tenant <sapimclient.client.Tenant>`,
    refer to the API documentation for a full list of supported methods.

Base
----

.. autosummary:: sapimclient.model.base
.. automodule:: sapimclient.model.base

    .. autoclass:: _BaseModel
        :members: typed_fields
    .. autoclass:: Endpoint
        :members: expands
    .. autoclass:: Resource
        :members: seq

    .. autoclass:: AdjustmentContext
    .. autoclass:: Value
    .. autoclass:: ValueClass
    .. autoclass:: ValueUnitType
    .. autoclass:: Reference
    .. autoclass:: Assignment
    .. autoclass:: BusinessUnitAssignment
    .. autoclass:: RuleUsage
    .. autoclass:: RuleUsageList
    .. autoclass:: SalesTransactionAssignment

Data Type
---------

.. autosummary:: sapimclient.model.data_type
.. automodule:: sapimclient.model.data_type

    .. autoclass:: _DataType
    .. autoclass:: CreditType
    .. autoclass:: EarningCode
    .. autoclass:: EarningGroup
    .. autoclass:: EventType
    .. autoclass:: FixedValueType
    .. autoclass:: PositionRelationType
    .. autoclass:: Reason
    .. autoclass:: StatusCode
    .. autoclass:: UnitType

Rule Elements
-------------

.. autosummary:: sapimclient.model.rule_element
.. automodule:: sapimclient.model.rule_element

    .. autoclass:: _RuleElement
    .. autoclass:: Category
    .. autoclass:: FixedValue
    .. autoclass:: CFixedValue
    .. autoclass:: FixedValueVariable
    .. autoclass:: Formula
    .. autoclass:: RelationalMDLT
    .. autoclass:: LookUpTableVariable
    .. autoclass:: RateTable
    .. autoclass:: RateTableVariable
    .. autoclass:: Territory
    .. autoclass:: TerritoryVariable
    .. autoclass:: Variable

Rule Element Owners
-------------------

.. autosummary:: sapimclient.model.rule_element_owner
.. automodule:: sapimclient.model.rule_element_owner

    .. autoclass:: _RuleElementOwner
    .. autoclass:: Plan
    .. autoclass:: Position
    .. autoclass:: Title

Resource
--------

.. autosummary:: sapimclient.model.resource

.. hint::
    See :ref:`usage:examples`

.. automodule:: sapimclient.model.resource

    .. autoclass:: AppliedDeposit
    .. autoclass:: AuditLog
    .. autoclass:: Balance
    .. autoclass:: BusinessUnit
    .. autoclass:: Calendar
    .. autoclass:: CategoryClassifier
    .. autoclass:: CategoryTree
    .. autoclass:: Commission
    .. autoclass:: Credit
    .. autoclass:: Deposit
    .. autoclass:: EarningGroupCode
    .. autoclass:: GenericClassifier
    .. autoclass:: GenericClassifierType
    .. autoclass:: GlobalFieldName
    .. autoclass:: Incentive
    .. autoclass:: Measurement
    .. autoclass:: PrimaryMeasurement
    .. autoclass:: SecondaryMeasurement
    .. autoclass:: Message
    .. autoclass:: MessageLog
    .. autoclass:: Participant
    .. autoclass:: PaymentMapping
    .. autoclass:: PaymentSummary
    .. autoclass:: Period
    .. autoclass:: PeriodType
    .. autoclass:: Pipeline
    .. autoclass:: PositionGroup
    .. autoclass:: PositionRelation
    .. autoclass:: PostalCode
    .. autoclass:: ProcessingUnit
    .. autoclass:: Product
    .. autoclass:: Quota
    .. autoclass:: SalesOrder
    .. autoclass:: SalesTransaction
    .. autoclass:: User
    .. autoclass:: PlanComponent
    .. autoclass:: Rule
    .. autoclass:: CreditRule
    .. autoclass:: CommissionRule
    .. autoclass:: DepositRule
    .. autoclass:: MeasurementRule

Pipeline
--------

.. autosummary:: sapimclient.model.pipeline

.. hint::
    See example :ref:`example_comp-and-pay`

.. automodule:: sapimclient.model.pipeline

    .. autoclass:: _PipelineJob
    .. autoclass:: ResetFromValidate
    .. autoclass:: Purge
    .. autoclass:: XMLImport
    .. autoclass:: _PipelineRunJob
    .. autoclass:: Classify
    .. autoclass:: Allocate
    .. autoclass:: Reward
    .. autoclass:: Pay
    .. autoclass:: Summarize
    .. autoclass:: Compensate
    .. autoclass:: CompensateAndPay
    .. autoclass:: ResetFromClassify
    .. autoclass:: ResetFromAllocate
    .. autoclass:: ResetFromReward
    .. autoclass:: ResetFromPay
    .. autoclass:: Post
    .. autoclass:: Finalize
    .. autoclass:: ReportsGeneration
    .. autoclass:: UndoPost
    .. autoclass:: UndoFinalize
    .. autoclass:: CleanupDefferedResults
    .. autoclass:: UpdateAnalytics
    .. autoclass:: _ImportJob
    .. autoclass:: Validate
    .. autoclass:: Transfer
    .. autoclass:: ValidateAndTransfer
    .. autoclass:: ValidateAndTransferIfAllValid
    .. autoclass:: TransferIfAllValid
