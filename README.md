# HR Analytics Dashboard

A comprehensive Streamlit dashboard for analyzing HR data, providing insights into employee demographics, performance, salary distribution, and termination patterns.

## Features

### 📊 Key Metrics
- Total Employees
- Active Employees
- Termination Rate
- Average Salary
- Average Tenure

### 📈 Visualizations
- **Employee Distribution**: Department and gender breakdowns
- **Performance Analysis**: Performance scores and employee satisfaction
- **Salary Analysis**: Salary by department and performance correlation
- **Termination Analysis**: Termination rates and reasons
- **Demographic Analysis**: Age distribution and diversity metrics
- **Advanced Analytics**: Manager effectiveness and engagement correlation

### 🔍 Interactive Features
- **Dynamic Filters**: Filter by Department, Employment Status, Gender, and Performance Score
- **Multiple Tabs**: Organized analysis across different categories
- **Data Export**: Download filtered data as CSV
- **Responsive Design**: Optimized for different screen sizes

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Pip package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Ensure Data File is Present
Make sure `HRDataset_v14_cleaned.csv` is in the same directory as `hr_dashboard.py`

### Step 3: Run the Dashboard
```bash
streamlit run hr_dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Usage Guide

### Navigation
1. **Sidebar Filters**: Use the filters on the left to narrow down your analysis
2. **Key Metrics**: Overview of important HR metrics at the top
3. **Main Charts**: Employee distribution visualizations
4. **Advanced Analytics Tabs**: 
   - **Salary Analysis**: Compensation insights
   - **Termination Analysis**: Employee retention metrics
   - **Demographic Analysis**: Diversity and age insights
   - **Performance Analysis**: Performance and engagement correlation
5. **Data Table**: View and export filtered data

### Key Insights Available
- Identify departments with highest/lowest salaries
- Analyze termination patterns and reasons
- Monitor performance distribution across teams
- Track diversity metrics
- Evaluate manager effectiveness
- Correlate engagement with satisfaction scores

## Dashboard Sections

### 1. Overview Section
- Real-time metrics update based on filters
- Quick snapshot of workforce status

### 2. Distribution Analysis
- Horizontal bar charts for departments
- Pie charts for gender distribution
- Performance score breakdowns

### 3. Advanced Analytics
- **Salary Analysis**: Compensation equity and performance correlation
- **Termination Analysis**: Retention insights and exit reasons
- **Demographics**: Age distribution and diversity metrics
- **Performance**: Engagement vs satisfaction scatter plots

### 4. Data Management
- Interactive data table with column selection
- Export functionality for further analysis
- Real-time filtering capabilities

## Technical Details

### Built With
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Data Processing
- Automatic date parsing and calculation
- Age and tenure calculations
- Data cleaning and standardization
- Missing value handling

## Customization

The dashboard can be easily customized by:
1. Modifying the color schemes in the Plotly charts
2. Adding new metrics or KPIs
3. Including additional chart types
4. Extending filter options
5. Adding new analysis tabs

## Troubleshooting

### Common Issues
1. **Data file not found**: Ensure `HRDataset_v14_cleaned.csv` is in the correct directory
2. **Module not found**: Run `pip install -r requirements.txt`
3. **Port already in use**: Use `streamlit run hr_dashboard.py --server.port 8502`

### Performance Tips
- Use filters to reduce data size for better performance
- Close unused tabs to free up browser memory
- Refresh the page if visualizations don't load properly

## Future Enhancements
- Real-time data connection
- Advanced predictive analytics
- Email report generation
- Role-based access control
- Mobile app version

---
*Built for HR Analytics and Data-Driven Decision Making*
