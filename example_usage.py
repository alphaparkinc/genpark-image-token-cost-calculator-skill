from client import VisionTokenCostCalculator

cost = VisionTokenCostCalculator.calculate_openai_tokens(1920, 1080, "high")
print("Vision Token Cost breakdown:\n", cost)
