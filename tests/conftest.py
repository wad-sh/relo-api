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




test_engine = create_engine(TEST_DATABASE_URL)

test_session_local = sessionmaker (
    bind= test_engine,
    autoflush=False
)

@pytest.fixture
def db_session ():
    Base.metadata.create_all(bind= test_engine)

    db = test_session_local()
    yield db
    db.close()
    Base.metadata.drop_all(bind= test_engine)

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
    userrr = db_session.query(User).filter(
        User.username == "tt1"
    ).first()

    return userrr

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
        id= user_driver.id
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
    assert "created_at" in r.json()
    return r.json()


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
    return r.json()

@pytest.fixture
def accepted_order (db_session,user,driver_default):
    order= Order(
        order_owner_id=user.id,
        status= OrderStatus.ACCEPTED,
        type= OrderType.LOCAL,
        operating_area= Governorate.SALFIT,
        address_receive="from there",
        address_delivery= "to there",
        description= "laptop",
        driver_id= driver_default.id,    
        )

    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    return order