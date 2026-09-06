from app.models.driver_assignment import DriverAssignment
from app.enums.assignment import AssignmentStatus
from app.enums.order import OrderStatus


def test_get_assignments_successful (client,token_driver_default,pending_order_local_2) :
    r=client.get(
        "/my/assignments",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    assert r.status_code == 200
    assert r.json() != []

def test_accept_assignment_successful (db_session,client,token_driver_default,pending_order_local_2) :
    r=client.put(
        "/assignmnts/1/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    assignment = db_session.query(DriverAssignment).filter(DriverAssignment.id == 1).first()
    assert r.status_code == 200
    assert "id" in r.json()
    assert assignment.status == AssignmentStatus.TAKEN


def test_accept_assignment_not_found (client,token_driver_default,pending_order_local_2) :
    r=client.put(
        "/assignmnts/110/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "assignment not found"

def test_accept_assignment_not_yours (client,token_driver_default,pending_order_local) :
    r=client.put(
        "/assignmnts/1/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "assignment not found"



def test_accept_assignment_not_pending (client,token_driver_default,pending_order_local_2) :
    r=client.put(
        "/assignmnts/1/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    #Taken now
    r=client.put(
        "/assignmnts/1/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "assignment not found"


def test_accept_assignment_successful (db_session,client,token_driver_default,pending_order_local_2,pending_order_local_3,
                                       pending_order_local_4,pending_order_local_5,pending_order_local_6,pending_order_local_7) :
    client.put(
        "/assignmnts/1/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    client.put(
        "/assignmnts/2/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    client.put(
        "/assignmnts/3/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    client.put(
        "/assignmnts/4/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    client.put(
        "/assignmnts/5/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
    r = client.put(
        "/assignmnts/6/accept",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )

    assert r.status_code == 409
    assert r.json()["detail"] == "you can not have more than 5 active orders at the same time"