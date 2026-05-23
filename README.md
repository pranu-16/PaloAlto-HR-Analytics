# 🔐 Employee Engagement, Satisfaction & Burnout Diagnostic Analysis
## Palo Alto Networks — HR Analytics Project

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat&logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat&logo=jupyter)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red?style=flat&logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualisation-3F4F75?style=flat&logo=plotly)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat)

---

## 📌 Project Overview

This project provides a **preventive HR diagnostic system** for Palo Alto Networks to detect employee disengagement and burnout risk **before** attrition occurs.

Rather than reacting after employees leave, this system identifies **early warning signals** using a composite Engagement Index, multi-signal Burnout Risk Score, and career stagnation indicators — shifting HR from reactive to proactive people management.

> 📄 Research paper published in **IJIRT Journal** (ISSN: 2349-6002 | Impact Factor: 8.412)

---

## 🎯 Key Findings

| KPI | Value | Insight |
|-----|-------|---------|
| Overall Engagement Index | **2.72 / 4.0** | 68.1% — moderate, room to improve |
| High Burnout Risk | **8.6%** | 126 employees need immediate action |
| Medium Burnout Risk | **40.0%** | 588 employees at tipping point |
| Overtime Attrition Rate | **30.5%** | 3× higher than non-overtime (10.4%) |
| Attrition Rate (overall) | **16.1%** | 237 of 1,470 employees left |
| Engagement — Employees who Left | **2.51** | vs 2.76 for those who stayed |

---

## 📊 Dataset

| Property | Value |
|----------|-------|
| Source | Palo Alto Networks HR Dataset |
| Total Records | 1,470 employees |
| Total Features | 31 attributes |
| Missing Values | None |
| Departments | Sales, Research & Development, Human Resources |
| Job Roles | 9 distinct roles |

---

## 🗂️ Project Structure

```
PaloAlto-HR-Analytics/
│
├── 📓 PaloAltoNetworks_HR_Analysis.ipynb       ← Full EDA + KPI Analysis (Jupyter)
├── 🐍 app.py                                   ← Streamlit Interactive Dashboard
├── 📊 Palo_Alto_Networks.csv                   ← HR Dataset (1,470 records)
├── 📄 PaloAltoNetworks_Research_Paper_Final.docx  ← IEEE Format Research Paper
└── 📝 README.md                                ← Project Documentation
```

---

## 📓 Jupyter Notebook — What's Inside

The notebook walks through the full analysis pipeline step by step:

| Step | Section | Description |
|------|---------|-------------|
| 0 | Library Setup | Import pandas, matplotlib, seaborn |
| 1 | Data Loading & EDA | Shape, columns, distributions |
| 2 | Data Validation | Missing values, ordinal range checks |
| 3 | Engagement Index | Composite score from 4 satisfaction dimensions |
| 4 | Burnout Risk | Low / Medium / High classification |
| 5 | Workload Analysis | Overtime, travel, commute effects |
| 6 | Career Stage Analysis | Tenure, stagnation, promotion gaps |
| 7 | Attrition Analysis | Stayed vs Left comparison |
| 8 | KPI Dashboard | Full summary + correlation heatmap |

---

## 🖥️ Streamlit Dashboard — 5 Tabs

| Tab | What You See |
|-----|-------------|
| 📊 Engagement Overview | 5 KPI cards + satisfaction breakdown charts |
| 🔥 Burnout Risk | Pie chart, stacked bars, scatter plot, risk table |
| 🏢 Department & Roles | Engagement by dept, role, job level |
| 📈 Career & Tenure | Stagnation signals, promotion gap, training impact |
| 🚪 Attrition Analysis | Stayed vs Left + full correlation heatmap |

**Live Sidebar Filters:** Department · Overtime · Engagement Threshold · Tenure Range · Burnout Risk Level

---

## 📦 Libraries Used

```python
pandas          # Data manipulation and analysis
numpy           # Numerical computing
matplotlib      # Static visualisations
seaborn         # Statistical charts
plotly          # Interactive charts for dashboard
streamlit       # Web application framework
scikit-learn    # Machine learning (Decision Tree)
```

---

## 🚀 How to Run

### 1. Clone this repository
```bash
git clone https://github.com/pranu-16/PaloAlto-HR-Analytics.git
cd PaloAlto-HR-Analytics
```

### 2. Install required libraries
```bash
pip install pandas numpy matplotlib seaborn plotly streamlit scikit-learn
```

### 3. Run Jupyter Notebook
```bash
jupyter notebook PaloAltoNetworks_HR_Analysis.ipynb
```

### 4. Run Streamlit Dashboard
```bash
streamlit run app.py
```
Your browser will automatically open the dashboard at `http://localhost:8501`

---

## 📈 Analytical Methodology

### Engagement Index Formula
```
EngagementIndex = mean(JobInvolvement + JobSatisfaction +
                       EnvironmentSatisfaction + RelationshipSatisfaction)
Range: 1.0 (fully disengaged) → 4.0 (fully engaged)
```

### Burnout Risk Classification
```
OvertimeFlag  = 1 if OverTime == 'Yes'  else 0
LowWLBFlag    = 1 if WorkLifeBalance <= 2  else 0
BurnoutScore  = OvertimeFlag + LowWLBFlag

Score 0 → Low Risk   (51.4% of workforce)
Score 1 → Medium Risk (40.0% of workforce)
Score 2 → High Risk   ( 8.6% of workforce)
```

---

## 💡 Key Recommendations

1. **Overtime Thresholds** — Cap sustained overtime; high-risk for attrition
2. **Medium-Risk Program** — Target 588 medium-risk employees proactively
3. **Role Rotation Triggers** — Flag employees stagnant 3+ years in same role
4. **Travel Policy Review** — Audit compound stressor (overtime + frequent travel)
5. **Promotion Cadence** — Review employees with 5+ years since last promotion
6. **Manager Coaching** — Relationship Satisfaction is the lowest-scoring dimension

---

## 📄 Research Paper

**Title:** Employee Engagement, Satisfaction, and Burnout Diagnostic Analysis at Palo Alto Networks

**Author:** Pranali Ananta Paturkar

**Published in:** IJIRT — International Journal of Innovative Research and Technology
- ISSN: 2349-6002
- Impact Factor: 8.412 (2026)
- UGC-Compliant Peer Reviewed Journal

---

## 👩‍💻 Author

**Pranali Ananta Paturkar**

[![Email](https://img.shields.io/badge/Email-Pranaliturankar95%40gmail.com-red?style=flat&logo=gmail)](mailto:Pranaliturankar95@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Pranali%20Paturkar-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/pranali-paturkar-942900106)
[![GitHub](https://img.shields.io/badge/GitHub-pranu--16-black?style=flat&logo=github)](https://github.com/pranu-16)

---

## 📃 License

This project is open source and available under the [MIT License](LICENSE).

---

⭐ **If you found this project helpful, please give it a star!** ⭐
