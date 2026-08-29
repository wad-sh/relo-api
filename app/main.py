from fastapi import FastAPI
from app.routers.application_router import application_router
from app.routers.assignment_router import assignment_router
from app.routers.driver_router import driver_router
from app.routers.history_router import history_router
from app.routers.order_router import order_router
from app.routers.trip_router import trip_router
from app.routers.user_rounter import user_router

app=FastAPI()

app.include_router(application_router)
app.include_router(assignment_router)
app.include_router(driver_router)
app.include_router(history_router)
app.include_router(order_router)
app.include_router(trip_router)
app.include_router(user_router)


