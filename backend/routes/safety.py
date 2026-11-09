# backend/routes/safety.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, SafetyReport
from schemas.safety import SafetyReportCreate, SafetyReportResponse, SafetyReportStatusUpdate
from routes.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/safety", tags=["Safety"])

@router.post("/report", response_model=SafetyReportResponse)
def submit_report(
    report: SafetyReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    valid_types = ["HARASSMENT", "OVER_CROWDING", "UNSAFE_TRAVEL", "BUS_BREAKDOWN", "OTHER"]
    if report.report_type.upper() not in valid_types:
        raise HTTPException(status_code=400, detail="Invalid report type")

    new_report = SafetyReport(
        user_id=current_user.id,
        bus_id=report.bus_id,
        route_id=report.route_id,
        report_type=report.report_type.upper(),
        description=report.description,
        status="OPEN"
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

@router.get("/my-reports", response_model=List[SafetyReportResponse])
def get_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(SafetyReport).filter(SafetyReport.user_id == current_user.id).order_by(SafetyReport.created_at.desc()).all()

@router.get("/reports", response_model=List[SafetyReportResponse])
def get_all_reports(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    return db.query(SafetyReport).order_by(SafetyReport.created_at.desc()).all()

@router.get("/reports/{report_id}", response_model=SafetyReportResponse)
def get_report_by_id(
    report_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    report = db.query(SafetyReport).filter(SafetyReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.put("/reports/{report_id}/status", response_model=SafetyReportResponse)
def update_report_status(
    report_id: int,
    status_update: SafetyReportStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    valid_statuses = ["OPEN", "INVESTIGATING", "RESOLVED"]
    if status_update.status.upper() not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    report = db.query(SafetyReport).filter(SafetyReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.status = status_update.status.upper()
    db.commit()
    db.refresh(report)
    return report