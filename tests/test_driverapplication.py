from app.enums.application import VehicleType
from app.enums.route_enum import Governorate
from app.enums.user_enum import UserEnum

def test_create_application_successful (client,user_token):
    r=client.post(
        "/applications",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
            "vehicle_type" : VehicleType.TRUCK,
            "vehicle_model" : "XX",
            "vehicle_year" : 1999,
            "vehicle_capacity_kg" : 500,
            "preferred_area" : Governorate.JERUSALEM,
            "preferred_route_from" :None,
            "preferred_route_to" :None,
            "description" :None
        }
    )

    assert r.status_code == 200
    assert "id" in r.json()

def test_create_application_not_customer (client,token_driver_default):
    r=client.post(
        "/applications",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "vehicle_type" : VehicleType.TRUCK,
            "vehicle_model" : "XX",
            "vehicle_year" : 1999,
            "vehicle_capacity_kg" : 500,
            "preferred_area" : Governorate.JERUSALEM,
            "preferred_route_from" :None,
            "preferred_route_to" :None,
            "description" :None
        }
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "admins and drivers can't apply"

def test_create_application_has_apps (client,user_token,app_):
    r=client.post(
        "/applications",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
            "vehicle_type" : VehicleType.TRUCK,
            "vehicle_model" : "XX",
            "vehicle_year" : 1999,
            "vehicle_capacity_kg" : 500,
            "preferred_area" : Governorate.JERUSALEM,
            "preferred_route_from" :None,
            "preferred_route_to" :None,
            "description" :None
        }
    )

    assert r.status_code == 409
    assert r.json()["detail"] == "you already have a pending application wait for the response"

def test_get_all_applications_admin_successful (client,admin_token,app_) :
    r=client.get(
        "/applications/all/admin",
        headers={"Authorization" : f"Bearer {admin_token}"}
    )
    assert r.status_code ==200
    assert r.json() != []

def test_accept_application_admin_successful (client,admin_token,app_,user) :
    r=client.put(
        f"/applications/1/accept",
        headers={"Authorization" : f"Bearer {admin_token}"}
    )

    assert r.status_code == 200
    assert user.role == UserEnum.Driver


def test_accept_application_admin_not_found (client,admin_token,app_,user) :
    client.put(
        f"/applications/1/accept",
        headers={"Authorization" : f"Bearer {admin_token}"}
    )

    r=client.put(
        f"/applications/1/accept",
        headers={"Authorization" : f"Bearer {admin_token}"}
    )

    assert r.status_code == 404
    assert r.json()["detail"] == "Application is not found or has already been reviewed"

def test_reject_application_admin_successful (client,admin_token,app_,user) :
    r=client.put(
        f"/applications/1/reject",
        headers={"Authorization" : f"Bearer {admin_token}"}
    )

    assert r.status_code == 200
    assert user.role == UserEnum.Customer

def test_get_my_applications_successful (client,user_token,app_):
    r=client.get(
        "/applications/me",
        headers={"Authorization" : f"Bearer {user_token}"}
    )

    assert r.status_code == 200
    assert r.json() !=[]

def test_get_my_applications_no_token (client,user_token,app_):
    r=client.get(
        "/applications/me"
    )

    assert r.status_code == 401
