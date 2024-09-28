from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base, created_at, updated_at
import datetime
from sqlalchemy import (select, exc)

from sqlalchemy.orm import Mapped, mapped_column

from db.models.tests_answers import Answers


# таблица tests в БД
class Questions(Base):
    __tablename__ = 'tests_questions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_id: Mapped[int]
    question_number: Mapped[int]
    question: Mapped[str]


    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


    @staticmethod
    async def add_question(test_id, question_number, question, session: AsyncSession):
        question = Questions(test_id=test_id, question_number=question_number, question=question)
        try:
            question = await session.merge(question)
            await session.flush()
        except exc.IntegrityError as e:
            await session.rollback()
            print(e)
            question = None

        return question


    @staticmethod
    async def get_question_by_id(id, session: AsyncSession):
        stmt = select(Questions).filter(Questions.id == id)
        return (await session.execute(stmt)).scalar_one_or_none()


    @staticmethod
    async def get_question_by_test_id(test_id, question_number, session: AsyncSession):
        stmt = select(Questions).filter(Questions.test_id == test_id).filter(Questions.question_number == question_number)
        return (await session.execute(stmt)).scalar_one_or_none()




