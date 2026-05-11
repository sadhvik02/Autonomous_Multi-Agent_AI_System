class ProposalAgent:
    def __init__(self):
        self.name = "Proposal Generation Agent"

    def execute(self, business_data: dict, analysis_data: dict, strategy_data: dict):
        """
        Generates a client-facing proposal.
        """
        name = business_data.get("name")
        score = analysis_data.get("maturity_score")
        
        proposal_text = f"""
# Digital Transformation Proposal for {name}

## Executive Summary
After analyzing your current digital footprint (Score: {score}/100), we have identified significant opportunities for growth in the {business_data['category']} sector.

## Identified Problem
Your business currently faces challenges with {analysis_data['weaknesses'].lower()}. This limits your ability to capture market share from competitors who are more digitally active.

## Suggested Solution
{strategy_data['recommended_strategy']}

## Key Deliverables
{strategy_data['priority_actions']}

## Expected ROI
{strategy_data['expected_impact']}
        """

        return {
            "proposal_text": proposal_text.strip(),
            "timeline": "4 - 8 Weeks",
            "estimated_cost": "$2,500 - $7,000",
            "expected_roi": "3x - 5x within 12 months"
        }
