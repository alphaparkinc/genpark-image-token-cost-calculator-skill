"""Image Token Cost Calculator.
100% Python Standard Library.
"""

import math

class VisionTokenCostCalculator:
    """Calculates LLM vision token consumption and costs across models."""
    @staticmethod
    def calculate_openai_tokens(width: int, height: int, detail="high") -> dict:
        if detail == "low":
            return {"tokens": 85, "tiles": 1, "detail": "low", "estimated_cost_usd": round(85 * 0.000005, 6)}

        scale = min(1.0, 2048.0 / max(width, height))
        scaled_w = width * scale
        scaled_h = height * scale

        scale2 = 768.0 / min(scaled_w, scaled_h)
        scaled_w = int(scaled_w * scale2)
        scaled_h = int(scaled_h * scale2)

        tiles_x = math.ceil(scaled_w / 512.0)
        tiles_y = math.ceil(scaled_h / 512.0)
        total_tiles = tiles_x * tiles_y

        tokens = total_tiles * 170 + 85
        return {
            "tokens": tokens,
            "tiles": total_tiles,
            "tiles_x": tiles_x,
            "tiles_y": tiles_y,
            "scaled_width": scaled_w,
            "scaled_height": scaled_h,
            "detail": "high",
            "estimated_cost_usd": round(tokens * 0.000005, 6)
        }

    @staticmethod
    def calculate_anthropic_tokens(width: int, height: int) -> dict:
        tokens = int(math.ceil((width * height) / 750.0))
        tokens = min(tokens, 1600)
        return {"tokens": tokens, "provider": "anthropic", "estimated_cost_usd": round(tokens * 0.000003, 6)}
