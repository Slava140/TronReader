from fastapi import HTTPException
from requests import HTTPError
from sqlalchemy.orm import Session
from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from tronpy.providers import HTTPProvider

from src.DAO import RequestDAO
from src.config import settings
from src.schemas import AccountResourceInfoS, AddRequestS, GetRequestS


class RequestService:
    @classmethod
    def add(cls, db_session: Session, schema: AddRequestS) -> None:
        RequestDAO.add(db_session, schema)

    @classmethod
    def get_many(cls, db_session: Session, page: int, limit: int) -> dict[str, list[GetRequestS]]:
        requests_list = RequestDAO.get_many(db_session, page, limit)
        if not requests_list:
            raise HTTPException(404, 'Requests was not found.')
        return {'data': requests_list}



class AccountService:
    def __init__(self, address: str):
        self.address = address

    def get_resource_info(self, db_session: Session) -> AccountResourceInfoS:
        client = Tron(HTTPProvider(api_key=settings.TRONGRID_API_KEY))
        try:
            balance = client.get_account_balance(self.address)
            resources = client.get_account_resource(self.address)
            resource_info = AccountResourceInfoS(
                balance=balance,
                bandwidth=resources.get('NetLimit') + resources.get('freeNetLimit'),
                energy=resources.get('EnergyLimit', 0)
            )
            return resource_info

        except HTTPError:
            raise HTTPException(502, 'Cannot get data. Try again later')

        except AddressNotFound:
            raise HTTPException(404, 'Address was not found.')

        finally:
            RequestService.add(db_session, AddRequestS(tron_address=self.address))
