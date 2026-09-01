from app.models.user import User
def test_register_success (client) :
    response = client.post(
        "/users/register",
        json={
            "username" : "tt1",
            "email" : "test1@gmail.com",
            "phone_number" : "0599887474",
            "password" : "12345678"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == "tt1"
    assert response.json()["email"] == "test1@gmail.com"



def test_reg_used_username (client,user) :
    
    response = client.post(
        "/users/register",
        json={
                    "username" : "tt1",
                    "email" : "t111122@gmail.com",
                    "phone_number" : "0599887474",
                    "password" : "12345678"
                }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "username already existed"

def test_reg_used_email (client,user) :
    

    response = client.post(
        "/users/register",
        json={
                    "username" : "test1111",
                    "email" : "test1@gmail.com",
                    "phone_number" : "0599887474",
                    "password" : "12345678"
                }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "email already existed"


def test_login_success_email (client,user) :
    

    response = client.post(
        "/users/login",
        data={
            "username" : "test1@gmail.com",
            "password" : "12345678"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_success_username (client,user) :
    

    response = client.post(
        "/users/login",
        data={
            "username" : "tt1",
            "password" : "12345678"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password (client,user) :
    

    response = client.post(
            "/users/login",
            data={
                "username" : "test1@gmail.com",
                "password" : "4444"
            }
        )

    assert response.status_code == 401
    assert response.json()["detail"] =="wrong email/username or password"



def test_login_wrong_email (client,user) :
    
    
    response = client.post(
                "/users/login",
                data={
                    "username" : "test10000@gmail.com",
                    "password" : "12345678"
                }
            )
    
    assert response.status_code == 401
    assert response.json()["detail"] =="wrong email/username or password"

def test_login_wrong_username (client,user) :
    
    
    response = client.post(
                "/users/login",
                data={
                    "username" : "tttttttttttttttttttttt1111132",
                    "password" : "12345678"
                }
            )
    
    assert response.status_code == 401
    assert response.json()["detail"] =="wrong email/username or password"

def test_delete_successfully (client,user_token) :
    r = client.delete(
        "/users/me",
        headers={"Authorization" : f"Bearer {user_token}"}
    )
    assert r.status_code == 200
    assert r.json()["message"] == "your account has been deleted"

def test_delete_not_found (client,user_token,db_session,user) :

    db_session.delete(user)
    db_session.commit()
    r = client.delete(
        "/users/me",
        headers={"Authorization" : f"Bearer {user_token}"}
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "no user has been found"

def test_delete_has_orders (client,user_token,accepted_order):
    r = client.delete(
        "/users/me",
        headers={"Authorization" : f"Bearer {user_token}"}
    )

    assert r.status_code == 409
    assert r.json()["detail"] =="you have orders accepted or in transit"

def test_delete_has_trips (client,token_driver_default,active_trip) :
        r = client.delete(
        "/users/me",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
        assert r.status_code == 409
        assert r.json()["detail"] == "you have trips planned or active"

def test_delete_has_apps (client,user_token,active_apps) :
        r = client.delete(
        "/users/me",
        headers={"Authorization" : f"Bearer {user_token}"}
    )
        assert r.status_code == 409
        assert r.json()["detail"] == "you have a pending driver application"

def test_delete_driver_has_orders (client,token_driver_default,accepted_order):
        r = client.delete(
        "/users/me",
        headers={"Authorization" : f"Bearer {token_driver_default}"}
    )
        assert r.status_code == 409
        assert r.json()["detail"] == "you have active orders as a driver"

def test_update_successfully (client,user_token):
    r= client.put(
        "/users/profile",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
            "username" : "new11",
            "email" : "new11@gmail.com"
        }
    )

    assert r.status_code == 200
    assert r.json()["username"] == "new11"
    assert r.json()["email"] == "new11@gmail.com"

def test_update_no_change (client,user_token):
    r= client.put(
        "/users/profile",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={
             "username" : None,
             "email" : None
        }
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "no change"

def test_update_same_username (client,user_token,user) :
    r= client.put(
        "/users/profile",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={"username" : user.username}
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "this username is already yours"

def test_update_same_email (client,user_token,user) :
    r= client.put(
        "/users/profile",
        headers={"Authorization" : f"Bearer {user_token}"},
        json={"email" : user.email}
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "email still the same"



def test_update_password_successful (client,user_token):
    r=client.put(
         "/users/password",
                 headers={"Authorization" : f"Bearer {user_token}"},
        json={
                "password" : "1597534682"
        }
         
    )
    assert r.status_code == 200
    assert r.json()["message"] == "password has been changed successfully"

def test_update_password_no_change (client,user_token):
    r=client.put(
         "/users/password",
                 headers={"Authorization" : f"Bearer {user_token}"},
        json={
                "password" : "12345678"
        }
         
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "can not use the same password"

def test_update_number_successful (client,user_token):
    r=client.put(
         "/users/phone",
                 headers={"Authorization" : f"Bearer {user_token}"},
        json={
                "phone_number" : "0571337419"
        }
         
    )
    assert r.status_code == 200
    assert r.json()["phone_number"] == "0571337419"



def test_update_number_no_change (client,user_token):
    r=client.put(
         "/users/phone",
                 headers={"Authorization" : f"Bearer {user_token}"},
        json={
                "phone_number" : "0599884747"
        }
         
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "no change"