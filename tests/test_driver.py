from app.enums.driver_modes import DrivingMode
from app.enums.route_enum import Governorate

def test_update_mode_successful (client,token_driver_default) :
    r=client.put(
        "/drivers/mode",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "mode" :DrivingMode.LOCAL,
            "operating_area" : Governorate.NABLUS
        }
    )

    assert r.status_code == 200 
    assert r.json()["mode"] == DrivingMode.LOCAL
    assert r.json()["local_operating_area"] == Governorate.NABLUS

def test_update_mode_successful_2 (client,token_driver_default) :
    r=client.put(
        "/drivers/mode",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "mode" :DrivingMode.TRIP,
            "operating_area" : None
        }
    )

    assert r.status_code == 200 
    assert r.json()["mode"] == DrivingMode.TRIP
    assert r.json()["local_operating_area"] == None


def test_update_mode_same_data (client,token_driver_default) :
    r=client.put(
        "/drivers/mode",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "mode" :DrivingMode.FLEXIBLE,
            "operating_area" : Governorate.HEBRON
        }
    )

    assert r.status_code == 400 
    assert r.json()["detail"] == "your informations already like that"

def test_update_mode_area_none (client,token_driver_trip) :
    r=client.put(
        "/drivers/mode",
        headers={"Authorization" : f"Bearer {token_driver_trip}"},
        json={
            "mode" :DrivingMode.LOCAL,
            "operating_area" : None
        }
    )

    assert r.status_code == 400 
    assert r.json()["detail"] == "operating area is required for local or flexible mode"



def test_update_mode_not_driver (client,user_token) :
    r=client.put(
        "/drivers/mode",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
            "mode" :DrivingMode.LOCAL,
            "operating_area" : Governorate.NABLUS
        }
    )

    assert r.status_code == 403
    assert r.json()["detail"] == "you are not a driver"


def test_update_mode_has_trips (client,token_driver_default,active_trip) :
    r=client.put(
        "/drivers/mode",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "mode" :DrivingMode.LOCAL,
            "operating_area" : Governorate.NABLUS
        }
    )

    assert r.status_code == 409
    assert r.json()["detail"] == "you have trips planned or active"

def test_update_mode_has_orders (client,token_driver_default,accepted_order) :
    r=client.put(
        "/drivers/mode",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "mode" :DrivingMode.LOCAL,
            "operating_area" : Governorate.NABLUS
        }
    )

    assert r.status_code == 409
    assert r.json()["detail"] == "you have active orders as a driver"

def test_update_area_successful (client,token_driver_default) :
    r=client.put(
        "/drivers/area",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "area" : Governorate.NABLUS
        }
    )
    assert r.status_code == 200


def test_update_area_wrong_mode (client,token_driver_trip) :
    r=client.put(
        "/drivers/area",
        headers={"Authorization" : f"Bearer {token_driver_trip}"},
        json={
            "area" : Governorate.NABLUS
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "mode should be local or flexible to change area"

def test_update_area_no_change (client,token_driver_default) :
    r=client.put(
        "/drivers/area",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "area" : Governorate.HEBRON
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "no change"