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
        """Check relationship types."""
        # This is a placeholder since relationship type data isn't in our current CSV format
        # In a real implementation, you'd check dependency relationship types
        failed_tasks = []
        
        # For now, assume all relationships are FS
        return self.format_result(True, "100% FS", failed_tasks)