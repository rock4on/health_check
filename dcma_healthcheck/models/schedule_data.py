"""Simple data model for schedule line."""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class ScheduleLine:
    """Represents a single line in the project schedule."""
    unique_id: str
    wbs_code: str
    wbs: str
    task_name: str
    start_date: Optional[datetime]
    finish_date: Optional[datetime] 
    duration: float
    predecessors: List[str]
    successors: List[str]
    
    @classmethod
    def from_csv_line(cls, line: str) -> 'ScheduleLine':
        """Create ScheduleLine from CSV line."""
        parts = line.strip().split(',')
        
        # Parse dates
        start_date = None
        finish_date = None
        if parts[4]:
            start_date = datetime.strptime(parts[4], '%Y-%m-%d')
        if parts[5]:
            finish_date = datetime.strptime(parts[5], '%Y-%m-%d')
            
        # Parse predecessors and successors
        predecessors = parts[7].split(';') if parts[7] else []
        successors = parts[8].split(';') if len(parts) > 8 and parts[8] else []
        
        return cls(
            unique_id=parts[0],
            wbs_code=parts[1], 
            wbs=parts[2],
            task_name=parts[3],
            start_date=start_date,
            finish_date=finish_date,
            duration=float(parts[6]) if parts[6] else 0.0,
            predecessors=predecessors,
            successors=successors
        )