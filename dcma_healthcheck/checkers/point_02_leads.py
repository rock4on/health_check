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
        """Check for negative lag values in predecessor relationships."""
        failed_tasks = []
        negative_lag_count = 0
        
        for task in schedule_lines:
            # Check predecessors for lag indicators (e.g., "76FS-5 days")
            for pred in task.predecessors:
                if 'FS-' in pred or 'SS-' in pred or 'FF-' in pred or 'SF-' in pred:
                    negative_lag_count += 1
                    failed_tasks.append(f"{task.unique_id}: {task.task_name} (predecessor: {pred})")
        
        passed = negative_lag_count == 0
        return self.format_result(passed, str(negative_lag_count), failed_tasks)