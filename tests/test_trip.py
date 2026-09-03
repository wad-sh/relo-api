from app.enums.route_enum import Governorate
from app.enums.trip import TripStatus

def test_create_trip_successful (client,token_driver_default) :
    r= client.post(
        "/trips",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "route_from" : Governorate.NABLUS,
            "route_to" : Governorate.JENIN
        }
    )
    assert r.status_code == 200
    assert "id" in r.json()

def test_create_trip_wrong_mode (client,token_driver_local) :
    r= client.post(
        "/trips",
        headers={"Authorization" : f"Bearer {token_driver_local}"},
        json={
            "route_from" : Governorate.NABLUS,
            "route_to" : Governorate.JENIN
        })

    assert r.status_code == 400
    assert r.json()["detail"] == "mode should be trip or flexible"

def test_create_trip_has_trips (client,active_trip,token_driver_default) :
    r= client.post(
        "/trips",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "route_from" : Governorate.NABLUS,
            "route_to" : Governorate.JENIN
        }
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "you have planned or active trips"

def test_create_trip_has_orders (client,accepted_order,token_driver_default) :
    r= client.post(
        "/trips",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "route_from" : Governorate.NABLUS,
            "route_to" : Governorate.JENIN
        }
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "you have accepted or in transit orders"


def test_create_trip_same_city (client,token_driver_default) :
    r= client.post(
        "/trips",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "route_from" : Governorate.JENIN,
            "route_to" : Governorate.JENIN
        }
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "invalid route"


def test_get_all_planned_trips (client,active_trip,driver_default) :
    r= client.get (
        "/trips/all",
        params={
            "route_from" : Governorate.SALFIT.value,
            "route_to" : Governorate.RAMALLAH_AND_AL_BIREH.value
        }
        
    )

    assert r.status_code == 200

def test_get_my_trips_successful (client,token_driver_default,active_trip):
    r= client.get(
        "/trips/driver",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    assert r.status_code == 200

def test_update_route_successful (client,token_driver_default,active_trip) :
    r=client.put (
        f"/trips/{active_trip}/route",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "route_from" : Governorate.NABLUS,
            "route_to" : Governorate.JENIN
        }
    )
    assert r.status_code == 200
    assert r.json()["route_from"] == Governorate.NABLUS
    assert r.json()["route_to"] == Governorate.JENIN


def test_update_route_not_found (client,token_driver_default) :
    r=client.put (
        "/trips/10/route",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "route_from" : Governorate.NABLUS,
            "route_to" : Governorate.JENIN
        }
    )

    assert r.status_code == 404
    assert r.json()["detail"] == "unable to find trip"

def test_update_route_not_planned (client,token_driver_default,completed_trip) :
    r=client.put (
        f"/trips/{completed_trip}/route",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "route_from" : Governorate.NABLUS,
            "route_to" : Governorate.JENIN
        }
    )

    assert r.status_code == 409
    assert r.json()["detail"] == "only planned trips can be edited"


def test_update_route_same_route (client,token_driver_default,active_trip) :
    r=client.put (
        f"/trips/{active_trip}/route",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "route_from" : Governorate.TULKARM,
            "route_to" : Governorate.QALQILYA
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "no change"

def test_update_status_successful (client,token_driver_default,active_trip) :
    r = client.put(
        f"/trips/{active_trip}/status",
        headers={"Authorization" : f"Bearer {token_driver_default}"}

    )

    assert r.status_code == 200
    assert r.json()["status"] == TripStatus.ACTIVE

def test_update_status_wrong_status (client,token_driver_default,completed_trip) :
    r = client.put(
        f"/trips/{completed_trip}/status",
        headers={"Authorization" : f"Bearer {token_driver_default}"}

    )

    assert r.status_code == 400
    assert r.json()["detail"] == "only liner change for trips status"

def test_update_status_admin_trip_successful (client,admin_token,active_trip):
    r=client.put(
        f"/trips/{active_trip}/status/admin",
        headers={"Authorization" : f"Bearer {admin_token}"},
        json={
            "status" : TripStatus.ERORR
        })
    assert  r.status_code == 200
    assert r.json()["status"] == TripStatus.ERORR

def test_update_status_admin_trip_not_admin (client,user_token,active_trip):
    r=client.put(
        f"/trips/{active_trip}/status/admin",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
            "status" :TripStatus.ERORR
        })
    assert  r.status_code == 403
    assert r.json()["detail"] == "you are not an admin"

def test_update_status_admin_trip_not_found (client,admin_token):
    r=client.put(
        "/trips/10/status/admin",
        headers={"Authorization" : f"Bearer {admin_token}"},
        json={
            "status" : TripStatus.COMPLETED
        })
    assert  r.status_code == 404
    assert r.json()["detail"] == "trip not found"

def test_delete_trip_successful (client,active_trip,token_driver_default):
    r=client.delete(
        f"/trips/{active_trip}",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    assert r.status_code == 200
    assert "message" in r.json()

def test_delete_trip_with_orders (client,active_trip,token_driver_default,order_in_trip):
    r=client.delete(
        f"/trips/{active_trip}",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "there is orders related to this trip make them avilable first"

