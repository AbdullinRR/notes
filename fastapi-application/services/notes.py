from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import connection
from core.models.notes import NoteModel
from core.schemas.notes import NoteCreate, NoteUpdate


class NoteService:
    @staticmethod
    @connection
    async def delete_note(note_id: int, session: AsyncSession):
        try:
            result = await session.execute(
                select(NoteModel).where(NoteModel.id == note_id)
            )
            note = result.scalars().first()
            await session.delete(note)
            await session.commit()

            return True

        except Exception as e:
            print(e)
            await session.rollback()
            return None

    @staticmethod
    @connection
    async def update_note(note_id, note: NoteUpdate, session: AsyncSession):
        try:
            result = await session.execute(
                select(NoteModel).where(NoteModel.id == note_id)
            )
            note_db = result.scalars().first()
            if not note_db:
                return None
            note_db.content = note.content
            await session.commit()
            await session.refresh(note_db)
            return note_db

        except Exception as e:
            print(e)
            await session.rollback()
            return None

    @staticmethod
    @connection
    async def get_notes(session: AsyncSession):
        try:
            notes = await session.execute(select(NoteModel))

            return notes.scalars().all()

        except Exception as e:
            print(e)
            await session.rollback()
            return None

    @staticmethod
    @connection
    async def get_note(note_id: int, session: AsyncSession):
        try:
            result = await session.execute(
                select(NoteModel).where(NoteModel.id == note_id)
            )
            return result.scalars().first()

        except Exception as e:
            print(e)
            await session.rollback()
            return None

    @staticmethod
    @connection
    async def create_note(note, session: AsyncSession):
        try:
            note_db = NoteModel(content=note.content)
            session.add(note_db)
            await session.commit()
            await session.refresh(note_db)
            return note_db

        except Exception as e:
            print(e)
            await session.rollback()
            return None
