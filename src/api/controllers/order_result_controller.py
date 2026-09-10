from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from flask import Blueprint, jsonify, send_file, request

from api.middleware import token_required, role_required
from services.order_result_service import OrderResultService


order_result_bp = Blueprint(
    "order_result",
    __name__,
    url_prefix="/order-results"
)


service = OrderResultService()


def serialize_scan(scan):
    return {
        "id": str(scan.id),
        "order_id": str(scan.order_id),
        "customer_id": str(scan.customer_id),
        "file_name": scan.file_name,
        "storage_path": scan.storage_path,
        "file_size": scan.file_size,
        "uploaded_at": (
            scan.uploaded_at.isoformat()
            if scan.uploaded_at
            else None
        ),
    }


# =========================================================
# OWNER UPLOAD ORDER RESULT
# =========================================================

@order_result_bp.route(
    "/<uuid:order_id>/upload",
    methods=["POST"]
)
@token_required
@role_required("film_lab_owner", "admin")
def upload_order_result(order_id):

    user_id = request.user["user_id"]
    role = request.user["role"]

    files = request.files.getlist("files")

    # Cho phép frontend gửi bằng key "images"
    if not files:
        files = request.files.getlist("images")

    if not files:
        return jsonify({
            "message": "At least one image file is required"
        }), 400

    try:

        scans, error = service.upload(
            order_id=order_id,
            user_id=user_id,
            role=role,
            files=files
        )

        if error == "not_found":
            return jsonify({
                "message": "Order not found"
            }), 404

        if error == "forbidden":
            return jsonify({
                "message": (
                    "You do not have permission "
                    "to access this order"
                )
            }), 403

        if error == "invalid_status":
            return jsonify({
                "message": (
                    "Order result can only be uploaded "
                    "when order status is COMPLETED"
                )
            }), 400

        if error == "no_files":
            return jsonify({
                "message": "No valid image files were uploaded"
            }), 400

        return jsonify({
            "message": "Order result uploaded successfully",
            "order_id": str(order_id),
            "files": [
                serialize_scan(scan)
                for scan in scans
            ]
        }), 201

    except Exception as exc:

        return jsonify({
            "message": "Failed to upload order result",
            "error": str(exc)
        }), 500


# =========================================================
# GET ORDER RESULT
# =========================================================

@order_result_bp.route(
    "/<uuid:order_id>",
    methods=["GET"]
)
@token_required
@role_required(
    "customer",
    "film_lab_owner",
    "admin"
)
def get_order_result(order_id):

    user_id = request.user["user_id"]
    role = request.user["role"]

    try:

        result, error = service.list_for_user(
            order_id=order_id,
            user_id=user_id,
            role=role
        )

        if error == "not_found":
            return jsonify({
                "message": "Order not found"
            }), 404

        if error == "forbidden":
            return jsonify({
                "message": (
                    "You do not have permission "
                    "to access this order"
                )
            }), 403

        if error == "not_available":
            return jsonify({
                "message": (
                    "Order result is available to customer "
                    "only when order status is DONE"
                )
            }), 403

        if error:
            return jsonify({
                "message": error
            }), 400

        return jsonify({
            "order_id": result["order_id"],
            "order_status": result["order_status"],
            "has_result": result["has_result"],
            "files": [
                serialize_scan(scan)
                for scan in result["files"]
            ]
        }), 200

    except Exception as exc:

        return jsonify({
            "message": "Failed to get order result",
            "error": str(exc)
        }), 500


# =========================================================
# VIEW / DOWNLOAD SINGLE RESULT FILE
# =========================================================

@order_result_bp.route(
    "/<uuid:order_id>/files/<uuid:scan_id>",
    methods=["GET"]
)
@token_required
@role_required(
    "customer",
    "film_lab_owner",
    "admin"
)
def get_order_result_file(order_id, scan_id):

    user_id = request.user["user_id"]
    role = request.user["role"]

    try:

        result, error = service.get_file_for_user(
            order_id=order_id,
            scan_id=scan_id,
            user_id=user_id,
            role=role
        )

        if error == "not_found":
            return jsonify({
                "message": "Result file not found"
            }), 404

        if error == "not_available":
            return jsonify({
                "message": (
                    "Order result is not available yet"
                )
            }), 403

        if error == "invalid_path":
            return jsonify({
                "message": "Invalid result file path"
            }), 400

        if error == "file_not_found":
            return jsonify({
                "message": "Stored result file not found"
            }), 404

        if error:
            return jsonify({
                "message": error
            }), 400

        scan = result["scan"]
        file_path = result["file_path"]

        return send_file(
            file_path,
            as_attachment=False,
            download_name=scan.file_name
        )

    except Exception as exc:

        return jsonify({
            "message": "Failed to open result file",
            "error": str(exc)
        }), 500


# =========================================================
# DOWNLOAD ALL RESULT FILES AS ZIP
# =========================================================

@order_result_bp.route(
    "/<uuid:order_id>/download",
    methods=["GET"]
)
@token_required
@role_required(
    "customer",
    "film_lab_owner",
    "admin"
)
def download_order_result(order_id):

    user_id = request.user["user_id"]
    role = request.user["role"]

    try:

        result, error = service.get_download_files(
            order_id=order_id,
            user_id=user_id,
            role=role
        )

        if error == "not_found":
            return jsonify({
                "message": "Order not found"
            }), 404

        if error == "not_available":
            return jsonify({
                "message": (
                    "Order result is not available yet"
                )
            }), 403

        if error == "no_result":
            return jsonify({
                "message": (
                    "This order does not have "
                    "any result files"
                )
            }), 404

        if error:
            return jsonify({
                "message": error
            }), 400

        order = result["order"]
        files = result["files"]

        zip_buffer = BytesIO()

        added_names = set()

        with ZipFile(
            zip_buffer,
            mode="w",
            compression=ZIP_DEFLATED
        ) as zip_file:

            for item in files:

                file_path = item["file_path"]
                file_name = Path(
                    item["file_name"]
                ).name

                if not file_name:
                    continue

                zip_name = file_name
                counter = 1

                while zip_name in added_names:

                    stem = Path(
                        file_name
                    ).stem

                    suffix = Path(
                        file_name
                    ).suffix

                    zip_name = (
                        f"{stem}_{counter}{suffix}"
                    )

                    counter += 1

                added_names.add(zip_name)

                zip_file.write(
                    file_path,
                    arcname=zip_name
                )

        zip_buffer.seek(0)

        if not added_names:
            return jsonify({
                "message": (
                    "No valid result files were found"
                )
            }), 404

        return send_file(
            zip_buffer,
            mimetype="application/zip",
            as_attachment=True,
            download_name=(
                f"order_{order.id}_results.zip"
            )
        )

    except Exception as exc:

        return jsonify({
            "message": "Failed to create result ZIP",
            "error": str(exc)
        }), 500