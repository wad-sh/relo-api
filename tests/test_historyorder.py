def test_history_get_successful (client,admin_token,pending_order_local) :
    response = client.get(
        f"/history-orders/{pending_order_local}",
        headers={"Authorization" : f"Bearer {admin_token}"}
    )

    assert response.status_code == 200