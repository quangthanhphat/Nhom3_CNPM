import uuid
from pathlib import Path

from services.file_validation_service import FileValidationService


BASE_DIR = Path(__file__).resolve().parent.parent

STORAGE_DIR = BASE_DIR / "storage"


class StorageService:

    # Cho phép các service khác sử dụng:
    # StorageService.STORAGE_DIR
    STORAGE_DIR = STORAGE_DIR

    @staticmethod
    def save_file(file, folder):
        FileValidationService.validate_image(file)

        folder_path = StorageService.STORAGE_DIR / folder
        folder_path.mkdir(
            parents=True,
            exist_ok=True
        )

        extension = Path(
            file.filename
        ).suffix.lower()

        file_name = f"{uuid.uuid4()}{extension}"

        file_path = (
            folder_path / file_name
        )

        file.save(file_path)

        return str(
            Path(folder) / file_name
        ).replace("\\", "/")

    @staticmethod
    def delete_file(storage_path):
        if not storage_path:
            return False

        storage_root = (
            StorageService.STORAGE_DIR
            .resolve()
        )

        file_path = (
            storage_root / storage_path
        ).resolve()

        # Không cho phép path thoát khỏi storage/
        try:
            file_path.relative_to(
                storage_root
            )
        except ValueError:
            return False

        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            return True

        return False

    @staticmethod
    def replace_file(
        file,
        old_storage_path,
        folder
    ):
        new_storage_path = (
            StorageService.save_file(
                file,
                folder
            )
        )

        if old_storage_path:
            try:
                StorageService.delete_file(
                    old_storage_path
                )
            except Exception:
                pass

        return new_storage_path