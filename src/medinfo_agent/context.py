from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MedinfoContext:
    search_result_ids: Optional[List[str]] = None
