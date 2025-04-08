from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.models import RequestM
from src.schemas import AddRequestS, GetRequestS


class RequestDAO:
    @classmethod
    def add(cls, db_session: Session, schema: AddRequestS) -> None:
        request_model = RequestM(**schema.model_dump())
        db_session.add(request_model)
        db_session.commit()

    @classmethod
    def get_many(cls, db_session: Session, page: int, limit: int) -> list[GetRequestS]:
        if page < 1 or limit < 1:
            raise ValueError('Page and limit must be positive.')

        result = db_session.query(
            RequestM
        ).order_by(
            desc(RequestM.created_at)
        ).limit(
            limit
        ).offset(
            (page-1) * limit
        )


        return [GetRequestS.model_validate(req.__dict__) for req in result]
