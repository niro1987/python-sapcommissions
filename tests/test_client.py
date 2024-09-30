"""Test for SAP Commissions Client."""
# pylint: disable=all

from datetime import datetime

from sapcommissions import CommissionsClient, model


async def test_client_create_participant(
    client: CommissionsClient,
) -> None:
    """Test the CommissionsClient."""
    pa: model.Participant = model.Participant(
        user_id="DUMMY",
        payee_id="DUMMY",
        last_name="DUMMY",
        effective_start_date=datetime(2024, 1, 1),
        effective_end_date=datetime(2200, 1, 1),
    )
    result = await client.create(pa)
    print(result)  # noqa: T201
