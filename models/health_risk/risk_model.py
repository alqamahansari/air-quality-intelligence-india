class HealthRiskModel:

    def __init__(self):
        self.categories = [
            (0, 50, "Low"),
            (51, 100, "Moderate"),
            (101, 200, "Unhealthy for Sensitive Groups"),
            (201, 300, "Poor"),
            (301, 400, "Very Poor"),
            (401, 1000, "Severe"),
        ]

    def get_category(self, aqi):
        for lower, upper, label in self.categories:
            if lower <= aqi <= upper:
                return label
        return "Unknown"

    def get_risk_score(self, aqi):
        # Normalize AQI into 0–1 range
        max_aqi = 500
        return min(aqi / max_aqi, 1.0)

    def population_adjusted_risk(self, aqi, group="general"):
        base_score = self.get_risk_score(aqi)

        sensitivity_weights = {
            "general": 1.0,
            "children": 1.2,
            "elderly": 1.3,
            "asthma": 1.5,
        }

        weight = sensitivity_weights.get(group, 1.0)
        adjusted_score = min(base_score * weight, 1.0)

        return adjusted_score

    def advisory_message(self, category):
        messages = {
            "Low": "Air quality is satisfactory. Normal outdoor activity is safe.",
            "Moderate": "Sensitive individuals should consider reducing prolonged outdoor exertion.",
            "Unhealthy for Sensitive Groups": "Children, elderly, and respiratory patients should limit outdoor exposure.",
            "Poor": "Reduce outdoor activity. Consider wearing masks.",
            "Very Poor": "Avoid outdoor exposure. Use air purification indoors.",
            "Severe": "Stay indoors. Health alert issued for all populations."
        }

        return messages.get(category, "No advisory available.")

if __name__ == "__main__":
    model = HealthRiskModel()

    predicted_aqi = 245

    category = model.get_category(predicted_aqi)
    score = model.get_risk_score(predicted_aqi)
    asthma_risk = model.population_adjusted_risk(predicted_aqi, "asthma")
    advisory = model.advisory_message(category)

    print("AQI:", predicted_aqi)
    print("Category:", category)
    print("Risk Score:", round(score, 2))
    print("Asthma Risk Score:", round(asthma_risk, 2))
    print("Advisory:", advisory)