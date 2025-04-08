from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas import TronAddressBody, AccountResourceInfoS, GetRequestS
from src.services import AccountService, RequestService

router = APIRouter(prefix='/wallet_info')


@router.post('/')
def get_account_resources(body: TronAddressBody, db_session: Session = Depends(get_db)) -> AccountResourceInfoS:
    account_service = AccountService(body.tron_address.get_secret_value())
    return account_service.get_resource_info(db_session)


@router.get('/')
def get_last_requests(page: int = 1, limit: int = 10, db_session: Session = Depends(get_db)) -> dict[str, list[GetRequestS]]:
    return RequestService.get_many(db_session, page, limit)
