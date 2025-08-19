"""DCMA Point 5: Start-to-Finish Relations checker."""
from typing import List, Dict, Any
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point05StartToFinish(BaseChecker):
    """Check that there are no Start-to-Finish dependencies."""
    
    def __init__(self):
        super().__init__(
            point_number=5,
            description="Start-to-Finish (SF) Relations",
            threshold="0",
            recommendation="Identify and eliminate SF dependencies, replacing them with FS or SS links as appropriate."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check for Start-to-Finish relationships."""
        sf_count = 0
        failed_tasks = []
        
        for task in schedule_lines:
            for pred in task.predecessors:
                if 'SF' in pred:
                    sf_count += 1
                    failed_tasks.append(f"{task.unique_id}: {task.task_name} (SF with {pred})")
        
        passed = sf_count == 0
        return self.format_result(passed, str(sf_count), failed_tasks)