import string
from datetime import datetime, timezone
from decimal import Decimal
from typing import Annotated
from tronpy.keys import is_base58check_address, is_address

from pydantic import BaseModel, BeforeValidator, SecretStr, NonNegativeInt, PlainSerializer, AfterValidator, \
    StringConstraints


def is_utc_datetime_validator(value: datetime) -> datetime:
    if isinstance(value, str):
        return datetime.fromisoformat(value).astimezone(timezone.utc)
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    else:
        raise ValueError('Value must be datetime.')


def is_tron_address(value: SecretStr) -> SecretStr:
    address = value.get_secret_value().strip(string.whitespace)
    if address == '' or not is_address(address):
        raise ValueError('Incorrect address')

    return SecretStr(address)



UTCDatetime = Annotated[datetime, BeforeValidator(is_utc_datetime_validator)]
TronAddress = Annotated[
    SecretStr,
    StringConstraints(min_length=1, max_length=50),
    AfterValidator(is_tron_address),
    PlainSerializer(lambda v: v.get_secret_value()),
]


class BaseRequestS(BaseModel):
    tron_address: TronAddress


class GetRequestS(BaseRequestS):
    id: int
    created_at: UTCDatetime


class AddRequestS(BaseRequestS):
    ...


class TronAddressBody(BaseModel):
    tron_address: TronAddress


class AccountResourceInfoS(BaseModel):
    balance: Decimal
    bandwidth: NonNegativeInt
    energy: NonNegativeInt