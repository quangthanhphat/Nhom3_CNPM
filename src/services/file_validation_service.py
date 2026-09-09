from pathlib import Path


ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB


class FileValidationService:

    @staticmethod
    def validate_image(file):
        if not file:
            raise ValueError("No file provided")

        if not file.filename:
            raise ValueError("Invalid file name")

        extension = Path(
            file.filename
        ).suffix.lower()

        if extension not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError(
                "Only JPG, JPEG, PNG and WEBP images are allowed"
            )

        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_IMAGE_SIZE:
            raise ValueError(
                "Image size must not exceed 10 MB"
            )

        return True