from contextlib import nullcontext as does_not_raise

import pytest

from src.DAO import RequestDAO
from src.schemas import AddRequestS


@pytest.mark.usefixtures('empty_requests')
class TestRequest:
    def test_add(self, db_session, tron_address):
        assert RequestDAO.add(db_session, AddRequestS(tron_address=tron_address)) is None

    @pytest.mark.parametrize(
        'page, limit, res, expectation',
        [
            (0, 0, 0, pytest.raises(ValueError)),
            (1, 0, 0, pytest.raises(ValueError)),
            (0, 2, 0, pytest.raises(ValueError)),
            (9, 9, 0, does_not_raise()),
            (1, 2, 2, does_not_raise()),
            (2, 1, 1, does_not_raise()),
        ]
    )
    def test_get_many(self, db_session, page, limit, res, expectation, add_requests):
        with expectation:
            assert len(RequestDAO.get_many(db_session, page, limit)) == res
