import json
import os
import re
import time
import urllib.error
import urllib.request

BASE_URL = os.getenv("FILMLAB_BASE_URL", "http://127.0.0.1:9999").rstrip("/")

REACHABLE_CODES = {
    200, 201, 400, 401, 403, 404, 405, 409, 415, 422
}

FAKE_UUID = "00000000-0000-0000-0000-000000000000"


def request(method, path, data=None, token=None):
    url = BASE_URL + path

    headers = {"Accept": "application/json"}

    if data is not None:
        headers["Content-Type"] = "application/json"

    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(data).encode("utf-8") if data is not None else None

    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers=headers
    )

    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            return response.status, response.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return None, str(e)


def normalize_path(path):
    return re.sub(r"\{[^}]+\}", FAKE_UUID, path)


def print_result(ok, method, path, status, note=""):
    icon = "✅" if ok else "❌"
    line = f"{icon} {method:<6} {path:<55} {status}"
    if note:
        line += f"  ({note})"
    print(line)


def test_auth():
    stamp = str(int(time.time()))

    owner_username = f"api_test_owner_{stamp}"
    owner_email = f"api_test_owner_{stamp}@example.com"

    status, body = request(
        "POST",
        "/auth/register",
        {
            "username": owner_username,
            "email": owner_email,
            "password": "Test123456!",
            "full_name": "API Test Owner",
            "phone": "0900000000"
        }
    )

    print_result(
        status in {201, 409},
        "POST",
        "/auth/register",
        status,
        "201 = created, 409 = already exists"
    )

    customer_username = f"api_test_customer_{stamp}"
    customer_email = f"api_test_customer_{stamp}@example.com"

    status, body = request(
        "POST",
        "/auth/mobile-register",
        {
            "username": customer_username,
            "email": customer_email,
            "password": "Test123456!",
            "full_name": "API Test Customer",
            "phone": "0900000001",
            "role": "customer"
        }
    )

    print_result(
        status in {201, 409},
        "POST",
        "/auth/mobile-register",
        status,
        "201 = created, 409 = already exists"
    )

    status, body = request(
        "POST",
        "/auth/login",
        {
            "username": owner_username,
            "password": "Test123456!"
        }
    )

    print_result(status == 200, "POST", "/auth/login", status)

    if status != 200:
        return None

    try:
        return json.loads(body).get("token")
    except json.JSONDecodeError:
        return None


def create_test_fixtures(token):
    """
    Create only the 3 fixtures needed to safely test the endpoints
    that previously caused IntegrityError when the old script sent {}.

    Returns:
        {
            "film_lab_id": ...,
            "category_id": ...,
            "service_id": ...
        }
    """
    fixtures = {}

    stamp = str(int(time.time()))

    # Film Lab
    status, body = request(
        "POST",
        "/film-labs",
        {
            "name": f"API Test Lab {stamp}",
            "city": "Ho Chi Minh City",
            "district": "District 1",
            "address": "1 API Test Street",
            "description": "Temporary lab for API smoke test",
            "phone": "0900000010",
            "email": f"api_lab_{stamp}@example.com"
        },
        token
    )

    if status not in {200, 201}:
        print_result(
            False, "POST", "/film-labs", status,
            "Không tạo được test film lab"
        )
        print(body[:500])
        return fixtures

    try:
        data = json.loads(body)
        lab = data.get("data", data)
        fixtures["film_lab_id"] = lab.get("id")
    except Exception:
        pass

    # Service Category
    status, body = request(
        "POST",
        "/service-categories",
        {
            "name": f"API Test Category {stamp}",
            "description": "Temporary category for API smoke test"
        },
        token
    )

    if status not in {200, 201}:
        print_result(
            False, "POST", "/service-categories", status,
            "Không tạo được test service category"
        )
        print(body[:500])
        return fixtures

    try:
        data = json.loads(body)
        category = data.get("data", data)
        fixtures["category_id"] = category.get("id")
    except Exception:
        pass

    # Service
    if fixtures.get("film_lab_id") and fixtures.get("category_id"):
        status, body = request(
            "POST",
            "/services",
            {
                "film_lab_id": fixtures["film_lab_id"],
                "category_id": fixtures["category_id"],
                "name": f"API Test Service {stamp}",
                "description": "Temporary service for API smoke test",
                "price": 100000,
                "turnaround_time_min": 3,
                "turnaround_time_max": 5,
                "processing_capacity": 10,
                "supported_film_formats": ["35mm / 135"],
                "processing_options": ["C-41"],
                "scanning_quality": ["4K"],
                "printing_options": ["4×6 Print"],
                "specialized_techniques": ["Push Processing"]
            },
            token
        )

        if status in {200, 201}:
            try:
                data = json.loads(body)
                service = data.get("data", data)
                fixtures["service_id"] = service.get("id")
            except Exception:
                pass
        else:
            print_result(
                False, "POST", "/services", status,
                "Không tạo được test service"
            )
            print(body[:500])

    return fixtures


