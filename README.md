# Project 2: Multi-Agent LLM System - Frontend

## 🎯 Overview

A modern React-based chat interface for the Scientific Data Analysis Assistant. Users can ask natural language questions and get interactive Vega-Lite visualizations.

## ✨ Features

- **💬 Chat Interface** - Clean, intuitive conversation UI
- **📊 Vega-Lite Visualizations** - Interactive, responsive charts
- **🎨 Modern Design** - Built with Tailwind CSS
- **⚡ Fast** - Powered by Vite
- **📱 Responsive** - Works on all screen sizes
- **🔍 Example Queries** - Get started quickly

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd project2-frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will open at `http://localhost:3000`

### 3. Make Sure Backend is Running

The frontend needs the backend API at `http://localhost:5001`

```bash
# In another terminal
cd ../project2-backend
python app.py
```

## 📁 Project Structure

```
project2-frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.tsx    # Main chat component
│   │   ├── MessageDisplay.tsx   # Message rendering
│   │   ├── VegaChart.tsx        # Vega-Lite renderer
│   │   └── ExampleQueries.tsx   # Example queries
│   ├── services/
│   │   └── api.ts               # API client
│   ├── types/
│   │   └── index.ts             # TypeScript types
│   ├── App.tsx                  # Root component
│   ├── main.tsx                 # Entry point
│   └── index.css                # Global styles
├── index.html                   # HTML template
├── package.json                 # Dependencies
├── vite.config.ts               # Vite configuration
├── tsconfig.json                # TypeScript config
└── tailwind.config.js           # Tailwind config
```

## 🧩 Components

### ChatInterface
Main component that handles:
- Message state management
- API communication
- User input
- Example query display

### MessageDisplay
Renders individual messages with:
- User/assistant differentiation
- Vega-Lite chart embedding
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

## 🔧 Configuration

### Change API URL

Edit `src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:5001';
```

### Change Port

Edit `vite.config.ts`:

```typescript
server: {
  port: 3000,  // Change to your preferred port
  open: true,
}
```

## 📊 Supported Visualizations

The frontend can render any valid Vega-Lite specification:

- **Bar Charts** - Categorical comparisons
- **Line Charts** - Trends over time
- **Scatter Plots** - Correlations
- **Histograms** - Distributions
- **Custom** - Any Vega-Lite spec

## 🎨 Styling

Built with Tailwind CSS for rapid, responsive design.

### Color Scheme
- Primary: Indigo (`indigo-600`)
- Background: Gray gradients
- Success: Green
- Error: Red

### Customize Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#your-color',
    },
  },
}
```

## 🧪 Testing

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

## 🐛 Troubleshooting

### Issue: Blank Page
**Solution:** Check browser console for errors. Ensure all dependencies are installed.

```bash
npm install
npm run dev
```

### Issue: API Connection Error
**Solution:** Verify backend is running:

```bash
curl http://localhost:5001/health
```

### Issue: Chart Not Rendering
**Solution:** Check browser console. Vega-Lite specs might be invalid. The component should show error message.

### Issue: TypeScript Errors
**Solution:** Ensure types are up to date:

```bash
npm install --save-dev @types/react @types/react-dom
```

### Issue: Styles Not Loading
**Solution:** Check Tailwind is properly configured:

```bash
# Verify these files exist
ls tailwind.config.js postcss.config.js
```

## 📦 Building for Production

```bash
npm run build
```

Output will be in `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

### Deploy

The built app can be deployed to:
- Vercel
- Netlify
- GitHub Pages
- Any static hosting service

Example for Vercel:
```bash
npm install -g vercel
vercel --prod
```

## 🚀 Performance Optimization

### Current Optimizations
- React.memo for expensive components
- Debounced input (if needed)
- Lazy loading for large charts
- Efficient state management

### Future Improvements
- Implement virtual scrolling for long conversations
- Add service worker for offline support
- Optimize bundle size with code splitting

## 📝 Development Notes

### Adding New Features

1. **New Visualization Type**
   - Update `VegaChart.tsx` if custom rendering needed
   - Most cases work automatically

2. **New UI Component**
   - Create in `src/components/`
   - Export from component
   - Import in parent component

3. **New API Endpoint**
   - Add to `src/services/api.ts`
   - Update TypeScript types in `src/types/`

### Code Style

- Use TypeScript for type safety
- Follow React hooks best practices
- Use functional components only
- Keep components small and focused
- Use Tailwind utilities for styling

## 🔗 Related

- Backend: `../project2-backend/`
- API Documentation: Backend README
- Vega-Lite Docs: https://vega.github.io/vega-lite/

## 📄 License

For educational purposes (Coding Test Project).
