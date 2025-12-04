"""
Data loading utilities for the agent system
"""
import pandas as pd
import os
from typing import Dict, Any

class DataLoader:
    """Load and manage scientific publication data"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.papers_df = None
        self.authors_df = None
        self.timeline_df = None
        self._load_data()
    
    def _load_data(self):
        """Load all CSV files"""
        try:
            papers_path = os.path.join(self.data_dir, "citation_nodes.csv")
            authors_path = os.path.join(self.data_dir, "author_nodes.csv")
            timeline_path = os.path.join(self.data_dir, "timeline.csv")
            
            if os.path.exists(papers_path):
                self.papers_df = pd.read_csv(papers_path)
                print(f"Loaded {len(self.papers_df)} papers")
            
            if os.path.exists(authors_path):
                self.authors_df = pd.read_csv(authors_path)
                print(f"Loaded {len(self.authors_df)} authors")
            
            if os.path.exists(timeline_path):
                self.timeline_df = pd.read_csv(timeline_path)
                print(f"Loaded timeline with {len(self.timeline_df)} years")
                
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary statistics of available data"""
        summary = {
            "papers_count": len(self.papers_df) if self.papers_df is not None else 0,
            "authors_count": len(self.authors_df) if self.authors_df is not None else 0,
            "year_range": None,
            "available_fields": []
        }
        
        if self.papers_df is not None and len(self.papers_df) > 0:
            summary["available_fields"] = list(self.papers_df.columns)
            if "year" in self.papers_df.columns:
                summary["year_range"] = [
                    int(self.papers_df["year"].min()),
                    int(self.papers_df["year"].max())
                ]
        
        return summary
    
    def query_papers(self, 
                     groupby: str = None,
                     measure: str = "count",
                     aggregation_field: str = None,
                     filters: Dict = None,
                     limit: int = None,
                     sort: str = "desc") -> pd.DataFrame:
        """
        Query papers data with aggregation
        
        Args:
            groupby: Field to group by (e.g., "year", "field")
            measure: Aggregation function ("count", "sum", "avg", "max", "min")
            aggregation_field: Field to aggregate (for sum, avg, max, min)
            filters: Dictionary of filters {field: value or condition}
            limit: Limit number of results
            sort: Sort order ("asc" or "desc")
        """
        if self.papers_df is None:
            return pd.DataFrame()
        
        df = self.papers_df.copy()
        
        # Apply filters
        if filters:
            for field, condition in filters.items():
                if field in df.columns:
                    if isinstance(condition, str) and condition.startswith(">="):
                        value = float(condition[2:])
                        df = df[df[field] >= value]
                    elif isinstance(condition, str) and condition.startswith("<="):
                        value = float(condition[2:])
                        df = df[df[field] <= value]
                    else:
                        df = df[df[field] == condition]
        
        # Group and aggregate
        if groupby and groupby in df.columns:
            if measure == "count":
                result = df.groupby(groupby).size().reset_index(name="count")
            elif measure in ["sum", "avg", "max", "min"] and aggregation_field:
                agg_func = {
                    "sum": "sum",
                    "avg": "mean", 
                    "max": "max",
                    "min": "min"
                }[measure]
                result = df.groupby(groupby)[aggregation_field].agg(agg_func).reset_index()
                result.columns = [groupby, "value"]
            else:
                result = df.groupby(groupby).size().reset_index(name="count")
        else:
            # No grouping, just return filtered data
            result = df
        
        # Sort
        if "count" in result.columns:
            result = result.sort_values("count", ascending=(sort == "asc"))
        elif "value" in result.columns:
            result = result.sort_values("value", ascending=(sort == "asc"))
        
        # Limit
        if limit:
            result = result.head(limit)
        
        return result
    
    def query_authors(self,
                      groupby: str = None,
                      measure: str = "count",
                      aggregation_field: str = None,
                      limit: int = None,
                      sort: str = "desc") -> pd.DataFrame:
        """Query authors data with aggregation"""
        if self.authors_df is None:
            return pd.DataFrame()
        
        df = self.authors_df.copy()
        
        if groupby and groupby in df.columns:
            if measure == "count":
                result = df.groupby(groupby).size().reset_index(name="count")
            else:
                result = df
        else:
            result = df
        
        # For top authors queries
        if aggregation_field and aggregation_field in df.columns:
            result = df[["name", aggregation_field]].rename(
                columns={aggregation_field: "value"}
            )
            result = result.sort_values("value", ascending=(sort == "asc"))
        
        if limit:
            result = result.head(limit)
        
        return result
    
    def get_timeline(self) -> pd.DataFrame:
        """Get timeline data"""
        if self.timeline_df is not None:
            return self.timeline_df
        elif self.papers_df is not None and "year" in self.papers_df.columns:
            # Generate timeline from papers
            timeline = self.papers_df.groupby("year").size().reset_index(name="paper_count")
            return timeline
        return pd.DataFrame()
