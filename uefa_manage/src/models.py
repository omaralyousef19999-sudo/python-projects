"""
نماذج بسيطة للتعامل مع نتائج DB (CRUD helpers).
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from .database import get_conn


@dataclass
class Team:
    team_id: Optional[int]
    name: str
    country: Optional[str] = None
    ranking: Optional[int] = None
    group_name: Optional[str] = None


@dataclass
class Player:
    player_id: Optional[int]
    name: str
    position: Optional[str]
    age: Optional[int]
    team_id: Optional[int]


@dataclass
class Match:
    match_id: Optional[int]
    home_team: int
    away_team: int
    home_goals: int = 0
    away_goals: int = 0
    date: Optional[str] = None
    stage: Optional[str] = None
    stadium: Optional[str] = None