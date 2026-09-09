import uuid
from pathlib import Path

from services.file_validation_service import FileValidationService


# src/
BASE_DIR = Path(__file__).resolve().parent.parent

# src/storage/
STORAGE_DIR = BASE_DIR / "storage"


class StorageService:

    @staticmethod
    def save_file(file, folder):
        """
        Save an uploaded image into storage.
        """

        # Validate image before saving
        FileValidationService.validate_image(file)

        folder_path = STORAGE_DIR / folder
        folder_path.mkdir(
            parents=True,
            exist_ok=True
        )

        extension = Path(
            file.filename
        ).suffix.lower()

        file_name = f"{uuid.uuid4()}{extension}"

        file_path = folder_path / file_name

        file.save(file_path)

        return str(
            Path(folder) / file_name
        ).replace("\\", "/")

    @staticmethod
    def delete_file(storage_path):
        """
        Delete a stored image.
        """

        if not storage_path:
            return

        file_path = STORAGE_DIR / storage_path

        if (
            file_path.exists()
            and file_path.is_file()
        ):
            file_path.unlink()

    @staticmethod
    def replace_file(
        file,
        old_storage_path,
        folder
    ):
        """
        Replace an existing image.

        The old image is deleted after
        the new image is successfully saved.
        """

        new_storage_path = StorageService.save_file(
            file,
            folder
        )

        if old_storage_path:
            StorageService.delete_file(
                old_storage_path
            )

        return new_storage_path