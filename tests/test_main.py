from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

receipts = [
    {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
            {
                "shortDescription": "Gatorade",
                "price": "2.25"
            },
            {
                "shortDescription": "Gatorade",
                "price": "2.25"
            },
            {
                "shortDescription": "Gatorade",
                "price": "2.25"
            },
            {
                "shortDescription": "Gatorade",
                "price": "2.25"
            }
        ],
        "total": "9.00"
    },
    {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
                "shortDescription": "Mountain Dew 12PK",
                "price": "6.49"
            },
            {
                "shortDescription": "Emils Cheese Pizza",
                "price": "12.25"
            },
            {
                "shortDescription": "Knorr Creamy Chicken",
                "price": "1.26"
            },
            {
                "shortDescription": "Doritos Nacho Cheese",
                "price": "3.35"
            },
            {
                "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                "price": "12.00"
            }
        ],
        "total": "35.35"
    },
    {
        "retailer": "",
        "purchaseDate": "2023-10-02",
        "purchaseTime": "10:30",
        "total": "0.01",
        "items": []
    },
]

invalid_receipts = [
    {
        "purchaseDate": "2023-10-01",
        "purchaseTime": "15:30",
        "total": "20.00",
        "items": []
    },
    {
        "retailer": "RETAILER",
        "purchaseDate": "INVALID DATE",
        "purchaseTime": "INVALID TIME",
        "total": "INVALID TOTAL",
        "items": []
    },
    {
        "retailer": "Target",
        "purchaseDate": "2023-10-01",
        "purchaseTime": "15:30",
        "total": "20.00",
        "items": [
            {"invalidKey": "INVALID ITEM"}
        ]
    },
    {
        "retailer": "Target",
        "purchaseDate": "2023-10-01",
        "purchaseTime": "15:30",
        "total": "20.00",
        "items": [
            {"shortDescription": "INVALID ITEM", "price": "-5.00"}
        ]
    },
]

# Test endpoints
def test_process_and_get_receipt():
    ids = []

    for receipt in receipts:
        response = client.post("/receipts/process", json=receipt)
        content = response.json()

        assert response.status_code == 200
        assert "id" in content
        ids.append(content["id"])

    response = client.get(f"/receipts/{ids[0]}/points")
    content = response.json()

    assert response.status_code == 200
    assert "points" in content
    assert content["points"] == 109

    response = client.get(f"/receipts/{ids[1]}/points")
    content = response.json()

    assert response.status_code == 200
    assert "points" in content
    assert content["points"] == 28

    response = client.get(f"/receipts/{ids[2]}/points")
    content = response.json()

    assert response.status_code == 200
    assert "points" in content
    assert content["points"] == 0

    print("test_process_and_get_receipt passed")


# Test POST with invalid data
def test_process_invalid_receipt():
    for receipt in invalid_receipts:
        response = client.post("/receipts/process", json=receipt)
        content = response.json()

        assert response.status_code == 422

    print("test_process_invalid_receipt passed")


# Test GET with invalid ID
def test_get_invalid_receipt():
    response = client.get("/receipts/INVALID/points")
    content = response.json()

    assert response.status_code == 422

    print("test_get_invalid_receipt passed")


test_process_and_get_receipt()
test_process_invalid_receipt()
test_get_invalid_receipt()
