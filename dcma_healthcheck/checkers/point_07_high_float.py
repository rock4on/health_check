"""DCMA Point 7: High Float checker."""
from typing import List, Dict, Any
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point07HighFloat(BaseChecker):
    """Check that ≤5% of activities have float >44 days."""
    
    def __init__(self):
        super().__init__(
            point_number=7,
            description="High Float",
            threshold="≤ 5%",
            recommendation="Analyze tasks with high float for unnecessary delay or missing dependencies."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check for high float values (>44 days)."""
        if not schedule_lines:
            return self.format_result(True, "0%", [])
        
        # Filter out milestone and completed tasks
        regular_tasks = [
            task for task in schedule_lines 
            if task.wbs_std not in ['START', 'CMPLT', 'MLSTN'] and task.duration > 0
        ]
        
        if not regular_tasks:
            return self.format_result(True, "0%", [])
        
        high_float_count = 0
        failed_tasks = []
        
        for task in regular_tasks:
            if task.total_slack > 44:
                high_float_count += 1
                failed_tasks.append(f"{task.unique_id}: {task.task_name} ({task.total_slack} days float)")
        
        percentage = (high_float_count / len(regular_tasks)) * 100
        passed = percentage <= 5.0
        
        return self.format_result(passed, f"{percentage:.1f}%", failed_tasks)