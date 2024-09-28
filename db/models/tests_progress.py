from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import count

from db.base import Base, created_at, updated_at



class Progress(Base):
    __tablename__ = 'progress'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    test_id: Mapped[int]
    user_id: Mapped[int]
    question_number: Mapped[int] = mapped_column(default=0)
    is_passed: Mapped[bool] = mapped_column(default=False)
    score: Mapped[int] = mapped_column(default=0)
    purchased_analysis: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


    @staticmethod
    async def add_progress(test_id, user_id, session):
        progress = Progress(test_id=test_id, user_id=user_id)
        await session.add(progress)



    @staticmethod
    async def update_progress_by_id(progress_id, session: AsyncSession, question_number=None, is_passed=None, score=None, purchased_analysis=None):
        progress = await session.get(Progress, progress_id)

        if progress is not None:
            progress.question_number = question_number if question_number is not None else progress.question_number
            progress.is_passed = is_passed if is_passed is not None else progress.is_passed
            progress.score = score if score is not None else progress.score
            progress.purchased_analysis = purchased_analysis if purchased_analysis is not None else progress.purchased_analysis
        await session.commit()


    @staticmethod
    async def get_progress_by_id(progress_id, session: AsyncSession):
        stmt = select(Progress).filter(Progress.id == progress_id)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()


    @staticmethod
    async def get_progress(test_id, user_id, session: AsyncSession):
        stmt = select(Progress).filter(Progress.test_id == test_id).filter(Progress.user_id == user_id)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()


    @staticmethod
    async def update_progress(test_id, user_id,  session: AsyncSession, question_number=None, is_passed=None, score=None, purchased_analysis=None):
        stmt = select(Progress).filter(Progress.test_id == test_id, Progress.user_id == user_id)
        progress = await session.execute(stmt)

        if progress is not None:
            progress.question_number = question_number if question_number is not None else progress.question_number
            progress.is_passed = is_passed if is_passed is not None else progress.is_passed
            progress.score = score if score is not None else progress.score
            progress.purchased_analysis = purchased_analysis if purchased_analysis is not None else progress.purchased_analysis

        await session.commit()


    @staticmethod
    async def stats(session: AsyncSession):
        stmt = select(count(Progress.id)).filter(Progress.is_passed)
        stmt2 = select(Progress.id).filter(Progress.purchased_analysis)
        passed = (await session.execute(stmt)).scalar_one()
        purchased = (await session.execute(stmt2)).scalar_one()

        return passed, purchased








