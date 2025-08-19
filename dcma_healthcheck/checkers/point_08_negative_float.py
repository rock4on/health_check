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
        negative_float_count = 0
        failed_tasks = []
        
        for task in schedule_lines:
            if task.total_slack < 0:
                negative_float_count += 1
                failed_tasks.append(f"{task.unique_id}: {task.task_name} ({task.total_slack} days)")
        
        passed = negative_float_count == 0
        return self.format_result(passed, str(negative_float_count), failed_tasks)