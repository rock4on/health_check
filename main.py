"""Main script to demonstrate DCMA schedule analysis."""
from dcma_healthcheck.analyzers.dcma_analyzer import DCMAAnalyzer


def main():
    """Run DCMA analysis on sample schedule."""
    analyzer = DCMAAnalyzer()
    
    # Analyze the sample schedule
    results = analyzer.process_csv_file('sample_schedule.csv')
    
    # Generate and print report
    report = analyzer.generate_report(results)
    print(report)


if __name__ == "__main__":
    main()