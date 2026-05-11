class DigitalAnalysisAgent:
    def __init__(self):
        self.name = "Digital Presence Analysis Agent"

    def execute(self, business_data: dict):
        """
        Analyzes business digital maturity.
        """
        has_website = business_data.get("website") is not None
        social_count = len(business_data.get("social_presence", "").split(", ")) if business_data.get("social_presence") else 0
        
        # Simple scoring algorithm
        score = 0
        score += 40 if has_website else 10
        score += social_count * 15
        score = min(score, 100)

        strengths = []
        weaknesses = []
        missing_assets = []

        if has_website:
            strengths.append("Active Website Presence")
        else:
            weaknesses.append("No Official Website")
            missing_assets.append("Professional Website")

        if social_count > 1:
            strengths.append("Multi-channel Social Presence")
        elif social_count == 1:
            strengths.append("Basic Social Presence")
        else:
            weaknesses.append("Missing Social Media Presence")
            missing_assets.append("Social Media Profiles (IG, FB, LinkedIn)")

        if score < 50:
            weaknesses.append("Low Search Engine Visibility")
            missing_assets.append("SEO Optimization")

        return {
            "maturity_score": score,
            "strengths": ", ".join(strengths),
            "weaknesses": ", ".join(weaknesses),
            "missing_assets": ", ".join(missing_assets)
        }
