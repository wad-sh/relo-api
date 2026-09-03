from app.enums.order import OrderType,OrderStatus
from app.enums.route_enum import Governorate
from app.models.order import Order
from app.models.history_order import HistoryOrder
from app.models.driver_assignment import DriverAssignment
from app.enums.assignment import AssignmentStatus

def test_create_order_local_successful (client, user_token,db_session,driver_default) :
    r=client.post(
        "/orders",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type" : OrderType.LOCAL,
    "operating_area" : Governorate.JERUSALEM,
    "address_receive":"from",
    "address_delivery": "to",
    "description": "keys",
        }
    )
    assignments = db_session.query(DriverAssignment).filter(DriverAssignment.order_id == r.json()["id"]).all()
    assert r.status_code == 200
    assert "type" in r.json()
    assert assignments is not None

def test_create_order_route_successful (client, user_token) :
    r=client.post(
        "/orders",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type" : OrderType.ROUTE,
    "route_from" : Governorate.JERUSALEM,
    "route_to" : Governorate.TULKARM,
    "address_receive":"there",
    "address_delivery": "to",
    "description": " 500g",
        }
    )
    assert r.status_code == 200
    assert "id" in r.json()

def test_create_order_local_no_area (client, user_token) :
    r=client.post(
        "/orders",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type" : OrderType.LOCAL,
    "operating_area" : None,
    "address_receive":"from",
    "address_delivery": "to",
    "description": "keys",
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "add operating area for local orders"

def test_create_order_route_no_route (client, user_token) :
    r=client.post(
        "/orders",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type" : OrderType.ROUTE,
    "route_from" : None,
    "route_to" : None,
    "address_receive":"there",
    "address_delivery": "to",
    "description": " 500g",
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "add full route for the order"

def test_create_order_route_same_from_to (client, user_token) :
    r=client.post(
        "/orders",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type" : OrderType.ROUTE,
    "route_from" : Governorate.JERUSALEM,
    "route_to" : Governorate.JERUSALEM,
    "address_receive":"there",
    "address_delivery": "to",
    "description": " 500g",
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "invalid route"

def test_order_update_successful (client,user_token,pending_order_local):
    r=client.put(
        f"/orders/{pending_order_local}",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type": OrderType.ROUTE,
    "operating_area" : None,
    "route_from": Governorate.NABLUS,
    "route_to": Governorate.SALFIT,
    "address_receive": "mid",
    "address_delivery":"mid",
    "description": "10 kg door",
        }
    )
    assert r.status_code == 200
    assert r.json()["type"] == OrderType.ROUTE

def test_order_update_not_yours (client,admin_token,pending_order_local):
    r=client.put(
        f"/orders/{pending_order_local}",
        headers={"Authorization" : f"Bearer {admin_token}"},
        json={
    "type": OrderType.ROUTE,
    "operating_area" : None,
    "route_from": Governorate.NABLUS,
    "route_to": Governorate.SALFIT,
    "address_receive": "mid",
    "address_delivery":"mid",
    "description": "10 kg door",
        }
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "order not found"

def test_order_update_accepted (client,user_token,accepted_order):
    r=client.put(
        f"/orders/{accepted_order}",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type": OrderType.ROUTE,
    "operating_area" : None,
    "route_from": Governorate.NABLUS,
    "route_to": Governorate.SALFIT,
    "address_receive": "mid",
    "address_delivery":"mid",
    "description": "10 kg door",
        }
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "order is not avilable for edit"

def test_order_update_no_change (client,user_token,pending_order_local):
    r=client.put(
        f"/orders/{pending_order_local}",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type": None,
    "operating_area" : None,
    "route_from": None,
    "route_to": None,
    "address_receive": None,
    "address_delivery":None,
    "description": None,
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "no change"

def test_order_update_no_area_local (client,user_token,pending_order_route):
    r=client.put(
        f"/orders/{pending_order_route}",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type": OrderType.LOCAL,
    "operating_area" : None,
    "route_from": Governorate.NABLUS,
    "route_to": Governorate.SALFIT,
    "address_receive": "mid",
    "address_delivery":"mid",
    "description": "10 kg door",
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "for local orders u need to add the area not the route"


def test_order_update_no_full_route (client,user_token,pending_order_local):
    r=client.put(
        f"/orders/{pending_order_local}",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type": OrderType.ROUTE,
    "operating_area" : None,
    "route_from": None,
    "route_to": Governorate.SALFIT,
    "address_receive": "mid",
    "address_delivery":"mid",
    "description": "10 kg door",
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "for route orders u need to add a full route not area"

def test_order_update_invalid_route (client,user_token,pending_order_local):
    r=client.put(
        f"/orders/{pending_order_local}",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type": OrderType.ROUTE,
    "operating_area" : None,
    "route_from": Governorate.SALFIT,
    "route_to": Governorate.SALFIT,
    "address_receive": "mid",
    "address_delivery":"mid",
    "description": "10 kg door",
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "invalid route"

def test_order_update_successful (db_session,client,user_token,pending_order_local):
    order = db_session.query(Order).filter(Order.id == pending_order_local).first()
    db_session.delete(order)
    db_session.commit()
    r=client.put(
        f"/orders/{pending_order_local}",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
    "type": OrderType.ROUTE,
    "operating_area" : None,
    "route_from": Governorate.NABLUS,
    "route_to": Governorate.SALFIT,
    "address_receive": "mid",
    "address_delivery":"mid",
    "description": "10 kg door",
        }
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "order not found"

def test_order_status_update_admin_successful (db_session,client,admin_token,pending_order_local) :
    r=client.put(
        f"/orders/{pending_order_local}/status/admin",
        {"Authorization" : f"Bearer {admin_token}"},
        json={
            "status" : OrderStatus.ERROR
        }
    )

    history = db_session.query(HistoryOrder).filter(HistoryOrder.id==pending_order_local).first()
    assert r.status_code == 200
    assert r.json()["status"] == OrderStatus.ERROR
    assert history is not None
    assert history.new_status == OrderStatus.ERROR

def test_order_status_update_admin_to_pending_successful (db_session,client,admin_token,pending_order_local,driver_default) :
    r=client.put(
        f"/orders/{pending_order_local}/status/admin",
        {"Authorization" : f"Bearer {admin_token}"},
        json={
            "status" : OrderStatus.PENDING
        }
    )

    history = db_session.query(HistoryOrder).filter(HistoryOrder.id==pending_order_local).first()
    assignments = db_session.query(DriverAssignment).filter(DriverAssignment.order_id == pending_order_local).all()
    assert r.status_code == 200
    assert r.json()["status"] == OrderStatus.PENDING
    assert history is not None
    assert history.new_status == OrderStatus.PENDING
    assert assignments is not None

def test_order_status_update_admin_no_change (client,admin_token,pending_order_local) :
    r=client.put(
        f"/orders/{pending_order_local}/status/admin",
        {"Authorization" : f"Bearer {admin_token}"},
        json={
            "status" : OrderStatus.PENDING
        }
    )
    assert r.status_code == 400
    assert r.json()["status"] == "no change"


def test_update_status_successful (client,db_session,token_driver_default,accepted_order) :
    r= client.put(
        f"/orders/{accepted_order}/status",
        headers= {"Authorization" : f"Bearer {token_driver_default}"}
    )
    history = db_session.query(HistoryOrder).filter(HistoryOrder.id==accepted_order).first()
    assert r.status_code == 200
    assert history is not None
    assert history.new_status == OrderStatus.IN_TRANSIT

def test_update_status_failed (client,token_driver_default,completed_order) :
    r= client.put(
        f"/orders/{completed_order}/status",
        headers= {"Authorization" : f"Bearer {token_driver_default}"}
    )

    assert r.status_code == 409
    assert r.json()["detail"] == "failed to update"

def test_update_status_not_yours (client,token_driver_default_2,accepted_order) :
    r= client.put(
        f"/orders/{accepted_order}/status",
        headers= {"Authorization" : f"Bearer {token_driver_default_2}"}
    )

    assert r.status_code == 404
    assert r.json()["detail"] == "order not found"

def test_get_my_orders_customer_successful (client,user_token):
    r=client.get(
        "/orders/customer",
        headers={"Authorization" : f"Bearer {user_token}"}
    )

    assert r.status_code == 200

def test_get_my_orders_driver_successful (client,token_driver_default):
    r=client.get(
        "/orders/customer",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )

    assert r.status_code == 200

def test_cancel_order_successful (db_session,client,user_token,pending_order_local) :
    r= client.put(
        f"/orders/{pending_order_local}/cancel",
        headers={"Authorization" : f"Bearer {user_token}"}
    )
    assignment = db_session.query(DriverAssignment).filter(DriverAssignment.order_id == pending_order_local).first()
    assert r.status_code == 200
    assert assignment is not None
    assert assignment.status == AssignmentStatus.EXPIRED
    assert "message" in r.json()

def test_make_order_avilable_again_successful(client,token_driver_default,accepted_order) :
    r=client.put(
        f"/orders/{accepted_order}/make-avilable",
        headers={ "Authorization" :f"Bearer {token_driver_default}"}
    )

    assert r.status_code == 200
    assert "message" in r.json()


def test_make_order_avilable_again_failed(client,token_driver_default,completed_order) :
    r=client.put(
        f"/orders/{completed_order}/make-avilable",
        headers={ "Authorization" :f"Bearer {token_driver_default}"}
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "can't make the order avilable again"