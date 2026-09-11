from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ReportConfig:
    """Sökvägar som behövs för att skapa rapporten"""

    input_path: Path = Path("data/orders.csv")
    output_dir: Path = Path("/output")                      