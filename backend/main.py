# from fastapi import Depends, FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# import database_models
# from database import SessionLocal, engine
# from models import Issue
# from classifier import classify_issue
# from classifier import classify_issue, calculate_urgency 

# app = FastAPI()

# database_models.Base.metadata.create_all(bind=engine)

# @app.get("/api/timeline")
# def get_timeline():
#     return []

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#     "http://localhost:5173",
#     "http://localhost:3000"
# ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# database_models.Base.metadata.create_all(bind=engine)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get("/api/issues")
# def get_issues(db: Session = Depends(get_db)):
#     issues = db.query(database_models.Issue).all()
#     return issues

# @app.post("/api/issues")
# def add_issue(issue: Issue, db: Session = Depends(get_db)):

#     # classify issue using HuggingFace model
#     issue_type = classify_issue(issue.description)

#     new_issue = database_models.Issue(
#         description=issue.description,
#         type=issue_type,   # ✅ USE THE CLASSIFIER RESULT
#         location_name=issue.location_name,
#         lat=issue.lat,
#         lng=issue.lng,
#         status="PENDING",
#         urgency=calculate_urgency(issue.description),
#         upvotes=0
#     )

#     db.add(new_issue)
#     db.commit()
#     db.refresh(new_issue)

#     return new_issue

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import database_models
from database import SessionLocal, engine
from models import Issue
# from classifier import classify_issue, calculate_urgency, classify_with_confidence   # 🔴 Disabled for now

app = FastAPI()

# ✅ Create tables (ONLY ONCE)
database_models.Base.metadata.create_all(bind=engine)

@app.get("/api/timeline")
def get_timeline():
    return []

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:3000"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Get Issues
@app.get("/api/issues")
def get_issues(db: Session = Depends(get_db)):
    issues = db.query(database_models.Issue).all()
    return issues

# ✅ Add Issue
@app.post("/api/issues")
def add_issue(issue: Issue, db: Session = Depends(get_db)):
    issue_type = classify_issue(issue.description)
    new_issue = database_models.Issue(
        description=issue.description,
        type=issue_type,
        location_name=issue.location_name,
        lat=issue.lat,
        lng=issue.lng,
        status="PENDING",
        urgency=calculate_urgency(issue.description),
        upvotes=0
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue

@app.post("/api/classify")        # ← THIS WAS MISSING
def classify_endpoint(req: ClassifyRequest):
    return classify_with_confidence(req.description)