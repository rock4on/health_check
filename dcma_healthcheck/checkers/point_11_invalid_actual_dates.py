"""DCMA Point 11: Invalid Actual Dates checker."""
from typing import List, Dict, Any
from datetime import datetime
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point11InvalidActualDates(BaseChecker):
    """Check that no actual dates are in the future."""
    
    def __init__(self):
        super().__init__(
            point_number=11,
            description="Invalid Actual Dates",
            threshold="0",
            recommendation="Correct future actual dates to reflect only completed work as of the current data date."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check for invalid actual dates (actual dates in the future)."""
        # Using current date as data date
        data_date = datetime.now().date()
        failed_tasks = []
        invalid_count = 0
        
        for task in schedule_lines:
            # Check actual start date
            if task.actual_start and task.actual_start.date() > data_date:
                invalid_count += 1
                failed_tasks.append(f"{task.unique_id}: {task.task_name} (actual start: {task.actual_start.strftime('%m/%d/%y')})")
            
            # Check actual finish date
            if task.actual_finish and task.actual_finish.date() > data_date:
                invalid_count += 1
                failed_tasks.append(f"{task.unique_id}: {task.task_name} (actual finish: {task.actual_finish.strftime('%m/%d/%y')})")
        
        passed = invalid_count == 0
        return self.format_result(passed, str(invalid_count), failed_tasks)