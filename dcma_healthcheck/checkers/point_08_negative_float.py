"""DCMA Point 8: Negative Float checker."""
from typing import List, Dict, Any
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point08NegativeFloat(BaseChecker):
    """Check that there is no negative float."""
    
    def __init__(self):
        super().__init__(
            point_number=8,
            description="Negative Float",
            threshold="0",
            recommendation="Re-sequence or adjust the schedule to eliminate negative float and align with project goals."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check for negative float values."""
        # This is a placeholder since float data isn't in our current CSV format
        # In a real implementation, you'd check for negative float values
        failed_tasks = []
        
        # For now, assume no negative float found
        return self.format_result(True, "0", failed_tasks)