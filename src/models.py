from dataclasses import dataclass, field
from typing import Any, Dict, List
from pathlib import Path
from constants import DEFAULT_ANALYSIS, DEFAULT_RECOMMENDATIONS


@dataclass
class FileInsights:
    analysis: str = DEFAULT_ANALYSIS
    recommendations: str = DEFAULT_RECOMMENDATIONS


@dataclass
class CodeAnalysis:
    file_tree: Dict[str, Any]
    python_files: List[Path]
    total_files: int
    total_dirs: int
    ai_insights: Dict[str, FileInsights] = field(default_factory=dict)
