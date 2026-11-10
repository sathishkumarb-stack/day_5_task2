
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database import get_db
from src.models import Customer
from src.schemas import CustomerCreate, CustomerUpdate, CustomerOut
from src.security import verify_api_key

app = FastAPI(title="Customer CRUD API - Task 2")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# CREATE
@app.post("/customers", response_model=CustomerOut, status_code=201)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    new_customer = Customer(**customer.model_dump())
    db.add(new_customer)

    try:
        db.commit()
        db.refresh(new_customer)
        return new_customer
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")


# READ ALL with pagination
@app.get("/customers", response_model=list[CustomerOut])
def get_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    offset = (page - 1) * per_page

    return (
        db.query(Customer)
        .order_by(Customer.id)
        .offset(offset)
        .limit(per_page)
        .all()
    )


# READ ONE
@app.get("/customers/{customer_id}", response_model=CustomerOut)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


# UPDATE
@app.put("/customers/{customer_id}", response_model=CustomerOut)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(customer, key, value)

    try:
        db.commit()
        db.refresh(customer)
        return customer
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")


# DELETE
@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()

    return {"message": "Customer deleted successfully"}
