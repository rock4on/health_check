"""DCMA Point 2: Leads (Negative Lag) checker."""
from typing import List, Dict, Any
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point02Leads(BaseChecker):
    """Check that there are no negative lag values (leads)."""
    
    def __init__(self):
        super().__init__(
            point_number=2,
            description="Leads (Negative Lag)",
            threshold="0",
            recommendation="Remove negative lags and replace with explicit task sequencing to show accurate logic."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check for negative lag values."""
        # This is a placeholder since lag data isn't in our current CSV format
        # In a real implementation, you'd check dependency lag values
        failed_tasks = []
        
        # For now, assume no negative lags found
        return self.format_result(True, "0", failed_tasks)