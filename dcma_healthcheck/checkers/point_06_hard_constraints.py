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
        """Check for hard constraints (≤5% of activities)."""
        if not schedule_lines:
            return self.format_result(True, "0%", [])
        
        # Filter out milestone tasks for this check
        regular_tasks = [
            task for task in schedule_lines 
            if task.wbs_std not in ['START', 'CMPLT', 'MLSTN']
        ]
        
        if not regular_tasks:
            return self.format_result(True, "0%", [])
        
        hard_constraint_count = 0
        failed_tasks = []
        
        # Check for hard constraints
        hard_constraint_types = [
            'Must Start On',
            'Must Finish On',
            'Start On',
            'Finish On'
        ]
        
        for task in regular_tasks:
            if task.constraint_type in hard_constraint_types:
                hard_constraint_count += 1
                failed_tasks.append(f"{task.unique_id}: {task.task_name} ({task.constraint_type})")
        
        percentage = (hard_constraint_count / len(regular_tasks)) * 100
        passed = percentage <= 5.0
        
        return self.format_result(passed, f"{percentage:.1f}%", failed_tasks)