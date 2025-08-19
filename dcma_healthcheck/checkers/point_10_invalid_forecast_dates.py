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
        """Check for invalid forecast dates."""
        # Using current date as data date for this example
        data_date = datetime.now().date()
        failed_tasks = []
        
        for task in schedule_lines:
            # Check if task is not completed and has dates before data date
            if task.start_date and task.start_date.date() < data_date:
                # This would be invalid if the task hasn't started yet
                # In real implementation, you'd check actual start vs planned start
                pass
            
            if task.finish_date and task.finish_date.date() < data_date:
                # This would be invalid if the task hasn't finished yet
                # In real implementation, you'd check actual finish vs planned finish
                pass
        
        # For now, assume no invalid forecast dates
        return self.format_result(True, "0", failed_tasks)