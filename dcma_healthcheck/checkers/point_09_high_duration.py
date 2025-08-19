"""DCMA Point 9: High Duration checker."""
from typing import List, Dict, Any
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point09HighDuration(BaseChecker):
    """Check that ≤5% of activities have duration >44 days."""
    
    def __init__(self):
        super().__init__(
            point_number=9,
            description="High Duration",
            threshold="≤ 5%",
            recommendation="Break long-duration tasks into smaller, more manageable activities with logical dependencies."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check for high duration activities."""
        if not schedule_lines:
            return self.format_result(True, "0%", [])
            
        # Filter out milestone tasks (duration = 0)
        regular_tasks = [
            line for line in schedule_lines 
            if line.duration > 0
        ]
        
        if not regular_tasks:
            return self.format_result(True, "0%", [])
            
        # Count tasks with high duration
        high_duration_tasks = 0
        failed_tasks = []
        
        for task in regular_tasks:
            if task.duration > 44:
                high_duration_tasks += 1
                failed_tasks.append(f"{task.unique_id}: {task.task_name} ({task.duration} days)")
        
        percentage = (high_duration_tasks / len(regular_tasks)) * 100
        passed = percentage <= 5.0
        
        return self.format_result(passed, f"{percentage:.1f}%", failed_tasks)