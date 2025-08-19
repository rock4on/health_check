"""DCMA Point 1: Logic checker."""
from typing import List, Dict, Any
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point01Logic(BaseChecker):
    """Check that ≥95% of activities have predecessors and successors."""
    
    def __init__(self):
        super().__init__(
            point_number=1,
            description="Logic",
            threshold="≥ 95%",
            recommendation="Review the schedule and ensure that all activities (except start/milestone) have both predecessors and successors."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check logic connectivity."""
        if not schedule_lines:
            return self.format_result(True, "100%", [])
            
        # Filter out start and milestone tasks
        regular_tasks = [
            line for line in schedule_lines 
            if line.wbs_std not in ['START', 'CMPLT', 'MLSTN']
        ]
        
        if not regular_tasks:
            return self.format_result(True, "100%", [])
            
        # Count tasks with proper logic
        tasks_with_logic = 0
        failed_tasks = []
        
        for task in regular_tasks:
            has_predecessors = bool(task.predecessors and task.predecessors != [''])
            has_successors = bool(task.successors and task.successors != [''])
            
            if has_predecessors and has_successors:
                tasks_with_logic += 1
            else:
                failed_tasks.append(f"{task.unique_id}: {task.task_name}")
        
        percentage = (tasks_with_logic / len(regular_tasks)) * 100
        passed = percentage >= 95.0
        
        return self.format_result(passed, f"{percentage:.1f}%", failed_tasks)