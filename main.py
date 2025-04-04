from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine

from models import Base, CoffeeReview
from crud import get_review, create_review
from schemas import CoffeeReviewCreate, CafeCreate

from typing import Optional
import uvicorn
import logging


from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

# Create tables in the database
Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/reviews/")
async def create_review_endpoint(
    review: CoffeeReviewCreate,
    db: Session = Depends(get_db),
):
    return create_review(db, review)


@app.get("/reviews/{review_id}")
async def get_review_endpoint(review_id: int, db: Session = Depends(get_db)):
    review = get_review(db, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@app.put("/reviews/{review_id}")
async def update_review_endpoint(
    review_id: int,
    drinkType: str,
    roastDarkness: int,
    tasteRating: int,
    price: float,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
):
    review = db.query(CoffeeReview).filter(CoffeeReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    review.drinkType = drinkType
    review.roastDarkness = roastDarkness
    review.tasteRating = tasteRating
    review.price = price
    review.notes = notes
    db.commit()
    db.refresh(review)

    return review


@app.delete("/reviews/{review_id}")
async def delete_review_endpoint(review_id: int, db: Session = Depends(get_db)):
    review = db.query(CoffeeReview).filter(CoffeeReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()

    return {"detail": "Review deleted"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