def cleanup_test_fixtures(token, fixtures):
    """
    Delete created test data in FK-safe order.
    Cleanup failures are printed but do not affect the smoke-test result.
    """
    for path, key in [
        ("/services/{id}", "service_id"),
        ("/film-labs/{id}", "film_lab_id"),
        ("/service-categories/{id}", "category_id"),
    ]:
        item_id = fixtures.get(key)
        if not item_id:
            continue

        status, body = request(
            "DELETE",
            path.replace("{id}", str(item_id)),
            token=token
        )

        if status not in {200, 204, 404}:
            print(
                f"⚠️ Cleanup {path} -> {status}: {body[:200]}"
            )


def safe_payload(method, path, fixtures):
    """
    Return a harmless payload.

    Only endpoints known from the traceback to require valid data are
    given real test data. Other POST/PUT/PATCH endpoints use {} so the
    API can return its normal validation response.
    """
    if method not in {"POST", "PUT", "PATCH"}:
        return None

    if path == "/auth/register":
        stamp = str(int(time.time() * 1000))
        return {
            "username": f"route_test_{stamp}",
            "email": f"route_test_{stamp}@example.com",
            "password": "Test123456!",
            "full_name": "Route Test Owner",
            "phone": "0900000002"
        }

    if path == "/auth/mobile-register":
        stamp = str(int(time.time() * 1000))
        return {
            "username": f"route_customer_{stamp}",
            "email": f"route_customer_{stamp}@example.com",
            "password": "Test123456!",
            "full_name": "Route Test Customer",
            "phone": "0900000003",
            "role": "customer"
        }

    if method == "POST" and path == "/film-labs":
        stamp = str(int(time.time() * 1000))
        return {
            "name": f"Route Test Lab {stamp}",
            "city": "Ho Chi Minh City",
            "district": "District 1",
            "address": "1 Route Test Street",
            "description": "Route smoke test",
            "phone": "0900000020",
            "email": f"route_lab_{stamp}@example.com"
        }

    if method == "POST" and path == "/service-categories":
        stamp = str(int(time.time() * 1000))
        return {
            "name": f"Route Test Category {stamp}",
            "description": "Route smoke test"
        }

    if method == "POST" and path == "/services":
        if fixtures.get("film_lab_id") and fixtures.get("category_id"):
            return {
                "film_lab_id": fixtures["film_lab_id"],
                "category_id": fixtures["category_id"],
                "name": "Route Test Service",
                "description": "Route smoke test",
                "price": 100000,
                "turnaround_time_min": 3,
                "turnaround_time_max": 5,
                "processing_capacity": 10,
                "supported_film_formats": ["35mm / 135"],
                "processing_options": ["C-41"],
                "scanning_quality": ["4K"],
                "printing_options": ["4×6 Print"],
                "specialized_techniques": ["Push Processing"]
            }

    return {}


