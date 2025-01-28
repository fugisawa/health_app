from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any
import pandas as pd

@dataclass
class BaseProtocol(ABC):
    """Abstract base class for all health protocols"""
    name: str
    description: str
    
    @abstractmethod
    def to_dataframe(self) -> Dict[str, pd.DataFrame]:
        """Convert protocol data to pandas DataFrame(s)"""
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate protocol data"""
        pass
    
    @abstractmethod
    def save_to_csv(self, output_dir: str) -> None:
        """Save protocol data to CSV files"""
        pass 