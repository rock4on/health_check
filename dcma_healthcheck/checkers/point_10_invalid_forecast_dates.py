"""DCMA Point 10: Invalid Forecast Dates checker."""
from typing import List, Dict, Any
from datetime import datetime
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point10InvalidForecastDates(BaseChecker):
    """Check that no forecast dates are earlier than data date."""
    
    def __init__(self):
        super().__init__(
            point_number=10,
            description="Invalid Forecast Dates",
            threshold="0",
            recommendation="Update planned dates to ensure no forecasted work precedes the current data date."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check for invalid forecast dates (planned dates before data date for incomplete work)."""
        # Using current date as data date
        data_date = datetime.now().date()
        failed_tasks = []
        invalid_count = 0
        
        for task in schedule_lines:
            # Check incomplete tasks with planned dates in the past
            if task.status not in ['Complete', 'Completed']:
                # Check planned start date
                if (task.start_date and task.start_date.date() < data_date and 
                    not task.actual_start):
                    invalid_count += 1
                    failed_tasks.append(f"{task.unique_id}: {task.task_name} (planned start: {task.start_date.strftime('%m/%d/%y')})")
                
                # Check planned finish date
                if (task.finish_date and task.finish_date.date() < data_date and 
                    not task.actual_finish):
                    invalid_count += 1
                    failed_tasks.append(f"{task.unique_id}: {task.task_name} (planned finish: {task.finish_date.strftime('%m/%d/%y')})")
        
        passed = invalid_count == 0
        return self.format_result(passed, str(invalid_count), failed_tasks)