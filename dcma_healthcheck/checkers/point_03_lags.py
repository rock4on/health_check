"""DCMA Point 3: Lags checker."""
from typing import List, Dict, Any
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point03Lags(BaseChecker):
    """Check that ≤5% of dependencies have positive lag."""
    
    def __init__(self):
        super().__init__(
            point_number=3,
            description="Lags",
            threshold="≤ 5%",
            recommendation="Review and eliminate lag where feasible, replacing it with additional tasks or more explicit dependencies to enhance schedule transparency and logical clarity."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check for excessive positive lag (>5% of relationships)."""
        if not schedule_lines:
            return self.format_result(True, "0%", [])
        
        total_relationships = 0
        positive_lag_count = 0
        failed_tasks = []
        
        for task in schedule_lines:
            # Count all predecessor relationships
            total_relationships += len(task.predecessors)
            
            # Check for positive lag indicators (e.g., "76FS+5 days")
            for pred in task.predecessors:
                if '+' in pred and ('FS+' in pred or 'SS+' in pred or 'FF+' in pred or 'SF+' in pred):
                    positive_lag_count += 1
                    failed_tasks.append(f"{task.unique_id}: {task.task_name} (predecessor: {pred})")
        
        if total_relationships == 0:
            return self.format_result(True, "0%", [])
        
        percentage = (positive_lag_count / total_relationships) * 100
        passed = percentage <= 5.0
        
        return self.format_result(passed, f"{percentage:.1f}%", failed_tasks)