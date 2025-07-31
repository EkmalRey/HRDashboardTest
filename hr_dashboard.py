import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load and cache data
@st.cache_data
def load_data():
    """Load HR dataset"""
    try:
        df = pd.read_csv('HRDataset_v14_cleaned.csv')
        
        # Data preprocessing
        # Fix DateofHire parsing with explicit format
        df['DateofHire'] = pd.to_datetime(df['DateofHire'], format='%m/%d/%Y', errors='coerce')
        
        # Fix DateofTermination parsing - handle "Nan" strings and date format
        df['DateofTermination'] = df['DateofTermination'].replace('Nan', pd.NaT)
        df['DateofTermination'] = pd.to_datetime(df['DateofTermination'], format='%m/%d/%Y', errors='coerce')
        
        # Fix LastPerformanceReview_Date parsing with explicit format
        df['LastPerformanceReview_Date'] = pd.to_datetime(df['LastPerformanceReview_Date'], format='%m/%d/%Y', errors='coerce')
        
        # Fix DOB parsing issue with 2-digit years
        def fix_dob(date_str):
            try:
                if pd.isna(date_str):
                    return pd.NaT
                # Parse the date manually to handle 2-digit years correctly
                date_obj = pd.to_datetime(date_str, format='%m/%d/%y', errors='coerce')
                # If year is after 2025 (current year), it's likely a past year (e.g., 70 = 1970, not 2070)
                if date_obj.year > 2025:
                    date_obj = date_obj.replace(year=date_obj.year - 100)
                return date_obj
            except:
                return pd.NaT
        
        df['DOB'] = df['DOB'].apply(fix_dob)
        
        # Calculate age and tenure
        current_date = datetime.now()
        df['Age'] = (current_date - df['DOB']).dt.days / 365.25
        df['Tenure_Years'] = (current_date - df['DateofHire']).dt.days / 365.25
        
        # Clean up any remaining invalid ages (negative or unreasonable)
        df.loc[df['Age'] < 0, 'Age'] = np.nan
        df.loc[df['Age'] > 100, 'Age'] = np.nan
        
        # Clean up categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col not in ['Employee_Name', 'DOB', 'DateofHire', 'DateofTermination', 'LastPerformanceReview_Date']:
                df[col] = df[col].astype(str).str.strip().str.title()
        
        return df
    except FileNotFoundError:
        st.error("Dataset file not found. Please ensure 'HRDataset_v14_cleaned.csv' is in the same directory.")
        return None

# Load data
df = load_data()

