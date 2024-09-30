Usage
=====

Installation
------------

To use this project, install it with pip:

.. code-block:: console

   (.venv) $ pip install python-sapcommissions

This project includes some command-line-interface commands,
to install the required dependencies, install them with pip:

.. code-block:: console

    (.venv) $ pip install python-sapcommissions[cli]

Examples
--------

.. _example_comp-and-pay:

Run Comp & Pay
``````````````

This example shows how to run Compensate And Pay for
period ``January 2024`` on the ``Main Monthly Calendar``.

.. code-block:: python

   from aoihttp
   from sapcommissions import CommissionsClient, model
   from sapcommissions.const import PipelineState, PipelineStatus
   from sapcommissions.model.base import Reference

   async def run_comp_and_pay(
      client: CommissionsClient,
      calendar_name: str,
      period_name: str,
   ) -> None:
      """Run Comp and Pay for the specified period in the specified calendar."""

      period: model.Period = await client.read_first(
         resource_cls=model.Period,
         filters=f"calendar/name eq '{calendar_name}' and name eq '{period_name}'",
      )
      assert isinstance(period, model.Period)
      assert isinstance(period.calendar, Reference)

      job: model.CompensateAndPay = model.CompensateAndPay(
         period_seq=period.period_seq,
         calendar_seq=period.calendar.key,
      )

      result: model.Pipeline = await client.run_pipeline(job)

      # Optionally you can wait for the pipeline to complete.
      while result.state != PipelineState.Done:
         await asyncio.sleep(60)
         result = await client.read(result)

      assert result.status == PipelineStatus.Successful
