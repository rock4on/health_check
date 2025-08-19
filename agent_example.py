"""Example usage of DCMA agent with OpenAI."""
import os
from dcma_healthcheck.agents.dcma_agent import DCMAAgent


def main():
    """Example of using the DCMA agent."""
    # Set environment variables (in real usage, set these in your environment)
    # os.environ['OPENAI_API_KEY'] = 'your-api-key-here'
    # os.environ['OPENAI_BASE_URL'] = 'https://api.openai.com/v1'  # Optional
    
    try:
        # Initialize the agent
        agent = DCMAAgent()
        
        # Analyze schedule with LLM interpretation
        print("Running DCMA analysis with LLM interpretation...")
        result = agent.analyze_with_llm('sample_schedule.csv')
        
        # Print structured results
        print(f"\n=== DCMA Analysis Results ===")
        print(f"Executive Summary: {result.executive_summary}")
        print(f"Overall Health Score: {result.overall_health_score}")
        print(f"Checks: {result.passed_checks}/{result.total_checks} passed")
        print(f"Risk Assessment: {result.risk_assessment}")
        
        print(f"\n=== Recommendations ===")
        for rec in result.recommendations:
            print(f"Point {rec.point_number}: {rec.point_name} - {rec.status}")
            if rec.status == "FAIL":
                print(f"  Priority: {rec.priority}")
                print(f"  Recommendation: {rec.recommendation}")
        
        print(f"\n=== Implementation Plan ===")
        for i, step in enumerate(result.implementation_plan, 1):
            print(f"{i}. {step}")
            
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set OPENAI_API_KEY environment variable")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()