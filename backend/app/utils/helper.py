from pathlib import Path
from fastapi import UploadFile
import shutil

from app.core.config import REPORTS_DIR


def save_file(
    owner_id: int, input_file: UploadFile, filename_to_save: str
) -> bool | str | None:
    try:
        dir: Path = REPORTS_DIR / str(owner_id)
        dir.mkdir(parents=True, exist_ok=True)

        save_dir: Path = dir / filename_to_save

        input_file.file.seek(0)

        with save_dir.open("wb") as file:
            shutil.copyfileobj(input_file.file, file)

        return True
    except Exception:
        return False
