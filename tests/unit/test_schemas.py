from contextlib import nullcontext as does_not_raise

import pytest
from pydantic import ValidationError, BaseModel

from src.schemas import TronAddress


@pytest.mark.parametrize(
    'address, res, expectation',
    [
        ('TUjx6w55Nx9G4GjjRNEB4e7w5BUH3WmJTZ', 34, does_not_raise()),
        ('\n  TUjx6w55Nx9G4GjjRNEB4e7w5BUH3WmJTZ   ', 34, does_not_raise()),
        ('', 0, pytest.raises(ValidationError)),
        ('werhbvft', 0, pytest.raises(ValidationError)),
        (12345, 0, pytest.raises(ValidationError)),
    ]
)
def test_tron_address(address, res, expectation):
    class T(BaseModel):
        addr: TronAddress

    with expectation:
        schema = T(addr=address)
        assert len(schema.addr.get_secret_value()) == res
