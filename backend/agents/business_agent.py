import random

class BusinessDiscoveryAgent:
    def __init__(self):
        self.name = "Business Discovery Agent"

    def execute(self, name: str, category: str, location: str):
        """
        Simulates discovering business details.
        In a real scenario, this would use Google Maps API or SerpApi.
        """
        # Mocking discovery logic
        website = f"https://www.{name.lower().replace(' ', '')}.com"
        socials = ["Instagram", "Facebook", "LinkedIn"]
        random.shuffle(socials)
        
        return {
            "name": name,
            "category": category,
            "location": location,
            "website": website if random.random() > 0.3 else None,
            "social_presence": ", ".join(socials[:random.randint(0, 3)]),
            "contact_info": f"info@{name.lower().replace(' ', '')}.com"
        }
