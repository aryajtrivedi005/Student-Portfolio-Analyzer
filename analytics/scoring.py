"""
Deterministic Scoring Utilities for Student360 AI
"""

def clamp(val: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    return max(min_val, min(max_val, float(val)))

def normalize_cgpa(cgpa: float) -> float:
    # 10.0 scale -> 100% scale
    return clamp((cgpa / 10.0) * 100.0)

def normalize_score(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    if max_val == min_val:
        return 100.0
    scaled = ((value - min_val) / (max_val - min_val)) * 100.0
    return clamp(scaled)
