from sqlalchemy.ext.asyncio import AsyncSession

from db.base import Base, created_at, updated_at
import datetime
from sqlalchemy import (select, exc)

from sqlalchemy.orm import Mapped, mapped_column


# таблица tests в БД
class Answers(Base):
    __tablename__ = 'tests_answers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    test_id: Mapped[int]
    question_id: Mapped[int]
    answer: Mapped[str]
    score: Mapped[int]
    comment: Mapped[str]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @staticmethod
    async def add_answer(test_id, question_id, answer, score, comment, session: AsyncSession):
        answer = Answers(test_id=test_id, question_id=question_id, answer=answer, score=score, comment=comment)
        try:
            answer = await session.merge(answer)
            await session.flush()
            return answer
        except exc.IntegrityError as e:
            await session.rollback()
            print(e)
            return None


    @staticmethod
    async def get_answer(id, session: AsyncSession):
        stmt = select(Answers).filter(Answers.id == id)
        answer = await session.execute(stmt)
        return answer.scalar_one_or_none()

    @staticmethod
    async def get_answers_for_question(test_id, question_id, session: AsyncSession):
        stmt = select(Answers).filter(Answers.test_id == test_id).filter(Answers.question_id == question_id)
        answers = await session.execute(stmt)
        return answers.scalars().all()
