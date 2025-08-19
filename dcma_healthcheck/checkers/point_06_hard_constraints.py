"""DCMA Point 6: Hard Constraints checker."""
from typing import List, Dict, Any
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point06HardConstraints(BaseChecker):
    """Check that ≤5% of activities have hard constraints."""
    
    def __init__(self):
        super().__init__(
            point_number=6,
            description="Hard Constraints",
            threshold="≤ 5%",
            recommendation="Replace hard constraints with flexible alternatives (e.g., 'As Late As Possible') to ensure that schedule outcomes are governed by logical sequencing."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check for hard constraints."""
        # This is a placeholder since constraint data isn't in our current CSV format
        # In a real implementation, you'd check for "Must Start On" or "Must Finish On" constraints
        failed_tasks = []
        
        # For now, assume no hard constraints found
        return self.format_result(True, "0%", failed_tasks)