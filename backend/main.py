# from fastapi import Depends, FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# import database_models

# from database import engine


# app = FastAPI()

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database_models
from database import SessionLocal, engine
from models import Issue
# from classifier import classify_issue   # 🔴 Disabled for now

app = FastAPI()

# ✅ Create tables (ONLY ONCE)
database_models.Base.metadata.create_all(bind=engine)

# ✅ CORS FIX (allow all)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 🔥 important fix
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Timeline API
@app.get("/api/timeline")
def get_timeline():
    return []

# ✅ Get Issues
@app.get("/api/issues")
def get_issues(db: Session = Depends(get_db)):
    issues = db.query(database_models.Issue).all()
    return issues

# ✅ Add Issue
@app.post("/api/issues")
def add_issue(issue: Issue, db: Session = Depends(get_db)):

    # 🔥 TEMP FIX (avoid classifier crash)
    issue_type = "general"

    # If you want later:
    # issue_type = classify_issue(issue.description)

    new_issue = database_models.Issue(
        description=issue.description,
        type=issue_type,
        location_name=issue.location_name,
        lat=issue.lat,
        lng=issue.lng,
        status="PENDING",
        urgency=50,
        upvotes=0
    )

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return new_issue