if df is not None:
    # Dashboard Title
    st.markdown('<h1 class="main-header">👥 HR Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.header("🔍 Dashboard Filters")
    
    # Department filter
    departments = ['All'] + sorted(df['Department'].dropna().unique().tolist())
    selected_dept = st.sidebar.selectbox("Select Department:", departments)
    
    # Employment Status filter
    emp_status = ['All'] + sorted(df['EmploymentStatus'].dropna().unique().tolist())
    selected_status = st.sidebar.selectbox("Select Employment Status:", emp_status)
    
    # Gender filter
    genders = ['All'] + sorted(df['Sex'].dropna().unique().tolist())
    selected_gender = st.sidebar.selectbox("Select Gender:", genders)
    
    # Performance Score filter
    perf_scores = ['All'] + sorted(df['PerformanceScore'].dropna().unique().tolist())
    selected_perf = st.sidebar.selectbox("Select Performance Score:", perf_scores)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
    if selected_status != 'All':
        filtered_df = filtered_df[filtered_df['EmploymentStatus'] == selected_status]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['Sex'] == selected_gender]
    if selected_perf != 'All':
        filtered_df = filtered_df[filtered_df['PerformanceScore'] == selected_perf]
    
    # Key Metrics Row
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_employees = len(filtered_df)
        st.metric("Total Employees", f"{total_employees:,}")
    
    with col2:
        active_employees = len(filtered_df[filtered_df['EmploymentStatus'] == 'Active'])
        st.metric("Active Employees", f"{active_employees:,}")
    
    with col3:
        terminated_employees = len(filtered_df[filtered_df['Terminated'] == 1])
        termination_rate = (terminated_employees / total_employees * 100) if total_employees > 0 else 0
        st.metric("Termination Rate", f"{termination_rate:.1f}%")
    
    with col4:
        avg_salary = filtered_df['Salary'].mean()
        st.metric("Average Salary", f"${avg_salary:,.0f}")
    
    with col5:
        avg_tenure = filtered_df['Tenure_Years'].mean()
        st.metric("Avg Tenure (Years)", f"{avg_tenure:.1f}")
    
    # Charts Row 1
    st.subheader("📈 Employee Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        # Department Distribution
        dept_counts = filtered_df['Department'].value_counts()
        fig_dept = px.bar(
            x=dept_counts.values,
            y=dept_counts.index,
            orientation='h',
            title="Employee Distribution by Department",
            labels={'x': 'Number of Employees', 'y': 'Department'},
            color=dept_counts.values,
            color_continuous_scale='viridis'
        )
        fig_dept.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_dept, use_container_width=True)
    
    with col2:
        # Gender Distribution
        gender_counts = filtered_df['Sex'].value_counts()
        fig_gender = px.pie(
            values=gender_counts.values,
            names=gender_counts.index,
            title="Gender Distribution",
            color_discrete_sequence=['#ff7f0e', '#1f77b4']
        )
        fig_gender.update_layout(height=400)
        st.plotly_chart(fig_gender, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance Score Distribution
        perf_counts = filtered_df['PerformanceScore'].value_counts()
        fig_perf = px.bar(
            x=perf_counts.index,
            y=perf_counts.values,
            title="Performance Score Distribution",
            labels={'x': 'Performance Score', 'y': 'Number of Employees'},
            color=perf_counts.values,
            color_continuous_scale='RdYlGn'
        )
        fig_perf.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with col2:
        # Employment Status
        status_counts = filtered_df['EmploymentStatus'].value_counts()
        fig_status = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            title="Employment Status Distribution",
            labels={'x': 'Employment Status', 'y': 'Number of Employees'},
            color=status_counts.values,
            color_continuous_scale='blues'
        )
        fig_status.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Advanced Analytics Section
    st.subheader("🔍 Advanced Analytics")
    
    # Tabs for different analysis
    tab1, tab2, tab3, tab4 = st.tabs(["Salary Analysis", "Termination Analysis", "Demographic Analysis", "Performance Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Salary by Department
            avg_salary_dept = filtered_df.groupby('Department')['Salary'].mean().sort_values(ascending=False)
            fig_sal_dept = px.bar(
                x=avg_salary_dept.values,
                y=avg_salary_dept.index,
                orientation='h',
                title="Average Salary by Department",
                labels={'x': 'Average Salary ($)', 'y': 'Department'},
                color=avg_salary_dept.values,
                color_continuous_scale='greens'
            )
            fig_sal_dept.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_sal_dept, use_container_width=True)
        
        with col2:
            # Salary vs Performance
            fig_sal_perf = px.box(
                filtered_df,
                x='PerformanceScore',
                y='Salary',
                title="Salary Distribution by Performance Score",
                color='PerformanceScore'
            )
            fig_sal_perf.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_sal_perf, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Termination by Department
            term_by_dept = filtered_df.groupby('Department')['Terminated'].agg(['sum', 'count']).reset_index()
            term_by_dept['Termination_Rate'] = (term_by_dept['sum'] / term_by_dept['count'] * 100)
            
            fig_term_dept = px.bar(
                term_by_dept,
                x='Department',
                y='Termination_Rate',
                title="Termination Rate by Department (%)",
                labels={'Termination_Rate': 'Termination Rate (%)'},
                color='Termination_Rate',
                color_continuous_scale='reds'
            )
            fig_term_dept.update_layout(height=400, showlegend=False)
            fig_term_dept.update_xaxes(tickangle=45)
            st.plotly_chart(fig_term_dept, use_container_width=True)
        
        with col2:
            # Termination Reasons
            term_reasons = filtered_df[filtered_df['Terminated'] == 1]['TermReason'].value_counts()
            if len(term_reasons) > 0:
                fig_term_reason = px.pie(
                    values=term_reasons.values,
                    names=term_reasons.index,
                    title="Termination Reasons",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_term_reason.update_layout(height=400)
                st.plotly_chart(fig_term_reason, use_container_width=True)
            else:
                st.info("No termination data available for current filters.")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Age Distribution
            age_data = filtered_df[filtered_df['Age'].notna()]  # Filter out NaN values
            if len(age_data) > 0:
                fig_age = px.histogram(
                    age_data,
                    x='Age',
                    nbins=20,
                    title="Age Distribution",
                    labels={'Age': 'Age (Years)', 'count': 'Number of Employees'},
                    color_discrete_sequence=['#2E86AB']
                )
                fig_age.update_layout(height=400)
                st.plotly_chart(fig_age, use_container_width=True)
            else:
                st.info("No valid age data available for current filters.")
        
        with col2:
            # Diversity Analysis
            race_counts = filtered_df['RaceDesc'].value_counts()
            fig_race = px.bar(
                x=race_counts.values,
                y=race_counts.index,
                orientation='h',
                title="Racial Diversity",
                labels={'x': 'Number of Employees', 'y': 'Race'},
                color=race_counts.values,
                color_continuous_scale='viridis'
            )
            fig_race.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_race, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance vs Engagement
            fig_perf_eng = px.scatter(
                filtered_df,
                x='EngagementSurvey',
                y='EmpSatisfaction',
                color='PerformanceScore',
                size='Salary',
                title="Employee Engagement vs Satisfaction",
                labels={'EngagementSurvey': 'Engagement Score', 'EmpSatisfaction': 'Satisfaction Score'},
                hover_data=['Department', 'Position']
            )
            fig_perf_eng.update_layout(height=400)
            st.plotly_chart(fig_perf_eng, use_container_width=True)
        
        with col2:
            # Manager Performance
            manager_stats = filtered_df.groupby('ManagerName').agg({
                'PerformanceScore': lambda x: (x == 'Exceeds').sum() / len(x) * 100,
                'Employee_Name': 'count'
            }).reset_index()
            manager_stats.columns = ['ManagerName', 'High_Performers_Pct', 'Team_Size']
            manager_stats = manager_stats[manager_stats['Team_Size'] >= 3]  # Only managers with 3+ employees
            
            if len(manager_stats) > 0:
                fig_manager = px.scatter(
                    manager_stats,
                    x='Team_Size',
                    y='High_Performers_Pct',
                    size='Team_Size',
                    title="Manager Effectiveness (High Performers %)",
                    labels={'Team_Size': 'Team Size', 'High_Performers_Pct': 'High Performers (%)'},
                    hover_data=['ManagerName']
                )
                fig_manager.update_layout(height=400)
                st.plotly_chart(fig_manager, use_container_width=True)
            else:
                st.info("Insufficient data for manager analysis.")
    
    # Data Table Section
    st.subheader("📋 Detailed Data View")
    
    # Show filtered data
    if st.checkbox("Show Filtered Data"):
        # Select columns to display
        display_columns = st.multiselect(
            "Select columns to display:",
            df.columns.tolist(),
            default=['Employee_Name', 'Department', 'Position', 'Salary', 'PerformanceScore', 'EmploymentStatus']
        )
        
        if display_columns:
            st.dataframe(
                filtered_df[display_columns],
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = filtered_df[display_columns].to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name=f"hr_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>HR Analytics Dashboard | Built with Streamlit 📊</p>
            <p>Data insights to drive better HR decisions</p>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.error("Unable to load data. Please check if the dataset file exists.")
