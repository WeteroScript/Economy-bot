import re
import tempfile
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

router = Router(name="file_creator")
EXTENSION_RE = re.compile(r"^[A-Za-z0-9]{1,10}$")


@router.message(Command("create"))
async def start_creation(message: Message) -> None:
    await message.answer(
        "Введите расширение текстового файла без точки, например txt, md, csv или py."
    )


@router.message(F.text)
async def create_file(message: Message) -> None:
    extension = (message.text or "").strip().lstrip(".")
    if not EXTENSION_RE.fullmatch(extension):
        return

    filename = f"created_file.{extension.lower()}"
    content = (
        f"Файл {filename} создан ботом по вашему запросу.\n"
        "Замените этот текст нужным содержимым.\n"
    )

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            suffix=f".{extension.lower()}",
            delete=False,
        ) as file:
            file.write(content)
            temp_path = Path(file.name)

        await message.answer_document(
            document=FSInputFile(temp_path, filename=filename),
            caption=f"Готово: {filename}",
        )
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)