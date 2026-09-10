from pathlib import Path

from infrastructure.models.digital_scan_model import DigitalScanModel
from infrastructure.repositories.digital_scan_repository import (
    DigitalScanRepository
)
from services.order_service import OrderService
from services.storage_service import StorageService


class OrderResultService:

    def __init__(self):
        self.scan_repository = DigitalScanRepository()
        self.order_service = OrderService()

    # =========================================================
    # Helpers
    # =========================================================

    def _get_order(self, order_id, user_id, role):
        order, error = self.order_service.get_by_id_for_user(
            order_id,
            user_id,
            role
        )

        if error:
            return None, error

        if not order:
            return None, "not_found"

        return order, None

    def _get_order_scans(self, order_id):
        scans = self.scan_repository.list_all()

        return [
            scan
            for scan in scans
            if str(scan.order_id) == str(order_id)
        ]

    def _get_file_path(self, storage_path):
        if not storage_path:
            return None

        storage_root = Path(
            StorageService.STORAGE_DIR
        ).resolve()

        file_path = (
            storage_root / storage_path
        ).resolve()

        # Không cho phép path thoát khỏi storage/
        try:
            file_path.relative_to(storage_root)
        except ValueError:
            return None

        return file_path

    # =========================================================
    # Upload Result
    # =========================================================

    def upload(
        self,
        order_id,
        user_id,
        role,
        files
    ):
        """
        Owner/Admin upload nhiều ảnh kết quả.

        Chỉ upload khi order = COMPLETED.
        Upload không thay đổi trạng thái order.
        """

        order, error = self._get_order(
            order_id,
            user_id,
            role
        )

        if error:
            return None, error

        if order.status != "completed":
            return None, "invalid_status"

        valid_files = [
            file
            for file in files
            if file and file.filename
        ]

        if not valid_files:
            return None, "no_files"

        created_scans = []
        saved_paths = []

        try:

            result_folder = (
                f"order_results/{order_id}"
            )

            for file in valid_files:

                original_name = Path(
                    file.filename
                ).name

                if not original_name:
                    continue

                storage_path = StorageService.save_file(
                    file,
                    folder=result_folder
                )

                saved_paths.append(storage_path)

                file_path = self._get_file_path(
                    storage_path
                )

                file_size = None

                if file_path and file_path.exists():
                    file_size = file_path.stat().st_size

                scan = DigitalScanModel(
                    order_id=order.id,
                    customer_id=order.customer_id,
                    file_name=original_name,
                    storage_path=storage_path,
                    file_size=file_size
                )

                created_scan = (
                    self.scan_repository.create(scan)
                )

                created_scans.append(
                    created_scan
                )

            if not created_scans:
                return None, "no_files"

            return created_scans, None

        except Exception:

            # Nếu upload lỗi giữa chừng,
            # xóa những file đã lưu.
            for storage_path in saved_paths:
                try:
                    StorageService.delete_file(
                        storage_path
                    )
                except Exception:
                    pass

            raise

    # =========================================================
    # List Result
    # =========================================================

    def list_for_user(
        self,
        order_id,
        user_id,
        role
    ):
        """
        Lấy danh sách result files.

        Customer:
            chỉ xem khi DONE.

        Owner/Admin:
            có thể xem trước DONE.
        """

        order, error = self._get_order(
            order_id,
            user_id,
            role
        )

        if error:
            return None, error

        if (
            role == "customer"
            and order.status != "done"
        ):
            return None, "not_available"

        scans = self._get_order_scans(
            order.id
        )

        return {
            "order_id": str(order.id),
            "order_status": order.status,
            "has_result": len(scans) > 0,
            "files": scans
        }, None

    # =========================================================
    # Get Single File
    # =========================================================

    def get_file_for_user(
        self,
        order_id,
        scan_id,
        user_id,
        role
    ):
        """
        Lấy một result file cụ thể.
        """

        order, error = self._get_order(
            order_id,
            user_id,
            role
        )

        if error:
            return None, error

        if (
            role == "customer"
            and order.status != "done"
        ):
            return None, "not_available"

        scan = self.scan_repository.find_by_id(
            scan_id
        )

        if not scan:
            return None, "not_found"

        if str(scan.order_id) != str(order.id):
            return None, "not_found"

        file_path = self._get_file_path(
            scan.storage_path
        )

        if not file_path:
            return None, "invalid_path"

        if not file_path.exists():
            return None, "file_not_found"

        return {
            "scan": scan,
            "file_path": file_path
        }, None

    # =========================================================
    # ZIP Result
    # =========================================================

    def get_download_files(
        self,
        order_id,
        user_id,
        role
    ):
        """
        Lấy các file hợp lệ để tạo ZIP.
        """

        order, error = self._get_order(
            order_id,
            user_id,
            role
        )

        if error:
            return None, error

        if (
            role == "customer"
            and order.status != "done"
        ):
            return None, "not_available"

        scans = self._get_order_scans(
            order.id
        )

        if not scans:
            return None, "no_result"

        files = []

        for scan in scans:

            file_path = self._get_file_path(
                scan.storage_path
            )

            if not file_path:
                continue

            if not file_path.exists():
                continue

            file_name = Path(
                scan.file_name or ""
            ).name

            if not file_name:
                continue

            files.append({
                "scan": scan,
                "file_path": file_path,
                "file_name": file_name
            })

        if not files:
            return None, "no_result"

        return {
            "order": order,
            "files": files
        }, None