from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import pandas as pd

@dataclass
class Protocol:
    """Base class for all health protocols"""
    name: str
    description: str
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert protocol data to pandas DataFrame"""
        raise NotImplementedError
    
    def validate(self) -> bool:
        """Validate protocol data"""
        raise NotImplementedError

@dataclass
class LLLTProtocol(Protocol):
    """LLLT (Low-Level Light Therapy) protocol implementation"""
    daily_schedule: List[Dict[str, Any]]
    supplement_schedule: List[Dict[str, Any]]
    
    def to_dataframe(self) -> Dict[str, pd.DataFrame]:
        """Convert LLLT data to DataFrames"""
        daily_df = pd.DataFrame(self.daily_schedule)
        supplement_df = pd.DataFrame(self.supplement_schedule)
        
        return {
            'daily': daily_df,
            'supplements': supplement_df
        }
    
    def validate(self) -> bool:
        """Validate LLLT protocol data"""
        required_daily_fields = ['Days', 'Day Type', 'Session']
        required_supplement_fields = ['Time', 'Supplements', 'Purpose']
        
        return all(all(field in entry for field in required_daily_fields) 
                  for entry in self.daily_schedule) and \
               all(all(field in entry for field in required_supplement_fields) 
                   for entry in self.supplement_schedule)

@dataclass
class MobilityProtocol(Protocol):
    """Mobility protocol implementation"""
    phases: Dict[str, List[List[str]]]
    phase_details: Dict[str, Dict[str, str]]
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert mobility data to DataFrame"""
        dfs = []
        for phase_name, exercises in self.phases.items():
            df = pd.DataFrame(exercises, 
                            columns=['Exercise', 'Sets/Reps/Duration', 'Equipment', 'Key Notes'])
            df.insert(0, 'Phase', self.phase_details[phase_name]['name'])
            df.insert(1, 'Session', 'Morning')
            dfs.append(df)
        
        return pd.concat(dfs).reset_index(drop=True) 