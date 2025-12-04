"""
Visualization Generator Agent - Creates Vega-Lite specifications
"""
import json
import os
from typing import List, Dict, Any
from openai import OpenAI
from utils.prompts import VIZ_GENERATOR_PROMPT, SYSTEM_MESSAGE

class VizGeneratorAgent:
    """Agent that generates Vega-Lite specifications"""
    
    def __init__(self):
        api_key = os.environ.get("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable not set")
        # Qwen API is compatible with OpenAI interface
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model = "qwen-plus"  # or "qwen-turbo", "qwen-max"
    
    def generate(self, 
                 query_plan: dict, 
                 analyzed_data: List[Dict[str, Any]]) -> dict:
        """
        Generate Vega-Lite specification
        
        Args:
            query_plan: Original query plan
            analyzed_data: Data from DataAnalystAgent
            
        Returns:
            Dictionary with description and Vega-Lite spec
        """
        try:
            # If no data, return empty chart
            if not analyzed_data:
                return self._create_empty_chart("No data available for this query")
            
            # Use template-based generation for reliability
            # AI generation sometimes produces incorrect configurations
            intent = query_plan.get("intent", "count_by_field")

            print(f"⚡ Using template for {intent}")
            return self._create_template_chart(query_plan, analyzed_data)

        except Exception as e:
            print(f"Error generating visualization: {e}")
            return self._create_template_chart(query_plan, analyzed_data)

    def _create_template_chart(self,
                                query_plan: dict,
                                data: List[Dict]) -> dict:
        """Create chart using templates (fallback)"""
        intent = query_plan.get("intent", "count_by_field")

        if intent == "top_ranking":
            return self._create_bar_chart(data, horizontal=True)
        elif intent == "trend_analysis":
            return self._create_line_chart(data)
        elif intent == "distribution":
            return self._create_histogram(data)
        else:
            return self._create_bar_chart(data, horizontal=False)

    def _create_bar_chart(self, data: List[Dict], horizontal: bool = False) -> dict:
        """Create a bar chart"""
        # Detect field names from data
        if not data:
            return self._create_empty_chart("No data")

        first_row = data[0]
        keys = list(first_row.keys())

        # Try to find category and value fields
        category_field = keys[0] if len(keys) > 0 else "category"
        value_field = keys[1] if len(keys) > 1 else "value"

        # Format data to ensure categories are strings
        formatted_data = []
        for item in data:
            formatted_item = {}
            for key, value in item.items():
                if key == category_field:
                    # Convert to string for proper display
                    formatted_item[key] = str(value)
                else:
                    formatted_item[key] = value
            formatted_data.append(formatted_item)

        if horizontal:
            x_field, y_field = value_field, category_field
            x_type, y_type = "quantitative", "nominal"
        else:
            x_field, y_field = category_field, value_field
            x_type, y_type = "nominal", "quantitative"

        spec = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "data": {"values": formatted_data},
            "mark": {"type": "bar", "tooltip": True},
            "encoding": {
                "x": {
                    "field": x_field,
                    "type": x_type,
                    "title": x_field.replace("_", " ").title(),
                    "axis": {
                        "labelAngle": -45 if not horizontal else 0,
                        "labelOverlap": False,  # Show all labels
                        "labelPadding": 10
                    }
                },
                "y": {
                    "field": y_field,
                    "type": y_type,
                    "title": y_field.replace("_", " ").title(),
                    "sort": "-x" if horizontal else None
                },
                "color": {
                    "field": y_field if horizontal else x_field,
                    "type": "nominal",
                    "legend": None
                },
                "tooltip": [
                    {"field": category_field, "type": "nominal", "title": category_field.replace("_", " ").title()},
                    {"field": value_field, "type": "quantitative", "title": value_field.replace("_", " ").title()}
                ]
            },
            "config": {
                "view": {"stroke": None},
                "axis": {
                    "labelFontSize": 12,
                    "titleFontSize": 14
                }
            },
            "width": 600,
            "height": 400
        }

        return {
            "description": f"Bar chart showing {category_field} by {value_field}",
            "spec": spec
        }

    def _create_line_chart(self, data: List[Dict]) -> dict:
        """Create a line chart for time series"""
        if not data:
            return self._create_empty_chart("No data")

        first_row = data[0]
        keys = list(first_row.keys())

        x_field = keys[0] if len(keys) > 0 else "x"
        y_field = keys[1] if len(keys) > 1 else "y"

        # Ensure x values are properly formatted as strings
        # This fixes the issue where years might be interpreted incorrectly
        formatted_data = []
        for item in data:
            formatted_item = {}
            for key, value in item.items():
                if key == x_field:
                    # Convert to string to ensure proper display
                    formatted_item[key] = str(value)
                else:
                    formatted_item[key] = value
            formatted_data.append(formatted_item)

        spec = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "data": {"values": formatted_data},
            "mark": {
                "type": "line",
                "point": True,
                "tooltip": True
            },
            "encoding": {
                "x": {
                    "field": x_field,
                    "type": "nominal",
                    "title": x_field.replace("_", " ").title(),
                    "sort": None,  # Preserve original order
                    "axis": {
                        "labelAngle": 0,  # Keep labels horizontal
                        "labelOverlap": False,  # Show all labels
                        "labelPadding": 10  # Add padding
                    }
                },
                "y": {
                    "field": y_field,
                    "type": "quantitative",
                    "title": y_field.replace("_", " ").title()
                },
                "tooltip": [
                    {"field": x_field, "type": "nominal", "title": x_field.replace("_", " ").title()},
                    {"field": y_field, "type": "quantitative", "title": y_field.replace("_", " ").title()}
                ]
            },
            "config": {
                "view": {"stroke": None},
                "axis": {
                    "labelFontSize": 12,
                    "titleFontSize": 14
                }
            },
            "width": 600,
            "height": 400
        }

        return {
            "description": f"Trend of {y_field} over {x_field}",
            "spec": spec
        }

    def _create_histogram(self, data: List[Dict]) -> dict:
        """Create a histogram"""
        if not data:
            return self._create_empty_chart("No data")

        spec = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "data": {"values": data},
            "mark": {"type": "bar", "tooltip": True},
            "encoding": {
                "x": {
                    "field": "bin",
                    "type": "nominal",
                    "title": "Range"
                },
                "y": {
                    "field": "count",
                    "type": "quantitative",
                    "title": "Count"
                },
                "tooltip": [
                    {"field": "bin", "type": "nominal"},
                    {"field": "count", "type": "quantitative"}
                ]
            },
            "config": {
                "view": {"stroke": None},
                "axis": {"labelAngle": -45}
            },
            "width": 600,
            "height": 400
        }

        return {
            "description": "Distribution histogram",
            "spec": spec
        }

    def _create_empty_chart(self, message: str) -> dict:
        """Create empty chart with message"""
        return {
            "description": message,
            "spec": {
                "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                "data": {"values": []},
                "mark": "text",
                "encoding": {
                    "text": {"value": message}
                },
                "width": 600,
                "height": 400
            }
        }