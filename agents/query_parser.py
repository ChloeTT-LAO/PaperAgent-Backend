import json
import os
from openai import OpenAI
from utils.prompts import QUERY_PARSER_PROMPT, SYSTEM_MESSAGE

class QueryParserAgent:
    """Agent that parses natural language queries into structured format"""
    
    def __init__(self):
        api_key = os.environ.get("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable not set")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model = "qwen-plus"  # or "qwen-turbo", "qwen-max"
    
    def parse(self, query: str) -> dict:
        # Format prompt
        prompt = QUERY_PARSER_PROMPT.format(query=query)

        # Call Qwen API using OpenAI-compatible interface
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Extract response
        response_text = response.choices[0].message.content.strip()

        # Clean response (remove markdown code blocks if present)
        if response_text.startswith("```json"):
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()

        # Parse JSON
        query_plan = json.loads(response_text)

        # Validate required fields
        required_fields = ["intent", "entity"]
        for field in required_fields:
            if field not in query_plan:
                query_plan[field] = self._infer_field(field, query)

        # Set defaults
        query_plan.setdefault("measure", "count")
        query_plan.setdefault("filters", {})
        query_plan.setdefault("sort", "desc")

        print(f"Query parsed: {query_plan}")
        return query_plan
    
    def _infer_field(self, field: str, query: str) -> str:
        """Infer missing field from query text"""
        query_lower = query.lower()
        
        if field == "intent":
            if "top" in query_lower or "most" in query_lower:
                return "top_ranking"
            elif "trend" in query_lower or "over time" in query_lower:
                return "trend_analysis"
            elif "distribution" in query_lower:
                return "distribution"
            else:
                return "count_by_field"
        
        elif field == "entity":
            if "author" in query_lower:
                return "authors"
            else:
                return "papers"
        
        return ""
    
    def _get_default_plan(self, query: str) -> dict:
        """Return a safe default query plan"""
        return {
            "intent": "count_by_field",
            "entity": "papers",
            "groupby": "year",
            "measure": "count",
            "filters": {},
            "sort": "asc",
            "original_query": query
        }
