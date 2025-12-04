from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from agents.query_parser import QueryParserAgent
from agents.data_analyst import DataAnalystAgent
from agents.viz_generator import VizGeneratorAgent
from utils.data_loader import DataLoader

# Load environment variables
DASHSCOPE_API_KEY = 'sk-72f878b1abab481f822d53f54686e874'
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
print("Initializing system...")
try:
    data_loader = DataLoader(data_dir="./data")
    query_parser = QueryParserAgent()
    data_analyst = DataAnalystAgent(data_loader)
    viz_generator = VizGeneratorAgent()
    print("System initialized successfully!")
except Exception as e:
    print(f"Initialization error: {e}")
    data_loader = None
    query_parser = None
    data_analyst = None
    viz_generator = None

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "agents": {
            "query_parser": query_parser is not None,
            "data_analyst": data_analyst is not None,
            "viz_generator": viz_generator is not None
        },
        "data": {
            "papers_loaded": len(data_loader.papers_df) if data_loader and data_loader.papers_df is not None else 0,
            "authors_loaded": len(data_loader.authors_df) if data_loader and data_loader.authors_df is not None else 0
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint - orchestrates all agents
    
    Request body:
    {
        "query": "Show me the number of papers by year"
    }
    
    Response:
    {
        "query": "original query",
        "query_plan": {...},
        "data": [...],
        "visualization": {...},
        "explanation": "..."
    }
    """
    try:
        # Get query from request
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        print(f"\nUser query: {query}")
        
        # Check if system is initialized
        if not all([query_parser, data_analyst, viz_generator]):
            return jsonify({"error": "System not properly initialized"}), 500
        
        # 1: Parse query
        print("Step 1: Parsing query...")
        query_plan = query_parser.parse(query)
        
        # 2: Analyze data
        print("Step 2: Analyzing data...")
        analyzed_data = data_analyst.analyze(query_plan)
        
        # 3: Generate visualization
        print("Step 3: Generating visualization...")
        visualization = viz_generator.generate(query_plan, analyzed_data)
        
        # Create explanation
        explanation = _generate_explanation(query_plan, analyzed_data, visualization)
        
        # Return response
        response = {
            "query": query,
            "query_plan": query_plan,
            "data": analyzed_data,
            "visualization": visualization,
            "explanation": explanation,
            "success": True
        }
        
        print("Response ready!\n")
        return jsonify(response)
        
    except Exception as e:
        print(f"Error processing request: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@app.route('/api/data/summary', methods=['GET'])
def data_summary():
    """Get summary of available data"""
    if not data_analyst:
        return jsonify({"error": "Data analyst not initialized"}), 500
    
    summary = data_analyst.get_summary_stats()
    return jsonify(summary)

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example queries"""
    examples = [
        {
            "category": "Count & Statistics",
            "queries": [
                "Show me the number of papers by year",
                "How many papers per field?",
                "Count papers by journal"
            ]
        },
        {
            "category": "Rankings",
            "queries": [
                "Top 10 most cited papers",
                "Top authors by publication count",
                "Most productive years"
            ]
        },
        {
            "category": "Trends",
            "queries": [
                "Papers trend over the last 5 years",
                "Show publication growth",
                "Citation trend by year"
            ]
        },
        {
            "category": "Distributions",
            "queries": [
                "Citation count distribution",
                "Patent count distribution",
                "Papers per author distribution"
            ]
        }
    ]
    return jsonify(examples)

def _generate_explanation(query_plan: dict, 
                         data: list, 
                         visualization: dict) -> str:
    """Generate natural language explanation of results"""
    intent = query_plan.get('intent', 'analysis')
    entity = query_plan.get('entity', 'papers')
    
    if not data:
        return "No data found matching your query."
    
    data_count = len(data)
    
    # Generate contextual explanation
    if intent == "count_by_field":
        groupby = query_plan.get('groupby', 'category')
        return f"Found {data_count} distinct {groupby} categories. The chart shows the distribution of {entity} across these categories."
    
    elif intent == "top_ranking":
        limit = query_plan.get('limit', 10)
        return f"Here are the top {min(limit, data_count)} {entity} ranked by the specified metric. The chart shows their relative performance."
    
    elif intent == "trend_analysis":
        return f"The chart shows how {entity} have changed over time. Found {data_count} time points in the data."
    
    elif intent == "distribution":
        return f"This histogram shows the distribution of values across {data_count} bins, helping you understand the data spread."
    
    else:
        return f"Analysis complete with {data_count} data points. The visualization shows the key insights from your query."

if __name__ == '__main__':
    # Check for API key
    if not os.environ.get('DASHSCOPE_API_KEY'):
        print("WARNING: DASHSCOPE_API_KEY not set!")
    
    print("\nStarting Multi-Agent LLM System (Qwen)...")
    print("API will be available at: http://localhost:5001")
    print("Endpoints:")
    print("   GET  /health - Health check")
    print("   POST /api/chat - Main chat endpoint")
    print("   GET  /api/data/summary - Data summary")
    print("   GET  /api/examples - Example queries")
    print("\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
