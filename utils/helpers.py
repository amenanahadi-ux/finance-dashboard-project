import streamlit as st

def format_currency(amount: float, symbol: str = "₹") -> str:
    """
    Formats a numeric float as a localized currency string.
    """
    if amount is None:
        return f"{symbol}0.00"
    if amount < 0:
        return f"-{symbol}{abs(amount):,.2f}"
    return f"{symbol}{amount:,.2f}"

def inject_custom_css():
    """
    Injects custom CSS stylesheets into Streamlit to create a premium,
    modern user interface with custom fonts, glassmorphism, cards, and transitions.
    """
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        
        <style>
            /* Apply custom typography */
            html, body, [class*="css"], .stApp {
                font-family: 'Outfit', sans-serif !important;
            }

            /* Custom background style if needed, Streamlit's natural theme matches well */
            .stApp {
                background-attachment: fixed;
            }

            /* Sleek Dashboard KPI Cards */
            .kpi-card {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                padding: 24px;
                margin: 10px 0;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .kpi-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.25);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .kpi-title {
                font-size: 14px;
                font-weight: 500;
                color: #a0aec0;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                margin-bottom: 8px;
            }

            .kpi-value {
                font-size: 28px;
                font-weight: 700;
                background: linear-gradient(to right, #ffffff, #cbd5e0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 4px;
            }

            .kpi-subtitle {
                font-size: 12px;
                color: #718096;
            }

            /* Gradient text for titles */
            .gradient-text {
                background: linear-gradient(135deg, #1e88e5, #00b0ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 800;
            }

            /* Custom styling for metrics */
            div[data-testid="stMetricValue"] {
                font-size: 2rem;
                font-weight: 700;
            }
            
            div[data-testid="stMetricLabel"] {
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            /* Smooth Sidebar changes */
            .sidebar .sidebar-content {
                background: #111;
            }
            
            /* Add subtle border styling to stSidebar */
            section[data-testid="stSidebar"] {
                border-right: 1px solid rgba(128, 128, 128, 0.15);
            }

            /* Styling tables to look cleaner */
            .dataframe {
                border-collapse: collapse;
                width: 100% !important;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            }
            
            .dataframe th {
                background-color: rgba(255,255,255,0.05) !important;
                font-weight: 600 !important;
                padding: 12px !important;
            }
            
            .dataframe td {
                padding: 10px !important;
            }

            /* Custom status pill styles */
            .status-pill {
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
                display: inline-block;
            }
            
            .status-over {
                background-color: rgba(231, 76, 60, 0.15);
                color: #e74c3c;
                border: 1px solid rgba(231, 76, 60, 0.3);
            }
            
            .status-under {
                background-color: rgba(46, 204, 113, 0.15);
                color: #2ecc71;
                border: 1px solid rgba(46, 204, 113, 0.3);
            }

            .status-none {
                background-color: rgba(127, 140, 141, 0.15);
                color: #95a5a6;
                border: 1px solid rgba(127, 140, 141, 0.3);
            }

            /* Responsive tweaks */
            @media (max-width: 768px) {
                .kpi-value {
                    font-size: 22px;
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )
