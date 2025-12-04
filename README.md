# Scientific Publication Network Visualization - Backend

> Multi-agent LLM system for analyzing and visualizing scientific publication data using Qwen API

---

## 🏗️ System Architecture

```
User Query → Query Parser Agent → Data Analyst Agent → Viz Generator Agent → Vega-Lite Spec
             (Qwen API)          (Pandas)             (Template-based)
```

### Agent Roles

1. **Query Parser Agent** (`agents/query_parser.py`)
   - Uses Qwen API to understand natural language queries
   - Extracts intent, entity, filters, and aggregation parameters
   - Outputs structured query plan

2. **Data Analyst Agent** (`agents/data_analyst.py`)
   - Executes data queries using pandas
   - Performs aggregation, filtering, and sorting
   - Returns analyzed results as JSON

3. **Visualization Generator Agent** (`agents/viz_generator.py`)
   - Creates Vega-Lite specifications
   - Supports line charts, bar charts, and histograms
   - Ensures proper data formatting for visualization

---
