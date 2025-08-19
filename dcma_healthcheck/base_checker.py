"""Base class for all DCMA checkers."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models.schedule_data import ScheduleLine


class BaseChecker(ABC):
    """Base class for all DCMA point checkers."""
    
    def __init__(self, point_number: int, description: str, threshold: str, 
                 recommendation: str):
        """Initialize checker with point details."""
        self.point_number = point_number
        self.description = description
        self.threshold = threshold
        self.recommendation = recommendation
        
    @abstractmethod
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check the schedule against this DCMA point.
        
        Returns:
            Dict with 'passed', 'value', 'threshold', 'failed_tasks', 'recommendation'
        """
        pass
        
    def format_result(self, passed: bool, value: Any, failed_tasks: List[str] = None) -> Dict[str, Any]:
        """Format the check result consistently."""
        return {
            'point': self.point_number,
            'description': self.description,
            'threshold': self.threshold,
            'value': value,
            'passed': passed,
            'failed_tasks': failed_tasks or [],
            'recommendation': self.recommendation if not passed else None
        }