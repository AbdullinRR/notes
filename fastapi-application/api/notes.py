from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from core.schemas.notes import NoteUpdate, NoteOut, NoteCreate
from services.notes import NoteService

router = APIRouter(prefix="/notes", tags=["Notes"])

NoteId = Annotated[int, Path(ge=1)]


@router.get("/", response_model=list[NoteOut])
async def get_notes():
    """
    Вернуть список заметок.
    """
    notes = await NoteService.get_notes()
    return notes


@router.get("/{note_id}", response_model=NoteOut)
async def get_note(note_id: int):
    note = await NoteService.get_note(note_id)

    return note


@router.post("/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate):
    """
    Создать заметку.
    """
    note_db = await NoteService.create_note(note)
    return note_db


@router.patch("/{note_id}", response_model=NoteOut)
async def update_note(note_id: NoteId, note: NoteUpdate):
    """
    Частично обновить заметку.
    """
    note = await NoteService.update_note(note_id, note)
    return note


@router.delete("/{note_id}")
async def delete_note(note_id: NoteId):
    """
    Удалить заметку.
    """
    note = await NoteService.delete_note(note_id)
    message = "note successfully deleted" if note else "failed to delete entry note"
    return {
        "message": message
    }
