from app.main import app
from app.database.database import get_db,Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.config import TEST_DATABASE_URL
import pytest
from fastapi.testclient import TestClient
from app.enums.order import OrderType,OrderStatus
from app.enums.user_enum import UserEnum
from app.enums.route_enum import Governorate
from app.models.user import User
from app.models.driver import Driver
from app.auth.security import password_hash
from app.enums.application import VehicleType
from app.models.order import Order
from app.enums.driver_modes import DrivingMode
from app.enums.trip import TripStatus
from app.models.trip import Trip





test_engine = create_engine(TEST_DATABASE_URL)

test_session_local = sessionmaker (
    bind= test_engine,
    autoflush=False
)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=test_engine)
    db = test_session_local()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def client (db_session) :
    def get_db_test ():
        yield db_session

    app.dependency_overrides[get_db] = get_db_test
    yield TestClient(app)
    app.dependency_overrides.clear()
     
@pytest.fixture
def user (client,db_session) :
    user_data = {
            "username" : "tt1",
            "email" : "test1@gmail.com",
            "phone_number": "0599884747",
            "password" : "12345678"
        }
    response = client.post(
        "/users/register",
        json= user_data
    )

    assert response.status_code == 200
    db_session.expire_all()


    return db_session.query(User).filter(User.username == "tt1").first()

@pytest.fixture
def user_token (client,user) :
    response = client.post(
            "/users/login",
            data={
                "username" : user.username,
                "password" : "12345678"
            }
        )
    
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def driver_default (db_session) :
    user_driver = User(
            username = "tt2",
            email = "test2@gmail.com",
            phone_number= "0597979797",
            hashed_password= password_hash("12345678"),
            role = UserEnum.Driver
    )
    db_session.add(user_driver)
    db_session.flush()

    driver = Driver(
        id= user_driver.id,
        local_operating_area= Governorate.HEBRON
    )

    db_session.add(driver)
    db_session.commit()
    return driver
@pytest.fixture
def token_driver_default(client, driver_default):
    r = client.post(
        "/users/login",
        data={
            "username": "tt2",
            "password": "12345678"
        }
    )

    assert r.status_code == 200
    return r.json()["access_token"]


    
@pytest.fixture
def active_trip (client,token_driver_default) :
    r=client.post(
        "/trips",
        headers={"Authorization" : f"Bearer {token_driver_default}"},
        json={
            "route_from" : Governorate.TULKARM,
            "route_to" : Governorate.QALQILYA
        }
    )
    assert r.status_code == 200
    assert "id" in r.json()
    return r.json()["id"]


@pytest.fixture
def active_apps (client,user_token) :
    r=client.post(
        "/applications",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
            "vehicle_type" : VehicleType.TRUCK,
            "vehicle_model" : 'volvo',
            "vehicle_year" : 1990,
            "vehicle_capacity_kg" : 1000,
            "preferred_area" : Governorate.QALQILYA
        }
    )
    assert r.status_code == 200
    assert "id" in r.json()
    return r.json()["id"]

@pytest.fixture
def accepted_order (db_session,user,driver_default):
    order= Order(
        order_owner_id=user.id,
        status= OrderStatus.ACCEPTED,
        type= OrderType.LOCAL,
        operating_area= Governorate.HEBRON,
        address_receive="from there",
        address_delivery= "to there",
        description= "laptop",
        driver_id= driver_default.id,    
        )

    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order.id

@pytest.fixture
def driver_trip (db_session) :
    user_driver = User(
            username = "driver12",
            email = "test3333@gmail.com",
            phone_number= "0597900797",
            hashed_password= password_hash("12345678"),
            role = UserEnum.Driver
    )
    db_session.add(user_driver)
    db_session.flush()

    driver = Driver(
        id= user_driver.id,
        mode = DrivingMode.TRIP
    )

    db_session.add(driver)
    db_session.commit()
    return driver

@pytest.fixture
def token_driver_trip(client, driver_trip):
    r = client.post(
        "/users/login",
        data={
            "username": "driver12",
            "password": "12345678"
        }
    )

    assert r.status_code == 200
    return r.json()["access_token"]


@pytest.fixture
def driver_local (db_session) :
    user_driver = User(
            username = "local1",
            email = "local1@gmail.com",
            phone_number= "0597910797",
            hashed_password= password_hash("12345678"),
            role = UserEnum.Driver
    )
    db_session.add(user_driver)
    db_session.flush()

    driver = Driver(
        id= user_driver.id,
        mode = DrivingMode.LOCAL,
        local_operating_area = Governorate.HEBRON
    )

    db_session.add(driver)
    db_session.commit()
    return driver

@pytest.fixture
def token_driver_local(client, driver_local):
    r = client.post(
        "/users/login",
        data={
            "username": "local1",
            "password": "12345678"
        }
    )

    assert r.status_code == 200
    return r.json()["access_token"]

@pytest.fixture 
def completed_trip (db_session,driver_default):
    trip = Trip(
        driver_id = driver_default.id,
        route_from= Governorate.HEBRON,
        route_to=Governorate.BETHLEHEM,
        status= TripStatus.COMPLETED
    )

    db_session.add(trip)
    db_session.commit()
    db_session.refresh(trip)
    return trip.id

@pytest.fixture
def admin(db_session) :
        admin = User(
        username="un",
        email="em@gmail.com",
        hashed_password = password_hash("12345678"),
        role = UserEnum.Admin,
        phone_number="0567676769"
    )

        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)
        return admin

@pytest.fixture
def admin_token (client,admin) :
    response = client.post(
            "/users/login",
            data={
                "username" : admin.username,
                "password" : "12345678"
            }
        )
    
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def order_in_trip (db_session,active_trip,user,driver_default):
    order= Order(
        order_owner_id=user.id,
        status= OrderStatus.ACCEPTED,
        type= OrderType.ROUTE,
        route_from= Governorate.TULKARM,
        route_to= Governorate.QALQILYA,
        address_receive="from there",
        address_delivery= "to there",
        description= "laptop",
        trip_id=active_trip,
        driver_id= driver_default.id,    
        )

    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order.id


@pytest.fixture 
def pending_order_local (client,user_token,driver_default) :
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
    assert r.status_code == 200
    assert "id" in r.json()
    return r.json["id"]

@pytest.fixture
def pending_order_route (client,user_token,driver_default) :
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
    return r.json()["id"]



@pytest.fixture
def completed_order (db_session,user,driver_default):
    order= Order(
        order_owner_id=user.id,
        status= OrderStatus.DELIVERED,
        type= OrderType.LOCAL,
        operating_area= Governorate.HEBRON,
        address_receive="from there",
        address_delivery= "to there",
        description= "laptop",
        driver_id= driver_default.id,    
        )

    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order.id


@pytest.fixture
def driver_default_2 (db_session) :
    user_driver = User(
            username = "tt22",
            email = "test22@gmail.com",
            phone_number= "0597979727",
            hashed_password= password_hash("12345678"),
            role = UserEnum.Driver
    )
    db_session.add(user_driver)
    db_session.flush()

    driver = Driver(
        id= user_driver.id,
        local_operating_area= Governorate.HEBRON
    )

    db_session.add(driver)
    db_session.commit()
    return driver
@pytest.fixture
def token_driver_default_2(client, driver_default):
    r = client.post(
        "/users/login",
        data={
            "username": "tt22",
            "password": "12345678"
        }
    )

    assert r.status_code == 200
    return r.json()["access_token"]
