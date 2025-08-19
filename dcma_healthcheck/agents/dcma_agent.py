"""OpenAI-based agent for DCMA schedule analysis."""
from typing import Dict, Any
from openai import OpenAI
from ..analyzers.dcma_analyzer import DCMAAnalyzer
from ..config.openai_config import OpenAIConfig
from ..prompts.dcma_prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT, INTERPRETATION_PROMPT
from ..models.dcma_models import DCMAAnalysisResponse


class DCMAAgent:
    """OpenAI agent wrapper for DCMA analysis."""
    
    def __init__(self):
        """Initialize the agent with OpenAI client."""
        self.config = OpenAIConfig()
        if not self.config.validate():
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(
            api_key=self.config.get_api_key(),
            base_url=self.config.get_base_url()
        )
        self.analyzer = DCMAAnalyzer()

    def analyze_schedule(self, csv_file_path: str) -> Dict[str, Any]:
        """Analyze schedule from CSV file."""
        try:
            results = self.analyzer.process_csv_file(csv_file_path)
            return results
        except Exception as e:
            return {"error": f"Failed to analyze schedule: {str(e)}"}

    def explain_dcma_point(self, point_number: int) -> Dict[str, Any]:
        """Explain a specific DCMA point."""
        explanations = {
            1: {
                "name": "Logic",
                "threshold": "≥95%",
                "description": "Ensures most activities have predecessors and successors (no open ends)",
                "recommendation": "Review the schedule and ensure that all activities (except start/milestone) have both predecessors and successors."
            },
            2: {
                "name": "Leads (Negative Lag)",
                "threshold": "0",
                "description": "Lead time (negative lag) should not be used as it can hide logic flaws",
                "recommendation": "Remove negative lags and replace with explicit task sequencing to show accurate logic."
            },
            3: {
                "name": "Lags",
                "threshold": "≤5%",
                "description": "Excessive lag can disrupt proper sequencing and control",
                "recommendation": "Review and eliminate lag where feasible, replacing it with additional tasks or more explicit dependencies."
            },
            4: {
                "name": "Relationship Types",
                "threshold": "≥90% FS",
                "description": "Ensures that at least 90% of activity relationships are Finish-to-Start (FS)",
                "recommendation": "Convert SS/FF dependencies to FS wherever practical to maintain clarity and sequencing discipline."
            },
            5: {
                "name": "Start-to-Finish Relations",
                "threshold": "0",
                "description": "Start-to-Finish dependencies are not recommended and should be avoided entirely",
                "recommendation": "Identify and eliminate SF dependencies, replacing them with FS or SS links as appropriate."
            },
            6: {
                "name": "Hard Constraints",
                "threshold": "≤5%",
                "description": "Limits use of constraints like 'Must Finish On' that override logic",
                "recommendation": "Replace hard constraints with flexible alternatives (e.g., 'As Late As Possible')."
            },
            7: {
                "name": "High Float",
                "threshold": "≤5%",
                "description": "Highlights overly flexible activities that may indicate poor logic",
                "recommendation": "Analyze tasks with high float for unnecessary delay or missing dependencies."
            },
            8: {
                "name": "Negative Float",
                "threshold": "0",
                "description": "Indicates the project is behind schedule or has unrealistic deadlines",
                "recommendation": "Re-sequence or adjust the schedule to eliminate negative float and align with project goals."
            },
            9: {
                "name": "High Duration",
                "threshold": "≤5%",
                "description": "Flags activities that are too long (+44 day duration) to manage effectively",
                "recommendation": "Break long-duration tasks into smaller, more manageable activities with logical dependencies."
            },
            10: {
                "name": "Invalid Forecast Dates",
                "threshold": "0",
                "description": "No forecast dates should be earlier than the data date",
                "recommendation": "Update planned dates to ensure no forecasted work precedes the current data date."
            },
            11: {
                "name": "Invalid Actual Dates",
                "threshold": "0",
                "description": "No actual dates should exist in the future",
                "recommendation": "Correct future actual dates to reflect only completed work as of the current data date."
            }
        }
        
        if point_number in explanations:
            return explanations[point_number]
        else:
            return {"error": f"Invalid DCMA point number: {point_number}. Must be 1-11."}

    def analyze_with_llm(self, csv_file_path: str) -> DCMAAnalysisResponse:
        """Analyze schedule and get LLM interpretation."""
        # First run the DCMA analysis
        analysis_results = self.analyze_schedule(csv_file_path)
        
        if "error" in analysis_results:
            raise ValueError(f"Analysis failed: {analysis_results['error']}")
        
        # Format results for LLM
        report = self.analyzer.generate_report(analysis_results)
        prompt = ANALYSIS_PROMPT.format(analysis_results=report)
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.config.model,
                messages=messages,
                response_format=DCMAAnalysisResponse,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            return response.choices[0].message.parsed
            
        except Exception as e:
            raise RuntimeError(f"Error communicating with OpenAI: {str(e)}")