"""
Custom SaaS CSS styles for Student360 AI
"""

def apply_custom_styles():
    import streamlit as st
    st.markdown("""
    <style>
    /* Global Styles & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header Styling */
    .app-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.15);
    }
    .app-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .app-header p {
        font-size: 1.05rem;
        opacity: 0.9;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }

    /* SaaS Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.08);
    }
    .metric-card .label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #6B7280;
        letter-spacing: 0.05em;
    }
    .metric-card .value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
        margin-top: 0.3rem;
    }

    /* Career Readiness Badge Gauge */
    .gauge-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.2);
    }
    .gauge-score {
        font-size: 4rem;
        font-weight: 800;
        line-height: 1;
        background: linear-gradient(135deg, #60A5FA 0%, #34D399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .gauge-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #94A3B8;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Alert Cards */
    .alert-warning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 1rem 1.25rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        color: #92400E;
    }
    .alert-danger {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
        padding: 1rem 1.25rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        color: #991B1B;
    }
    .alert-success {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        padding: 1rem 1.25rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        color: #065F46;
    }

    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 9999px;
        text-transform: uppercase;
    }
    .badge-high { background-color: #FEE2E2; color: #991B1B; }
    .badge-medium { background-color: #FEF3C7; color: #92400E; }
    .badge-low { background-color: #E0E7FF; color: #3730A3; }
    .badge-verified { background-color: #D1FAE5; color: #065F46; }

    </style>
    """, unsafe_allow_html=True)
