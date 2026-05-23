# ============================================================
#  Palo Alto Networks — HR Engagement & Burnout Dashboard
#  Built with Streamlit
#  HOW TO RUN:
#    1. pip install streamlit plotly pandas
#    2. streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PAN HR Analytics",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS Styling ────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; color: #ffffff; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1a1d2e;
        border-right: 1px solid #2d2f3e;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e2130, #252840);
        border: 1px solid #3d4166;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 6px 0 2px 0;
    }
    .kpi-label {
        font-size: 0.78rem;
        color: #8b8fa8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-delta {
        font-size: 0.82rem;
        margin-top: 4px;
    }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #a0a8d0;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 8px 0 4px 0;
        border-bottom: 1px solid #2d2f3e;
        margin-bottom: 16px;
    }

    /* Alert box */
    .alert-high {
        background: rgba(231,76,60,0.15);
        border-left: 4px solid #e74c3c;
        border-radius: 6px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 0.88rem;
    }
    .alert-medium {
        background: rgba(243,156,18,0.15);
        border-left: 4px solid #f39c12;
        border-radius: 6px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 0.88rem;
    }

    /* Hide default streamlit header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING & PROCESSING
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data   # Cache so data doesn't reload every time user clicks something
def load_and_process(path):
    df = pd.read_csv(path)

    # ── Build Engagement Index ──────────────────────────────────────────────
    eng_cols = ['JobInvolvement','JobSatisfaction',
                'EnvironmentSatisfaction','RelationshipSatisfaction']
    df['EngagementIndex'] = df[eng_cols].mean(axis=1).round(2)

    # ── Burnout Risk ────────────────────────────────────────────────────────
    df['OvertimeFlag'] = (df['OverTime'] == 'Yes').astype(int)
    df['LowWLBFlag']   = (df['WorkLifeBalance'] <= 2).astype(int)
    df['BurnoutScore'] = df['OvertimeFlag'] + df['LowWLBFlag']
    df['BurnoutRisk']  = df['BurnoutScore'].map({0:'Low',1:'Medium',2:'High'})

    # ── Satisfaction Stability ──────────────────────────────────────────────
    sat_cols = ['JobSatisfaction','EnvironmentSatisfaction',
                'RelationshipSatisfaction','JobInvolvement']
    df['SatisfactionStability'] = (4 - df[sat_cols].std(axis=1)).round(2)

    # ── Workload Stress ─────────────────────────────────────────────────────
    df['WorkloadStress'] = (
        (df['OverTime'] == 'Yes') &
        (df['BusinessTravel'] == 'Travel_Frequently')
    ).astype(int)

    # ── Attrition Label ─────────────────────────────────────────────────────
    df['AttritionLabel'] = df['Attrition'].map({0:'Stayed',1:'Left'})

    # ── Tenure Stage ────────────────────────────────────────────────────────
    df['TenureStage'] = pd.cut(
        df['YearsAtCompany'],
        bins=[-1,2,5,10,20,100],
        labels=['New (0–2y)','Early (3–5y)','Mid (6–10y)','Senior (11–20y)','Veteran (20+y)']
    )

    # ── Commute Category ────────────────────────────────────────────────────
    df['CommuteCategory'] = pd.cut(
        df['DistanceFromHome'],
        bins=[0,10,20,100],
        labels=['Short (0–10)','Medium (11–20)','Long (21+)']
    )

    return df

# Load data
try:
    df = load_and_process('Palo_Alto_Networks.csv')
except FileNotFoundError:
    st.error("⚠️ CSV file not found! Make sure 'Palo_Alto_Networks.csv' is in the same folder as app.py")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — FILTERS
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🔐 PAN HR Analytics")
    st.markdown("*Employee Engagement & Burnout Diagnostic*")
    st.markdown("---")

    st.markdown("### 🎛️ Filters")

    # Department filter
    all_depts = ['All'] + sorted(df['Department'].unique().tolist())
    dept_filter = st.selectbox("Department", all_depts)

    # Overtime filter
    overtime_filter = st.radio("Overtime", ["All", "Yes", "No"], horizontal=True)

    # Engagement threshold slider
    eng_threshold = st.slider(
        "Min Engagement Index",
        min_value=1.0, max_value=4.0, value=1.0, step=0.1
    )

    # Tenure range
    tenure_range = st.slider(
        "Years at Company (range)",
        min_value=0, max_value=int(df['YearsAtCompany'].max()),
        value=(0, int(df['YearsAtCompany'].max()))
    )

    st.markdown("---")

    # Burnout risk filter
    burnout_filter = st.multiselect(
        "Burnout Risk Level",
        options=['Low','Medium','High'],
        default=['Low','Medium','High']
    )

    st.markdown("---")
    st.markdown("### 📋 About")
    st.markdown("*Dashboard built as part of HR Analytics project for Palo Alto Networks.*")

# ── Apply Filters ─────────────────────────────────────────────────────────────
filtered = df.copy()

if dept_filter != 'All':
    filtered = filtered[filtered['Department'] == dept_filter]

if overtime_filter != 'All':
    filtered = filtered[filtered['OverTime'] == overtime_filter]

filtered = filtered[filtered['EngagementIndex'] >= eng_threshold]
filtered = filtered[
    (filtered['YearsAtCompany'] >= tenure_range[0]) &
    (filtered['YearsAtCompany'] <= tenure_range[1])
]
filtered = filtered[filtered['BurnoutRisk'].isin(burnout_filter)]


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN DASHBOARD — PAGE TABS
# ══════════════════════════════════════════════════════════════════════════════

# Top title
st.markdown("""
<h1 style='font-size:1.8rem; font-weight:700; margin-bottom:4px;'>
🔐 Palo Alto Networks — HR Engagement & Burnout Dashboard
</h1>
<p style='color:#8b8fa8; font-size:0.9rem; margin-bottom:20px;'>
Real-time diagnostics for employee engagement, burnout risk, and attrition prevention.
</p>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Engagement Overview",
    "🔥 Burnout Risk",
    "🏢 Department & Roles",
    "📈 Career & Tenure",
    "🚪 Attrition Analysis"
])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1: ENGAGEMENT OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════

with tab1:

    # ── KPI Cards Row ─────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)

    avg_eng   = filtered['EngagementIndex'].mean()
    avg_wlb   = filtered['WorkLifeBalance'].mean()
    avg_stab  = filtered['SatisfactionStability'].mean()
    high_burn = (filtered['BurnoutRisk'] == 'High').mean() * 100
    att_rate  = filtered['Attrition'].mean() * 100

    with k1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Engagement Index</div>
            <div class='kpi-value' style='color:#4fc3f7;'>{avg_eng:.2f}</div>
            <div class='kpi-delta' style='color:#8b8fa8;'>out of 4.0</div>
        </div>""", unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Work-Life Balance</div>
            <div class='kpi-value' style='color:#81c784;'>{avg_wlb:.2f}</div>
            <div class='kpi-delta' style='color:#8b8fa8;'>out of 4.0</div>
        </div>""", unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Satisfaction Stability</div>
            <div class='kpi-value' style='color:#ce93d8;'>{avg_stab:.2f}</div>
            <div class='kpi-delta' style='color:#8b8fa8;'>consistency score</div>
        </div>""", unsafe_allow_html=True)

    with k4:
        color = '#e74c3c' if high_burn > 20 else '#f39c12' if high_burn > 10 else '#2ecc71'
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>High Burnout Risk</div>
            <div class='kpi-value' style='color:{color};'>{high_burn:.1f}%</div>
            <div class='kpi-delta' style='color:#8b8fa8;'>of workforce</div>
        </div>""", unsafe_allow_html=True)

    with k5:
        color = '#e74c3c' if att_rate > 20 else '#f39c12' if att_rate > 10 else '#2ecc71'
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Attrition Rate</div>
            <div class='kpi-value' style='color:{color};'>{att_rate:.1f}%</div>
            <div class='kpi-delta' style='color:#8b8fa8;'>{filtered['Attrition'].sum()} employees left</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row ────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Engagement Index Distribution</div>", unsafe_allow_html=True)
        fig = px.histogram(
            filtered, x='EngagementIndex', nbins=25,
            color_discrete_sequence=['#4fc3f7'],
            labels={'EngagementIndex': 'Engagement Index', 'count': 'Employees'}
        )
        fig.add_vline(x=avg_eng, line_dash='dash', line_color='#e74c3c',
                      annotation_text=f'Mean: {avg_eng:.2f}', annotation_position='top right')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', showlegend=False, height=320,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Satisfaction Dimensions Breakdown</div>", unsafe_allow_html=True)
        sat_means = {
            'Job Involvement':     filtered['JobInvolvement'].mean(),
            'Job Satisfaction':    filtered['JobSatisfaction'].mean(),
            'Environment Sat.':    filtered['EnvironmentSatisfaction'].mean(),
            'Relationship Sat.':   filtered['RelationshipSatisfaction'].mean(),
        }
        fig2 = go.Figure(go.Bar(
            x=list(sat_means.values()),
            y=list(sat_means.keys()),
            orientation='h',
            marker_color=['#4fc3f7','#81c784','#ce93d8','#ffb74d'],
            text=[f'{v:.2f}' for v in sat_means.values()],
            textposition='outside'
        ))
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=320, xaxis_range=[0, 4.5],
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Overtime vs Engagement ─────────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='section-header'>Engagement: Overtime vs No Overtime</div>", unsafe_allow_html=True)
        fig3 = px.box(
            filtered, x='OverTime', y='EngagementIndex',
            color='OverTime',
            color_discrete_map={'Yes': '#e74c3c', 'No': '#2ecc71'},
            labels={'EngagementIndex': 'Engagement Index', 'OverTime': 'Overtime'}
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', showlegend=False, height=300,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("<div class='section-header'>Engagement by Travel Frequency</div>", unsafe_allow_html=True)
        travel_eng = filtered.groupby('BusinessTravel')['EngagementIndex'].mean().reset_index()
        travel_eng.columns = ['Travel', 'Avg Engagement']
        fig4 = px.bar(
            travel_eng, x='Travel', y='Avg Engagement',
            color='Avg Engagement',
            color_continuous_scale='Blues',
            text='Avg Engagement'
        )
        fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', showlegend=False, height=300,
            margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False
        )
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2: BURNOUT RISK
# ══════════════════════════════════════════════════════════════════════════════

with tab2:

    col1, col2, col3 = st.columns(3)

    low_count  = (filtered['BurnoutRisk'] == 'Low').sum()
    med_count  = (filtered['BurnoutRisk'] == 'Medium').sum()
    high_count = (filtered['BurnoutRisk'] == 'High').sum()

    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>🟢 Low Risk</div>
            <div class='kpi-value' style='color:#2ecc71;'>{low_count}</div>
            <div class='kpi-delta' style='color:#8b8fa8;'>{low_count/len(filtered)*100:.1f}% of staff</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>🟡 Medium Risk</div>
            <div class='kpi-value' style='color:#f39c12;'>{med_count}</div>
            <div class='kpi-delta' style='color:#8b8fa8;'>{med_count/len(filtered)*100:.1f}% of staff</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>🔴 High Risk</div>
            <div class='kpi-value' style='color:#e74c3c;'>{high_count}</div>
            <div class='kpi-delta' style='color:#8b8fa8;'>{high_count/len(filtered)*100:.1f}% of staff</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Burnout Risk Distribution</div>", unsafe_allow_html=True)
        burnout_counts = filtered['BurnoutRisk'].value_counts().reset_index()
        burnout_counts.columns = ['Risk', 'Count']
        fig = px.pie(
            burnout_counts, names='Risk', values='Count',
            color='Risk',
            color_discrete_map={'Low':'#2ecc71','Medium':'#f39c12','High':'#e74c3c'},
            hole=0.45
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=340,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Burnout Risk by Department</div>", unsafe_allow_html=True)
        dept_burn = filtered.groupby(['Department','BurnoutRisk']).size().reset_index(name='Count')
        fig2 = px.bar(
            dept_burn, x='Department', y='Count', color='BurnoutRisk',
            barmode='stack',
            color_discrete_map={'Low':'#2ecc71','Medium':'#f39c12','High':'#e74c3c'},
            labels={'Count':'Employees'}
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=340,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Burnout vs Engagement scatter
    st.markdown("<div class='section-header'>Burnout Risk vs Engagement Index (All Employees)</div>", unsafe_allow_html=True)
    fig3 = px.scatter(
        filtered, x='WorkLifeBalance', y='EngagementIndex',
        color='BurnoutRisk', size='MonthlyIncome',
        color_discrete_map={'Low':'#2ecc71','Medium':'#f39c12','High':'#e74c3c'},
        hover_data=['Department','JobRole','OverTime'],
        labels={'WorkLifeBalance':'Work-Life Balance','EngagementIndex':'Engagement Index'}
    )
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff', height=380,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig3, use_container_width=True)

    # High-risk employee table
    st.markdown("<div class='section-header'>🔴 High Burnout Risk — Priority Employees</div>", unsafe_allow_html=True)
    high_risk_df = filtered[filtered['BurnoutRisk'] == 'High'][[
        'Department','JobRole','JobLevel','EngagementIndex',
        'WorkLifeBalance','OverTime','YearsAtCompany','AttritionLabel'
    ]].sort_values('EngagementIndex').head(15)
    st.dataframe(
        high_risk_df.style.map(
            lambda v: 'background-color: rgba(231,76,60,0.2)' if v == 'Left' else '',
            subset=['AttritionLabel']
        ),
        use_container_width=True, height=300
    )


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3: DEPARTMENT & ROLES
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Average Engagement by Department</div>", unsafe_allow_html=True)
        dept_eng = filtered.groupby('Department')['EngagementIndex'].mean().reset_index()
        dept_eng.columns = ['Department','Avg Engagement']
        fig = px.bar(
            dept_eng.sort_values('Avg Engagement'),
            x='Avg Engagement', y='Department', orientation='h',
            color='Avg Engagement', color_continuous_scale='Blues',
            text='Avg Engagement'
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=300, coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Average Engagement by Job Role</div>", unsafe_allow_html=True)
        role_eng = filtered.groupby('JobRole')['EngagementIndex'].mean().reset_index()
        role_eng.columns = ['Job Role','Avg Engagement']
        fig2 = px.bar(
            role_eng.sort_values('Avg Engagement'),
            x='Avg Engagement', y='Job Role', orientation='h',
            color='Avg Engagement', color_continuous_scale='Teal',
            text='Avg Engagement'
        )
        fig2.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=360, coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='section-header'>Engagement by Job Level</div>", unsafe_allow_html=True)
        jl_eng = filtered.groupby('JobLevel')['EngagementIndex'].mean().reset_index()
        jl_eng.columns = ['Job Level','Avg Engagement']
        fig3 = px.line(
            jl_eng, x='Job Level', y='Avg Engagement',
            markers=True, line_shape='spline',
            color_discrete_sequence=['#4fc3f7']
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=300,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(tickmode='linear', dtick=1)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("<div class='section-header'>Attrition Rate by Department</div>", unsafe_allow_html=True)
        dept_att = filtered.groupby('Department')['Attrition'].mean().mul(100).reset_index()
        dept_att.columns = ['Department','Attrition Rate (%)']
        fig4 = px.bar(
            dept_att.sort_values('Attrition Rate (%)'),
            x='Department', y='Attrition Rate (%)',
            color='Attrition Rate (%)', color_continuous_scale='Reds',
            text='Attrition Rate (%)'
        )
        fig4.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=300, coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Department summary table
    st.markdown("<div class='section-header'>📋 Full Department Summary</div>", unsafe_allow_html=True)
    dept_summary = filtered.groupby('Department').agg(
        Employees       = ('EngagementIndex','count'),
        Avg_Engagement  = ('EngagementIndex','mean'),
        Avg_WLB         = ('WorkLifeBalance','mean'),
        High_Burnout_Pct= ('BurnoutScore', lambda x: f"{(x==2).mean()*100:.1f}%"),
        Overtime_Pct    = ('OvertimeFlag',  lambda x: f"{x.mean()*100:.1f}%"),
        Attrition_Rate  = ('Attrition',     lambda x: f"{x.mean()*100:.1f}%")
    ).round(2).reset_index()
    st.dataframe(dept_summary, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4: CAREER & TENURE
# ══════════════════════════════════════════════════════════════════════════════

with tab4:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Engagement by Tenure Stage</div>", unsafe_allow_html=True)
        ten_eng = filtered.groupby('TenureStage', observed=True)['EngagementIndex'].mean().reset_index()
        ten_eng.columns = ['Tenure Stage','Avg Engagement']
        fig = px.bar(
            ten_eng, x='Tenure Stage', y='Avg Engagement',
            color='Avg Engagement', color_continuous_scale='Blues',
            text='Avg Engagement'
        )
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=320, coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Stagnation Signal — Years in Role vs Engagement</div>", unsafe_allow_html=True)
        role_yrs = filtered.groupby('YearsInCurrentRole')['EngagementIndex'].mean().reset_index()
        fig2 = px.line(
            role_yrs, x='YearsInCurrentRole', y='EngagementIndex',
            markers=True, line_shape='spline',
            color_discrete_sequence=['#ff7675'],
            labels={'YearsInCurrentRole':'Years in Current Role','EngagementIndex':'Avg Engagement'}
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=320,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='section-header'>Years Since Promotion vs Engagement</div>", unsafe_allow_html=True)
        promo_eng = filtered.groupby('YearsSinceLastPromotion')['EngagementIndex'].mean().reset_index()
        fig3 = px.area(
            promo_eng, x='YearsSinceLastPromotion', y='EngagementIndex',
            color_discrete_sequence=['#a29bfe'],
            labels={'YearsSinceLastPromotion':'Years Since Promotion','EngagementIndex':'Avg Engagement'}
        )
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=300,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("<div class='section-header'>Training & Engagement</div>", unsafe_allow_html=True)
        train_eng = filtered.groupby('TrainingTimesLastYear')['EngagementIndex'].mean().reset_index()
        fig4 = px.bar(
            train_eng, x='TrainingTimesLastYear', y='EngagementIndex',
            color='EngagementIndex', color_continuous_scale='Greens',
            text='EngagementIndex',
            labels={'TrainingTimesLastYear':'Training Sessions Last Year'}
        )
        fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', height=300, coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5: ATTRITION ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

with tab5:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Engagement: Stayed vs Left</div>", unsafe_allow_html=True)
        fig = px.box(
            filtered, x='AttritionLabel', y='EngagementIndex',
            color='AttritionLabel',
            color_discrete_map={'Stayed':'#2ecc71','Left':'#e74c3c'},
            labels={'AttritionLabel':'','EngagementIndex':'Engagement Index'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', showlegend=False, height=340,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header'>Attrition Rate by Overtime</div>", unsafe_allow_html=True)
        ot_att = filtered.groupby('OverTime')['Attrition'].mean().mul(100).reset_index()
        ot_att.columns = ['Overtime','Attrition Rate (%)']
        fig2 = px.bar(
            ot_att, x='Overtime', y='Attrition Rate (%)',
            color='Overtime',
            color_discrete_map={'Yes':'#e74c3c','No':'#2ecc71'},
            text='Attrition Rate (%)'
        )
        fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff', showlegend=False, height=340,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Correlation heatmap
    st.markdown("<div class='section-header'>Correlation Heatmap — All Key Metrics</div>", unsafe_allow_html=True)
    corr_cols = [
        'EngagementIndex','WorkLifeBalance','JobSatisfaction',
        'EnvironmentSatisfaction','RelationshipSatisfaction',
        'JobInvolvement','BurnoutScore','OvertimeFlag','Attrition'
    ]
    corr = filtered[corr_cols].corr().round(2)
    fig3 = px.imshow(
        corr, text_auto=True, aspect='auto',
        color_continuous_scale='RdYlGn', zmin=-1, zmax=1,
        labels=dict(color='Correlation')
    )
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff', height=450,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Stats comparison table
    st.markdown("<div class='section-header'>📋 Metric Comparison — Stayed vs Left</div>", unsafe_allow_html=True)
    metrics = ['EngagementIndex','WorkLifeBalance','JobSatisfaction',
               'EnvironmentSatisfaction','RelationshipSatisfaction','MonthlyIncome']
    comp = filtered.groupby('AttritionLabel')[metrics].mean().round(3).T
    comp['Difference'] = (comp.get('Stayed', 0) - comp.get('Left', 0)).round(3)
    st.dataframe(comp, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#8b8fa8; font-size:0.8rem;'>"
    "🔐 Palo Alto Networks HR Analytics Dashboard &nbsp;|&nbsp; "
    f"Showing {len(filtered):,} of {len(df):,} employees &nbsp;|&nbsp; "
    "Built with Streamlit + Plotly"
    "</p>",
    unsafe_allow_html=True
)
