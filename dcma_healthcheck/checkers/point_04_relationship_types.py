"""DCMA Point 4: Relationship Types checker."""
from typing import List, Dict, Any
from ..base_checker import BaseChecker
from ..models.schedule_data import ScheduleLine


class Point04RelationshipTypes(BaseChecker):
    """Check that ≥90% of relationships are Finish-to-Start (FS)."""
    
    def __init__(self):
        super().__init__(
            point_number=4,
            description="Relationship Types (SS/FF)",
            threshold="≥ 90% Finish-to-Start (FS)",
            recommendation="Convert SS/FF dependencies to FS wherever practical to maintain clarity and sequencing discipline."
        )
    
    def check(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Check that ≥90% of relationships are Finish-to-Start (FS)."""
        if not schedule_lines:
            return self.format_result(True, "100% FS", [])
        
        total_relationships = 0
        fs_relationships = 0
        non_fs_tasks = []
        
        for task in schedule_lines:
            for pred in task.predecessors:
                total_relationships += 1
                
                # Check relationship type in predecessor string
                if 'SS' in pred or 'FF' in pred or 'SF' in pred:
                    # Non-FS relationship found
                    relationship_type = 'SS' if 'SS' in pred else 'FF' if 'FF' in pred else 'SF'
                    non_fs_tasks.append(f"{task.unique_id}: {task.task_name} ({relationship_type} with {pred})")
                else:
                    # Assume FS if no other type specified
                    fs_relationships += 1
        
        if total_relationships == 0:
            return self.format_result(True, "100% FS", [])
        
        fs_percentage = (fs_relationships / total_relationships) * 100
        passed = fs_percentage >= 90.0
        
        return self.format_result(passed, f"{fs_percentage:.1f}% FS", non_fs_tasks)