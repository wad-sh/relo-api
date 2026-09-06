# Relo API

A RESTful Delivery Management API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

Relo API is a backend system designed to manage delivery operations between customers, drivers, and administrators. Customers can create delivery orders, drivers can receive and accept assignments, and administrators can review driver applications and manage delivery operations.

---

## Features

- JWT-based authentication
- Role-based authorization
- Customer, Driver, and Admin roles
- User registration and login
- Driver application workflow
- Admin application review
- Local and route delivery orders
- Automatic driver assignment
- Driver assignment acceptance
- Local, Flexible, and Trip driver modes
- Route-based trip matching
- Delivery order status management
- Order history and audit trail
- Delivery fee handling
- Request and response validation with Pydantic
- PostgreSQL database
- SQLAlchemy ORM
- Alembic database migrations
- Automated testing with pytest
- Transaction handling
- Row-level locking for critical order-acceptance operations

---

# System Overview

Relo API is built around three main types of users:

```text
                    ┌─────────────┐
                    │   Customer  │
                    └──────┬──────┘
                           │
                    Creates Orders
                           │
                           ▼
                    ┌─────────────┐
                    │    Order    │
                    └──────┬──────┘
                           │
                  Creates Assignments
                           │
                           ▼
                    ┌─────────────┐
                    │   Drivers   │
                    └──────┬──────┘
                           │
                      Accept Order
                           │
                           ▼
                    ┌─────────────┐
                    │  Delivery   │
                    │  Operation  │
                    └─────────────┘

                    ┌─────────────┐
                    │    Admin    │
                    └──────┬──────┘
                           │
              Reviews Applications
              & Manages Operations
User Roles
Customer

Customers can:

Register an account
Log in
Create delivery orders
View their orders
Cancel eligible orders
View order history
Submit an application to become a driver
Driver

Drivers can:

Log in
Receive delivery assignments
Accept available assignments
Handle assigned deliveries
Operate using different driver modes
Admin

Administrators can:

Review driver applications
Accept or reject applications
Monitor delivery operations
Update order statuses
Record details for administrative status changes
Authentication

Authentication is implemented using JWT access tokens.

Protected endpoints require an authorization header:

Authorization: Bearer <access_token>

Authentication and authorization are separated:

Authentication verifies the identity of the user.
Authorization verifies whether the authenticated user has permission to perform the requested operation.

Role-based authorization is used for customer, driver, and administrator operations.

Delivery Orders

Relo supports two main types of delivery orders.

Local Orders

A local order is a delivery within a specific operating area.

A local order contains:

Operating area
Pickup address
Delivery address
Description

Example:

{
  "type": "LOCAL",
  "operating_area": "NABLUS",
  "address_receive": "Example pickup address",
  "address_delivery": "Example delivery address",
  "description": "Package description"
}
Route Orders

A route order represents a delivery between two governorates.

A route order contains:

Route origin
Route destination
Pickup address
Delivery address
Description

Example:

{
  "type": "ROUTE",
  "route_from": "NABLUS",
  "route_to": "RAMALLAH_AND_AL_BIREH",
  "address_receive": "Example pickup address",
  "address_delivery": "Example delivery address",
  "description": "Package description"
}

The order schemas use a discriminated union based on the type field, allowing each order type to have its own required fields.

Driver Modes

Drivers can operate in three different modes.

LOCAL

A Local driver handles local orders within their configured operating area.

A Local driver can accept a local order only when:

Driver operating area == Order operating area
FLEXIBLE

A Flexible driver is a general-purpose driver.

A Flexible driver can:

Handle local orders when the operating area matches
Handle route orders without requiring a predefined trip
TRIP

A Trip driver handles route orders through planned trips.

A Trip driver can be matched with a route order when the driver's planned trip matches:

Trip route_from == Order route_from
Trip route_to   == Order route_to
Trip status     == PLANNED
Driver Assignments

When a delivery order is created, the system finds eligible drivers and creates assignments for them.

Assignments initially have a waiting state.

WAITING
   |
   v
TAKEN

If an order becomes unavailable, its active assignments are expired.

Assignment Rules
Local Order

Eligible drivers:

LOCAL      -> matching operating area
FLEXIBLE   -> matching operating area
TRIP       -> not eligible
Route Order

Eligible drivers:

FLEXIBLE   -> eligible for any route
TRIP       -> eligible when a planned trip matches the route
LOCAL      -> not eligible
Accepting an Assignment

When a driver accepts an assignment, the system performs several operations together:

Validates the driver.
Verifies that the assignment belongs to that driver.
Verifies that the assignment is still available.
Locks the relevant order.
Locks the driver record.
Checks the driver's active-order limit.
Expires the other assignments for the order.
Marks the accepted assignment as TAKEN.
Assigns the order to the driver.
Changes the order status to ACCEPTED.
Records the response timestamp.
Commits the transaction.

A driver cannot have more than 5 active orders at the same time.

The active statuses considered for this limit are:

ACCEPTED
IN_TRANSIT
Order Lifecycle

A typical order lifecycle is:

PENDING
   |
   v
ACCEPTED
   |
   v
IN_TRANSIT
   |
   v
DELIVERED

Orders can also enter other states such as cancellation or error states according to the business rules.

When an order is no longer available to drivers, its active assignments are expired.

Order Cancellation

Customers can cancel eligible orders.

When an order is cancelled:

Order
  |
  +--> status = CANCELLED
  |
  +--> active assignments = EXPIRED

The order is then committed to the database.

Administrative Status Changes

Administrators can update order statuses through a dedicated administrative operation.

Administrative status changes require additional details/reasoning.

Example:

{
  "status": "ERROR",
  "more_details": "Reason for changing the order status"
}

This provides an audit trail for administrative actions.

The system also prevents an administrator from performing a status update when the requested status is already the current status.

Order History

Important order status changes are recorded in the order history.

A history record can contain:

Order ID
Previous status
New status
User responsible for the change
Additional details
Timestamp

Example workflow:

Order status changes
        |
        v
Create History Record
        |
        v
Persist Audit Information

This allows the system to maintain a record of important operational changes.

Driver Applications

Customers can submit an application to become drivers.

An application contains information such as:

Vehicle type
Vehicle model
Vehicle year
Vehicle capacity
Preferred operating area
Preferred route
Additional description

Example:

{
  "vehicle_type": "TRUCK",
  "vehicle_model": "XX",
  "vehicle_year": 2020,
  "vehicle_capacity_kg": 500,
  "preferred_area": "JERUSALEM",
  "preferred_route_from": null,
  "preferred_route_to": null,
  "description": "Additional information"
}
Application Lifecycle

Applications follow a review workflow:

PENDING
   |
   +----------------+
   |                |
   v                v
ACCEPTED         REJECTED

Only customers are allowed to submit driver applications.

Drivers and administrators cannot submit new driver applications.

The system also prevents a customer from creating another active application while an existing active application is still active.

Application Validation

Application input is validated using Pydantic.

For example, the vehicle year has a defined valid range:

Minimum: 1930
Maximum: Current year

Invalid values are rejected during request validation.

Delivery Fees

The current delivery fee rules are:

Order Type	Delivery Fee
Local	10
Route	20
Database

Relo API uses PostgreSQL as its relational database.

Database access is implemented using SQLAlchemy.

Database schema changes are managed using Alembic migrations.

Main Domain Models

The project contains models representing:

User
Driver
Delivery Order
Driver Application
Driver Assignment
Trip
Order History

The Driver entity is associated with a User account, with the driver's identifier tied to the corresponding user identifier.

Database Migrations

Alembic is used to manage database schema changes.

Apply all migrations:

alembic upgrade head

Check the current migration:

alembic current

Create a new migration after modifying database models:

alembic revision --autogenerate -m "describe your change"

Then apply it:

alembic upgrade head
Transactions & Concurrency

Operations that modify multiple related records are performed within database transactions.

The assignment acceptance operation uses SQLAlchemy's row-level locking:

.with_for_update()

The order and driver records involved in the critical operation are locked before the final state changes are committed.

This is important because accepting an assignment changes several related pieces of state:

Assignment
    |
    +--> TAKEN
    |
    v
Order
    |
    +--> ACCEPTED
    |
    +--> driver_id updated
    |
    v
Other assignments
    |
    +--> EXPIRED

The implementation therefore treats assignment acceptance as a transactional operation rather than as a collection of unrelated database updates.

API Structure

The application is organized around resource-based routers.

Main resource areas include:

/users
/orders
/assignmnts
/applications
/trips
/history
Authentication
POST /users/register
POST /users/login
Orders

Representative order operations include:

POST /orders
GET /orders/...
PUT /orders/{order_id}/cancel
PUT /orders/{order_id}/status
PUT /orders/{order_id}/status/admin
Assignments

Driver assignment acceptance:

PUT /assignmnts/{assignment_id}/accept
Applications

Create a driver application:

POST /applications

Administrative application operations provide the review workflow for accepting or rejecting applications.

The FastAPI routers and OpenAPI documentation are the source of truth for the complete endpoint list and exact request/response schemas.

HTTP Status Codes

The API uses standard HTTP status codes for successful and failed operations.

Status	Meaning
200	Successful operation
201	Resource created
400	Invalid business operation
401	Authentication required or invalid
403	Insufficient permissions
404	Resource not found
409	Business-rule conflict
422	Request validation error
500	Unexpected server error
Validation & Business Logic

The project separates two types of validation.

Request Validation

Pydantic handles structural validation such as:

Required fields
Data types
Enum values
Numeric ranges
Discriminated unions

For example, an invalid vehicle year can be rejected before the request reaches the service layer.

Business Validation

The service layer handles rules such as:

Only customers can apply to become drivers.
A customer cannot maintain multiple active applications.
Drivers can only accept their own assignments.
An assignment must still be available.
A driver cannot exceed five active orders.
Local drivers must match the local operating area.
Trip drivers must have a matching planned trip.
Customers can only modify their own eligible orders.
Administrators cannot perform a status update that results in no state change.
Project Architecture

The application follows a layered backend structure.

Client
  |
  v
FastAPI Router
  |
  v
Authentication / Authorization
  |
  v
Service Layer
  |
  v
SQLAlchemy ORM
  |
  v
PostgreSQL

The main responsibilities are separated into:

Routers

Handle:

HTTP requests
Dependencies
Authentication requirements
Response models
Schemas

Handle:

Request validation
Response serialization
API data contracts
Services

Handle:

Business logic
Validation rules
Transactions
Database operations
Models

Represent:

Database tables
Relationships
Database-level structure
Enums

Represent domain-specific states such as:

User roles
Order types
Order statuses
Application statuses
Assignment statuses
Driver modes
Vehicle types
Governorates
Project Structure

The project follows a modular structure similar to:

relo-api/
│
├── app/
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── routers/
│   │
│   ├── enums/
│   │
│   ├── database.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── ...
│
├── tests/
│   └── ...
│
├── alembic.ini
├── requirements.txt
├── .env
└── README.md

The exact files and modules may vary as the project evolves.

Tech Stack
Backend
Python
FastAPI 0.141.1
Uvicorn 0.52.2
Database
PostgreSQL
SQLAlchemy 2.0.52
Psycopg 3.3.4
Psycopg2
Validation & Configuration
Pydantic 2.13.4
Pydantic Settings 2.15.0
python-dotenv
Authentication & Security
python-jose 3.5.0
Argon2
pwdlib 0.3.1
cryptography 50.0.0
Database Migrations
Alembic 1.19.1
Testing
pytest 9.1.1
HTTPX
FastAPI TestClient

The complete dependency list is available in:

requirements.txt
Requirements

Before running the project, make sure you have:

Python installed
PostgreSQL installed and running
Git installed

The project dependencies can be installed from requirements.txt.

Installation
1. Clone the repository
git clone https://github.com/wad-sh/relo-api.git
cd relo-api
2. Create a virtual environment

Windows:

python -m venv .venv

Activate it using Command Prompt:

.venv\Scripts\activate.bat

Or PowerShell:

.venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
Environment Configuration

Create a .env file in the project root.

Example:

DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/relo_api

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

Replace the database credentials and secret key with your own values.

Important

Do not commit .env to Git.

Secrets and database credentials should remain outside source control.

Database Setup

Create a PostgreSQL database for the project.

Configure the database connection inside .env.

Then run:

alembic upgrade head

This creates the database schema according to the project's migration history.

Running the Application

Start the development server:

uvicorn app.main:app --reload

The API will normally be available at:

http://127.0.0.1:8000
API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI
http://127.0.0.1:8000/docs
ReDoc
http://127.0.0.1:8000/redoc

The documentation can be used to inspect:

Available endpoints
Request schemas
Response schemas
Authentication requirements
HTTP status codes
Testing

The project uses pytest for automated testing.

Run the complete test suite:

pytest

For verbose output:

pytest -v

The tests cover important parts of the application, including:

Authentication
Authorization
User roles
Order creation
Order validation
Order cancellation
Order status updates
Driver assignments
Assignment acceptance
Driver applications
Application validation
Business rules
Order history

The test suite uses FastAPI's testing tools and database fixtures to verify API behavior.

Testing Philosophy

The tests focus on both:

Happy Paths

Examples:

Customer successfully creates an order
Driver successfully accepts an assignment
Customer successfully creates an application
Admin successfully changes an order status
Failure Cases

Examples:

Unauthorized user
Wrong role
Missing resource
Invalid request
Duplicate active application
Unavailable assignment
Too many active orders
Invalid business operation

This ensures that the API does not only work under ideal conditions but also enforces its business rules.

Security

The project includes several security-related mechanisms:

Password hashing
JWT authentication
Role-based authorization
Protected endpoints
Resource ownership validation
Environment-based secrets
Database transactions
Input validation

Passwords should never be stored as plain text.

Secret keys and database credentials should never be hard-coded into the source code.

Example Delivery Workflow

A normal delivery operation can be represented as:

Customer
   |
   | Create delivery order
   v
PENDING
   |
   | System finds eligible drivers
   v
Driver Assignments
   |
   | Drivers receive WAITING assignments
   v
Driver accepts assignment
   |
   +----------------------------+
   |                            |
   v                            v
Assignment = TAKEN        Other assignments = EXPIRED
   |
   v
Order = ACCEPTED
   |
   v
IN_TRANSIT
   |
   v
DELIVERED
Example Driver Application Workflow
Customer
   |
   | Submit application
   v
PENDING
   |
   | Admin reviews application
   |
   +----------------------+
   |                      |
   v                      v
ACCEPTED               REJECTED
Error Handling

Expected application and business errors are handled using FastAPI's HTTPException.

Examples include:

401 Unauthorized
404 Not Found
409 Conflict
400 Bad Request

Unexpected exceptions are rolled back at the transaction level where appropriate and returned as internal server errors rather than leaving partially committed changes.

Development Workflow

A typical development workflow is:

1. Modify code
       |
       v
2. Update models/schemas/services
       |
       v
3. Create Alembic migration if database changes are required
       |
       v
4. Apply migration
       |
       v
5. Add/update tests
       |
       v
6. Run pytest
       |
       v
7. Commit changes
Database Migration Workflow

When a SQLAlchemy model changes:

alembic revision --autogenerate -m "describe the change"

Review the generated migration before applying it.

Then:

alembic upgrade head

Avoid relying on Base.metadata.create_all() as a replacement for migrations in a project where Alembic is being used to manage the schema.

Design Decisions
Discriminated Order Schemas

Local and route orders do not require the same fields.

Instead of making every field optional, the API uses separate schemas selected by the order type.

OrderCreate
   |
   +---- LOCAL
   |
   +---- ROUTE

This keeps request validation explicit and prevents invalid combinations of fields.

Service-Layer Business Logic

Business rules are implemented in services rather than placing the entire application logic inside routers.

This keeps routers relatively thin and makes the business logic easier to test.

Assignment Expiration

Assignments are expired instead of being deleted when they are no longer available.

This preserves the assignment record and its state history.

Transactional Assignment Acceptance

Assignment acceptance modifies several related records and therefore is handled as one transactional operation.

Future Improvements

Possible future improvements include:

Refresh token support
Pagination
Filtering and sorting
Driver availability management
Customer and driver notifications
Real-time delivery tracking
WebSocket support
Dedicated concurrency/load testing
Dockerization
CI/CD pipeline
Production deployment configuration
API rate limiting
More extensive integration testing
Monitoring and logging
Automated API documentation publishing
Project Status
Completed

Relo API currently contains the core delivery-management backend, including:

Authentication
Authorization
User roles
Driver applications
Application review workflow
Delivery orders
Driver assignments
Assignment acceptance
Driver modes
Trips
Order status management
Order cancellation
Order history
Delivery fees
PostgreSQL persistence
SQLAlchemy ORM
Alembic migrations
Automated tests
Author

Wadee

GitHub:

https://github.com/wad-sh/relo-api

License

This project is currently a personal/portfolio project.

If a formal open-source license is added in the future, this section should be updated accordingly.