"""Simple data model for schedule line."""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class ScheduleLine:
    """Represents a single line in the project schedule."""
    unique_id: str
    id: str
    wbs_std: str
    wbs: str
    task_name: str
    percent_complete: float
    status: str
    start_date: Optional[datetime]
    finish_date: Optional[datetime]
    actual_start: Optional[datetime]
    actual_finish: Optional[datetime]
    duration: float
    actual_duration: float
    predecessors: List[str]
    successors: List[str]
    unique_id_predecessors: List[str]
    unique_id_successors: List[str]
    constraint_type: str
    constraint_date: Optional[datetime]
    free_slack: float
    total_slack: float
    critical: bool
    
    @classmethod
    def from_csv_line(cls, line: str) -> 'ScheduleLine':
        """Create ScheduleLine from CSV line."""
        parts = line.strip().split('\t')  # Tab-separated
        
        if len(parts) < 21:
            raise ValueError(f"Invalid CSV line format. Expected 21+ fields, got {len(parts)}")
        
        # Pad with empty strings if missing fields
        while len(parts) < 22:
            parts.append('')
    
    @classmethod
    def from_csv_with_headers(cls, data_dict: dict) -> 'ScheduleLine':
        """Create ScheduleLine from dictionary with headers."""
        # Parse dates with new format (e.g., "Tue 2/1/22")
        def parse_date(date_str: str) -> Optional[datetime]:
            if not date_str or date_str.upper() == 'NA':
                return None
            try:
                # Try different date formats
                if '/' in date_str:
                    # Format: "Tue 2/1/22" or "2/1/22"
                    date_part = date_str.split()[-1] if ' ' in date_str else date_str
                    return datetime.strptime(date_part, '%m/%d/%y')
                return None
            except ValueError:
                return None
        
        # Parse duration (e.g., "779.88 days" -> 779.88)
        def parse_duration(duration_str: str) -> float:
            if not duration_str or duration_str.upper() == 'NA':
                return 0.0
            try:
                return float(duration_str.split()[0])  # Extract number before "days"
            except (ValueError, IndexError):
                return 0.0
        
        # Parse percentage (e.g., "87%" -> 87.0)
        def parse_percentage(pct_str: str) -> float:
            if not pct_str or pct_str.upper() == 'NA':
                return 0.0
            try:
                return float(pct_str.rstrip('%'))
            except ValueError:
                return 0.0
        
        # Parse predecessors/successors (comma-separated)
        def parse_relationships(rel_str: str) -> List[str]:
            if not rel_str or rel_str.upper() == 'NA':
                return []
            return [x.strip() for x in rel_str.split(',') if x.strip()]
        
        return cls(
            unique_id=data_dict.get('Unique ID', ''),
            id=data_dict.get('ID', ''),
            wbs_std=data_dict.get('WBS STD', ''),
            wbs=data_dict.get('WBS', ''),
            task_name=data_dict.get('Task Name', ''),
            percent_complete=parse_percentage(data_dict.get('% Complete', '0%')),
            status=data_dict.get('Status', ''),
            start_date=parse_date(data_dict.get('Start', '')),
            finish_date=parse_date(data_dict.get('Finish', '')),
            actual_start=parse_date(data_dict.get('Actual Start', '')),
            actual_finish=parse_date(data_dict.get('Actual Finish', '')),
            duration=parse_duration(data_dict.get('Duration', '0 days')),
            actual_duration=parse_duration(data_dict.get('Actual Duration', '0 days')),
            predecessors=parse_relationships(data_dict.get('Predecessors', '')),
            successors=parse_relationships(data_dict.get('Successors', '')),
            unique_id_predecessors=parse_relationships(data_dict.get('Unique ID Predecessors', '')),
            unique_id_successors=parse_relationships(data_dict.get('Unique ID Successors', '')),
            constraint_type=data_dict.get('Constraint Type', ''),
            constraint_date=parse_date(data_dict.get('Constraint Date', '')),
            free_slack=parse_duration(data_dict.get('Free Slack', '0 days')),
            total_slack=parse_duration(data_dict.get('Total Slack', '0 days')),
            critical=data_dict.get('Critical', '').upper() == 'YES'
        )
        
        # Parse dates with new format (e.g., "Tue 2/1/22")
        def parse_date(date_str: str) -> Optional[datetime]:
            if not date_str or date_str.upper() == 'NA':
                return None
            try:
                # Try different date formats
                if '/' in date_str:
                    # Format: "Tue 2/1/22" or "2/1/22"
                    date_part = date_str.split()[-1] if ' ' in date_str else date_str
                    return datetime.strptime(date_part, '%m/%d/%y')
                return None
            except ValueError:
                return None
        
        # Parse duration (e.g., "779.88 days" -> 779.88)
        def parse_duration(duration_str: str) -> float:
            if not duration_str or duration_str.upper() == 'NA':
                return 0.0
            try:
                return float(duration_str.split()[0])  # Extract number before "days"
            except (ValueError, IndexError):
                return 0.0
        
        # Parse percentage (e.g., "87%" -> 87.0)
        def parse_percentage(pct_str: str) -> float:
            if not pct_str or pct_str.upper() == 'NA':
                return 0.0
            try:
                return float(pct_str.rstrip('%'))
            except ValueError:
                return 0.0
        
        # Parse predecessors/successors (comma-separated)
        def parse_relationships(rel_str: str) -> List[str]:
            if not rel_str or rel_str.upper() == 'NA':
                return []
            return [x.strip() for x in rel_str.split(',') if x.strip()]
        
        return cls(
            unique_id=parts[0],
            id=parts[1],
            wbs_std=parts[2],
            wbs=parts[3],
            task_name=parts[4],
            percent_complete=parse_percentage(parts[5]),
            status=parts[6],
            start_date=parse_date(parts[7]),
            finish_date=parse_date(parts[8]),
            actual_start=parse_date(parts[9]),
            actual_finish=parse_date(parts[10]),
            duration=parse_duration(parts[11]),
            actual_duration=parse_duration(parts[12]),
            predecessors=parse_relationships(parts[13]),
            successors=parse_relationships(parts[14]),
            unique_id_predecessors=parse_relationships(parts[15]),
            unique_id_successors=parse_relationships(parts[16]),
            constraint_type=parts[17],
            constraint_date=parse_date(parts[18]),
            free_slack=parse_duration(parts[19]),
            total_slack=parse_duration(parts[20]),
            critical=parts[21].upper() == 'YES'
        )