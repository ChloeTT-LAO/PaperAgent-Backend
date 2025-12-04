# Project 2: Multi-Agent LLM System - Frontend

## Overview

A React-based chat interface for the Scientific Data Analysis Assistant. Users can ask natural language questions and get interactive Vega-Lite visualizations.


## Components

### ChatInterface
Main component that handles:
- Message state management
- API communication
- User input
- Example query display

### MessageDisplay
Renders individual messages with:
- User/assistant differentiation
- Query plan details (expandable)
- Explanation text

### VegaChart
Vega-Lite visualization component:
- Renders Vega-Lite specs
- Handles errors gracefully
- Provides export functionality

### ExampleQueries
Shows categorized example queries:
- Loads from backend API
- Clickable query buttons
- Grouped by category


## Supported Visualizations

The frontend can render any valid Vega-Lite specification:

- **Bar Charts** - Categorical comparisons
- **Line Charts** - Trends over time
- **Scatter Plots** - Correlations
- **Histograms** - Distributions
- **Custom** - Any Vega-Lite spec


## Testing

### Manual Testing Checklist

- [ ] Send a simple query (e.g., "papers by year")
- [ ] Verify chart renders correctly
- [ ] Test example query buttons
- [ ] Check responsive design (mobile/tablet)
- [ ] Test error handling (disconnect backend)
- [ ] Verify loading states
- [ ] Test multiple queries in sequence

### Test with Sample Queries

```typescript
// Count & Statistics
"Show me the number of papers by year"
"How many papers per field?"

// Rankings
"Top 10 most cited papers"
"Top authors by publication count"

// Trends
"Papers trend over the last 5 years"

// Distributions
"Citation count distribution"
```