def main():
    print("=" * 70)
    print("FILM LAB API - FULL QUICK TEST")
    print("=" * 70)
    print(f"Base URL : {BASE_URL}")
    print()

    # 1. Server
    status, body = request("GET", "/")

    if status is None:
        print("❌ SERVER DOWN")
        print(body)
        print()
        print("Hãy chạy: py src/app.py")
        return

    print(f"✅ SERVER ONLINE   GET /   -> {status}")
    print()

    # 2. Swagger
    status, body = request("GET", "/swagger.json")

    if status != 200:
        print(f"❌ Swagger JSON -> {status}")
        print(body[:500])
        return

    try:
        swagger = json.loads(body)
    except json.JSONDecodeError:
        print("❌ /swagger.json không trả về JSON hợp lệ.")
        return

    paths = swagger.get("paths", {})

    if not paths:
        print("❌ Swagger không có endpoint nào.")
        return

    print(f"Found {len(paths)} API paths")
    print()

    # 3. Authentication
    print("=" * 70)
    print("AUTHENTICATION TEST")
    print("=" * 70)

    token = test_auth()

    if not token:
        print()
        print("❌ Không lấy được JWT.")
        print("Dừng test authenticated APIs.")
        return

    print("✅ JWT obtained successfully")
    print()

    # 4. Create safe fixtures
    print("=" * 70)
    print("CREATE SAFE TEST FIXTURES")
    print("=" * 70)

    fixtures = create_test_fixtures(token)

    print()
    print(f"Film Lab ID       : {fixtures.get('film_lab_id', '-')}")
    print(f"Category ID       : {fixtures.get('category_id', '-')}")
    print(f"Service ID        : {fixtures.get('service_id', '-')}")
    print()

    # 5. All API routes
    print("=" * 70)
    print("ALL API ROUTES")
    print("=" * 70)

    passed = 0
    failed = 0
    results = []

    for path, path_item in paths.items():
        if path == "/swagger.json":
            continue

        real_path = normalize_path(path)

        for method in path_item.keys():
            method_upper = method.upper()

            if method_upper not in {
                "GET", "POST", "PUT", "PATCH", "DELETE"
            }:
                continue

            data = safe_payload(method_upper, path, fixtures)

            status, body = request(
                method_upper,
                real_path,
                data=data,
                token=token
            )

            if status is None:
                failed += 1
                results.append(
                    ("FAIL", method_upper, path, "-", body[:200])
                )
                continue

            if status in REACHABLE_CODES:
                passed += 1
                results.append(
                    ("PASS", method_upper, path, status, "")
                )
            else:
                failed += 1
                results.append(
                    ("FAIL", method_upper, path, status, body[:200])
                )

    print()

    for result, method, path, status, detail in results:
        icon = "✅" if result == "PASS" else "❌"
        print(f"{icon} {method:<6} {path:<55} {status}")

        if result == "FAIL" and detail:
            print(f"       {detail}")

    print("-" * 70)
    print()
    print("SUMMARY")
    print(f"API paths                  : {len(paths)}")
    print(f"Operations checked         : {len(results)}")
    print(f"Passed / reachable         : {passed}")
    print(f"Failed / unexpected        : {failed}")
    print()

    # Cleanup
    print("=" * 70)
    print("CLEANUP")
    print("=" * 70)
    cleanup_test_fixtures(token, fixtures)
    print("✅ Test fixtures cleanup finished.")
    print()

    if failed == 0:
        print("🎉 ALL API ROUTES PASSED THE QUICK TEST.")
    else:
        print("⚠️ Có API cần kiểm tra thêm.")

    print()
    print("NOTE:")
    print("- Test không tạo order/payment/transaction thật.")
    print("- Film Lab / Service Category / Service dùng dữ liệu test hợp lệ.")
    print("- Các endpoint còn lại chỉ smoke-test route + JWT + validation.")
    print("- GET/DELETE endpoint có ID dùng UUID giả.")


if __name__ == "__main__":
    main()
