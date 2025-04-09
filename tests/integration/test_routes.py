import pytest
from httpx import AsyncClient, ASGITransport

from src.app import app
from src.models import RequestM


@pytest.mark.parametrize(
    'body, status_code, should_inserted_count',
    [
        ({'tron_address': 'TUjx6w55Nx9G4GjjRNEB4e7w5BUH3WmJTZ'}, 200, 1),
        ({'tron_address': 'TAzQBLhBDEK7svczWtpD5RgabCNfiFhuN5'}, 404, 1),
        ({'tron_address': ''}, 422, 0),
        ({'tron_address': 'qwertyu'}, 422, 0),
        ({'trn_adr': 'TUjx6w55Nx9G4GjjRNEB4e7w5BUH3WmJTZ'}, 422, 0),
        ({}, 422, 0),
    ]
)
@pytest.mark.asyncio
async def test_get_account_resources(body, status_code, should_inserted_count, db_session, empty_requests):
    async with AsyncClient(transport=ASGITransport(app), base_url='http://test') as async_client:
        response = await async_client.post('/wallet_info/', json=body)
        assert response.status_code == status_code
        assert response.json()

        inserted_request = db_session.query(RequestM).all()
        assert len(inserted_request) == should_inserted_count
