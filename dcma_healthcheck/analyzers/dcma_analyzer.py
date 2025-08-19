"""Main DCMA analyzer that runs all checks."""
from typing import List, Dict, Any
from ..models.schedule_data import ScheduleLine
from ..checkers.point_01_logic import Point01Logic
from ..checkers.point_02_leads import Point02Leads
from ..checkers.point_03_lags import Point03Lags
from ..checkers.point_04_relationship_types import Point04RelationshipTypes
from ..checkers.point_05_start_to_finish import Point05StartToFinish
from ..checkers.point_06_hard_constraints import Point06HardConstraints
from ..checkers.point_07_high_float import Point07HighFloat
from ..checkers.point_08_negative_float import Point08NegativeFloat
from ..checkers.point_09_high_duration import Point09HighDuration
from ..checkers.point_10_invalid_forecast_dates import Point10InvalidForecastDates
from ..checkers.point_11_invalid_actual_dates import Point11InvalidActualDates


class DCMAAnalyzer:
    """Main analyzer that orchestrates all DCMA checks."""
    
    def __init__(self):
        """Initialize all checkers."""
        self.checkers = [
            Point01Logic(),
            Point02Leads(),
            Point03Lags(),
            Point04RelationshipTypes(),
            Point05StartToFinish(),
            Point06HardConstraints(),
            Point07HighFloat(),
            Point08NegativeFloat(),
            Point09HighDuration(),
            Point10InvalidForecastDates(),
            Point11InvalidActualDates(),
        ]
    
    def analyze_schedule(self, schedule_lines: List[ScheduleLine]) -> Dict[str, Any]:
        """Run all DCMA checks on the schedule."""
        results = []
        
        for checker in self.checkers:
            result = checker.check(schedule_lines)
            results.append(result)
        
        # Calculate summary
        total_checks = len(results)
        passed_checks = sum(1 for r in results if r['passed'])
        
        return {
            'summary': {
                'total_checks': total_checks,
                'passed_checks': passed_checks,
                'failed_checks': total_checks - passed_checks,
                'overall_pass_rate': f"{(passed_checks / total_checks) * 100:.1f}%" if total_checks > 0 else "0%"
            },
            'results': results
        }
    
    def process_csv_file(self, file_path: str, has_headers: bool = True) -> Dict[str, Any]:
        """Process a CSV file and analyze it."""
        schedule_lines = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                if has_headers and lines:
                    # Parse with headers
                    headers = [h.strip() for h in lines[0].split('\t')]
                    
                    for line_num, line in enumerate(lines[1:], 2):
                        if line.strip():
                            try:
                                values = [v.strip() for v in line.split('\t')]
                                # Create dictionary from headers and values
                                data_dict = dict(zip(headers, values))
                                schedule_line = ScheduleLine.from_csv_with_headers(data_dict)
                                schedule_lines.append(schedule_line)
                            except Exception as e:
                                print(f"Error parsing line {line_num}: {e}")
                else:
                    # Parse without headers (old method)
                    for line_num, line in enumerate(lines, 1):
                        if line.strip():
                            try:
                                schedule_line = ScheduleLine.from_csv_line(line)
                                schedule_lines.append(schedule_line)
                            except Exception as e:
                                print(f"Error parsing line {line_num}: {e}")
                                
        except FileNotFoundError:
            return {'error': f"File not found: {file_path}"}
        
        return self.analyze_schedule(schedule_lines)
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a formatted report."""
        if 'error' in analysis_results:
            return f"Error: {analysis_results['error']}"
        
        report = []
        report.append("DCMA 11-Point Schedule Quality Check Report")
        report.append("=" * 50)
        
        # Summary
        summary = analysis_results['summary']
        report.append(f"Overall Results: {summary['passed_checks']}/{summary['total_checks']} checks passed ({summary['overall_pass_rate']})")
        report.append("")
        
        # Individual results
        for result in analysis_results['results']:
            status = "PASS" if result['passed'] else "FAIL"
            report.append(f"Point {result['point']}: {result['description']} - {status}")
            report.append(f"  Threshold: {result['threshold']}")
            report.append(f"  Actual: {result['value']}")
            
            if not result['passed']:
                report.append(f"  Recommendation: {result['recommendation']}")
                if result['failed_tasks']:
                    report.append("  Failed Tasks:")
                    for task in result['failed_tasks']:
                        report.append(f"    - {task}")
            report.append("")
        
        return "\n".join(report)