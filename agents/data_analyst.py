"""
Data Analyst Agent - Executes data queries and performs analysis
"""
import pandas as pd
from typing import List, Dict, Any
from utils.data_loader import DataLoader

class DataAnalystAgent:
    """Agent that performs data analysis based on query plan"""
    
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
    
    def analyze(self, query_plan: dict) -> List[Dict[str, Any]]:
        """
        Execute data analysis based on query plan
        
        Args:
            query_plan: Structured query from QueryParserAgent
            
        Returns:
            List of dictionaries with analyzed data
        """
        try:
            intent = query_plan.get("intent", "count_by_field")
            entity = query_plan.get("entity", "papers")
            
            # Route to appropriate analysis method
            if intent == "count_by_field":
                result = self._count_by_field(query_plan, entity)
            elif intent == "top_ranking":
                result = self._top_ranking(query_plan, entity)
            elif intent == "trend_analysis":
                result = self._trend_analysis(query_plan, entity)
            elif intent == "distribution":
                result = self._distribution(query_plan, entity)
            elif intent == "comparison":
                result = self._comparison(query_plan, entity)
            else:
                result = self._count_by_field(query_plan, entity)
            
            print(f"Analysis complete: {len(result)} data points")
            return result
            
        except Exception as e:
            print(f"Error in data analysis: {e}")
            return []
    
    def _count_by_field(self, query_plan: dict, entity: str) -> List[Dict]:
        """Count entities grouped by a field"""
        groupby = query_plan.get("groupby", "year")
        filters = query_plan.get("filters", {})
        sort = query_plan.get("sort", "desc")
        
        if entity == "papers":
            df = self.data_loader.query_papers(
                groupby=groupby,
                measure="count",
                filters=filters,
                sort=sort,
                limit=50
            )
        else:
            df = self.data_loader.query_authors(
                groupby=groupby,
                measure="count",
                sort=sort,
                limit=50
            )
        
        # Convert to list of dicts
        if not df.empty:
            # Rename columns for consistency
            if groupby in df.columns and "count" in df.columns:
                df = df.rename(columns={groupby: "category", "count": "value"})
            return df.to_dict('records')
        return []
    
    def _top_ranking(self, query_plan: dict, entity: str) -> List[Dict]:
        """Get top N entities by some metric"""
        limit = query_plan.get("limit", 10)
        aggregation_field = query_plan.get("aggregation_field", "citations_count")
        sort = query_plan.get("sort", "desc")
        
        if entity == "papers":
            df = self.data_loader.papers_df
            if df is not None and aggregation_field in df.columns:
                # Get top papers
                df = df.nlargest(limit, aggregation_field)
                result = []
                for _, row in df.iterrows():
                    result.append({
                        "name": row.get("title", "Unknown")[:50] + "...",  # Truncate title
                        "value": float(row[aggregation_field])
                    })
                return result
        else:
            df = self.data_loader.query_authors(
                aggregation_field=aggregation_field,
                limit=limit,
                sort=sort
            )
            if not df.empty and "name" in df.columns and "value" in df.columns:
                return df.to_dict('records')
        
        return []
    
    def _trend_analysis(self, query_plan: dict, entity: str) -> List[Dict]:
        """Analyze trends over time"""
        groupby = query_plan.get("groupby", "year")
        filters = query_plan.get("filters", {})
        sort = "asc"  # Always ascending for time series
        
        if entity == "papers":
            df = self.data_loader.query_papers(
                groupby=groupby,
                measure="count",
                filters=filters,
                sort=sort,
                limit=50
            )
        else:
            df = self.data_loader.query_authors(
                groupby=groupby,
                measure="count",
                sort=sort,
                limit=50
            )
        
        if not df.empty:
            # Format for time series
            if groupby in df.columns and "count" in df.columns:
                df = df.rename(columns={groupby: "x", "count": "y"})
            return df.to_dict('records')
        return []
    
    def _distribution(self, query_plan: dict, entity: str) -> List[Dict]:
        """Analyze distribution of values"""
        aggregation_field = query_plan.get("aggregation_field", "citations_count")
        
        if entity == "papers":
            df = self.data_loader.papers_df
            if df is not None and aggregation_field in df.columns:
                # Create histogram bins
                values = df[aggregation_field].dropna()
                
                # Use pandas cut to create bins
                if len(values) > 0:
                    bins = min(20, len(values.unique()))
                    hist, bin_edges = pd.cut(values, bins=bins, retbins=True, duplicates='drop')
                    
                    # Count values in each bin
                    counts = hist.value_counts().sort_index()
                    
                    result = []
                    for interval, count in counts.items():
                        result.append({
                            "bin": f"{interval.left:.0f}-{interval.right:.0f}",
                            "count": int(count),
                            "min": float(interval.left),
                            "max": float(interval.right)
                        })
                    return result
        
        return []
    
    def _comparison(self, query_plan: dict, entity: str) -> List[Dict]:
        """Compare entities across categories"""
        # Similar to count_by_field but with multiple measures
        return self._count_by_field(query_plan, entity)
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for context"""
        return self.data_loader.get_data_summary()
