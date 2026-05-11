class StrategyAgent:
    def __init__(self):
        self.name = "Strategy Generation Agent"

    def execute(self, business_data: dict, analysis_data: dict):
        """
        Generates business improvement strategy.
        """
        score = analysis_data.get("maturity_score", 0)
        category = business_data.get("category", "Business")
        
        if score < 40:
            strategy = f"Comprehensive Digital Foundation setup for {business_data['name']}. Focus on building a primary digital identity."
            actions = "1. Develop Responsive Website; 2. Setup Google Business Profile; 3. Initial Social Media Branding."
            impact = "Expected 200% increase in online discoverability and professional credibility."
        elif score < 70:
            strategy = f"Growth & Optimization Strategy for {business_data['name']}. Transition from basic presence to active lead generation."
            actions = "1. SEO Content Strategy; 2. Performance Marketing (Ads); 3. Lead Capture integration on Website."
            impact = "Expected 40% increase in monthly inbound inquiries."
        else:
            strategy = f"Digital Excellence & Automation for {business_data['name']}. Leverage existing presence for automated growth."
            actions = "1. CRM Integration; 2. Advanced Analytics; 3. Reputation Management Automation."
            impact = "Expected 25% improvement in client retention and operational efficiency."

        return {
            "recommended_strategy": strategy,
            "priority_actions": actions,
            "expected_impact": impact
        }
