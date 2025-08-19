"""Pydantic models for DCMA analysis."""
from typing import List
from pydantic import BaseModel


class DCMARecommendation(BaseModel):
    """Single DCMA recommendation."""
    point_number: int
    point_name: str
    status: str  # "PASS" or "FAIL"
    threshold: str
    actual_value: str
    recommendation: str = None
    priority: str = None  # "HIGH", "MEDIUM", "LOW"


class DCMAAnalysisResponse(BaseModel):
    """Structured response for DCMA analysis."""
    executive_summary: str
    overall_health_score: str
    total_checks: int
    passed_checks: int
    failed_checks: int
    recommendations: List[DCMARecommendation]
    implementation_plan: List[str]
    risk_assessment: str