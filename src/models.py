from dataclasses import dataclass, field
from typing import Any, Dict, List
from pathlib import Path
from constants import DEFAULT_ANALYSIS, DEFAULT_RECOMMENDATIONS

@dataclass
class RankedRecommendation:
    text: str
    priority: str
    impact_score: int
    justification: str

@dataclass
class FileInsights:
    analysis: str = DEFAULT_ANALYSIS
    analysis_summary: str = ""
    ranked_recommendations: List[RankedRecommendation] = field(default_factory=list)
    recommendations: str = DEFAULT_RECOMMENDATIONS


@dataclass
class CodeAnalysis:
    file_tree: Dict[str, Any]
    python_files: List[Path]
    total_files: int
    total_dirs: int
    ai_insights: Dict[str, FileInsights] = field(default_factory=dict)

