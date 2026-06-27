import os
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf_report(df: pd.DataFrame, kpis: dict, insights: list, budgets: dict, ml_results: dict, output_pdf_path: str):
    """
    Generates a professional financial analytics PDF report.
    """
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    
    # Page setup - letter size, 0.5 inch margins
    margin = 0.5 * inch
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#7f8c8d'),
        spaceAfter=15
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#2c3e50'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )
    
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=1 # Center
    )
    
    td_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#2c3e50')
    )
    
    td_bold_style = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#2c3e50')
    )

    story = []

    # Title & Metadata Header
    story.append(Paragraph("Personal Finance Analytics Report", title_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | Source: Financial Transaction History", subtitle_style))
    story.append(Spacer(1, 10))

    # Section 1: Executive KPI Summary
    story.append(Paragraph("1. Executive Summary KPIs", section_title_style))
    
    # 3x3 KPI Layout using Table
    kpi_data = [
        [
            Paragraph("<b>Total Income</b><br/>₹{:,.2f}".format(kpis["total_income"]), body_style),
            Paragraph("<b>Total Expenses</b><br/>₹{:,.2f}".format(kpis["total_expense"]), body_style),
            Paragraph("<b>Net Savings</b><br/>₹{:,.2f}".format(kpis["net_savings"]), body_style)
        ],
        [
            Paragraph("<b>Savings Rate</b><br/>{:.1f}%".format(kpis["savings_rate"]), body_style),
            Paragraph("<b>Total Transactions</b><br/>{:,}".format(kpis["total_transactions"]), body_style),
            Paragraph(f"<b>Largest Expense Category</b><br/>{kpis['largest_expense_category']}", body_style)
        ],
        [
            Paragraph("<b>Avg Monthly Income</b><br/>₹{:,.2f}".format(kpis["avg_monthly_income"]), body_style),
            Paragraph("<b>Avg Monthly Expense</b><br/>₹{:,.2f}".format(kpis["avg_monthly_expense"]), body_style),
            Paragraph(f"<b>Highest Spending Month</b><br/>{kpis['highest_spending_month']}", body_style)
        ]
    ]
    
    # KPI Grid Table Styling
    kpi_table = Table(kpi_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 15))

    # Section 2: Automated Insights
    story.append(Paragraph("2. Financial Insights & Observations", section_title_style))
    # Clean and format insights for ReportLab's Paragraph parser
    for ins in insights:
        # 1. Handle bold format: alternate between <b> and </b>
        parts = ins.split("**")
        bold_formatted = []
        for idx, part in enumerate(parts):
            if idx % 2 == 1:
                bold_formatted.append(f"<b>{part}</b>")
            else:
                bold_formatted.append(part)
        formatted_ins = "".join(bold_formatted)
        
        # 2. Handle italic format: alternate between <i> and </i>
        parts = formatted_ins.split("*")
        italic_formatted = []
        for idx, part in enumerate(parts):
            if idx % 2 == 1:
                italic_formatted.append(f"<i>{part}</i>")
            else:
                italic_formatted.append(part)
        formatted_ins = "".join(italic_formatted)
        
        # 3. Strip emojis which are incompatible with standard Helvetica fonts
        emojis = ["🌟", "👍", "⚠️", "🚨", "📈", "📉", "⚖️", "🛍️", "⚡", "🔍", "🔄", "🛡️"]
        for emo in emojis:
            formatted_ins = formatted_ins.replace(emo, "")
        
        # Strip any extra leading/trailing whitespace left after emojis
        formatted_ins = formatted_ins.strip()
        
        story.append(Paragraph(f"• {formatted_ins}", bullet_style))
    story.append(Spacer(1, 15))

    # Section 3: Budget Analysis
    story.append(Paragraph("3. Budget Variance Performance", section_title_style))
    
    # Build Budget Table
    # Find actual spending by category
    expense_df = df[df["Transaction Type"] == "Expense"]
    actual_spending = expense_df.groupby("Category")["Amount"].sum().to_dict()
    
    budget_table_data = [
        [
            Paragraph("Category", th_style), 
            Paragraph("Budget Limit (₹)", th_style), 
            Paragraph("Actual Spent (₹)", th_style), 
            Paragraph("Remaining (₹)", th_style), 
            Paragraph("Usage Status", th_style)
        ]
    ]

    all_categories = sorted(list(set(list(budgets.keys()) + list(actual_spending.keys()))))
    
    total_budget_limit = 0.0
    total_actual_spent = 0.0
    
    for cat in all_categories:
        limit = budgets.get(cat, 0.0)
        actual = actual_spending.get(cat, 0.0)
        remaining = limit - actual
        
        total_budget_limit += limit
        total_actual_spent += actual
        
        if limit == 0:
            status = "No Limit Set"
            status_color = "#7f8c8d"
        elif remaining < 0:
            status = f"Over budget ({(abs(remaining)/limit*100):.1f}%)"
            status_color = "#e74c3c"
        else:
            status = f"Under budget ({((actual)/limit*100):.1f}%)"
            status_color = "#2ecc71"
            
        budget_table_data.append([
            Paragraph(cat, td_style),
            Paragraph(f"₹{limit:,.2f}" if limit > 0 else "—", td_style),
            Paragraph(f"₹{actual:,.2f}", td_style),
            Paragraph(f"₹{remaining:,.2f}" if limit > 0 else "—", td_style),
            Paragraph(f"<font color='{status_color}'><b>{status}</b></font>", td_style)
        ])
        
    # Total row
    budget_table_data.append([
        Paragraph("<b>Total</b>", td_bold_style),
        Paragraph(f"<b>₹{total_budget_limit:,.2f}</b>" if total_budget_limit > 0 else "—", td_bold_style),
        Paragraph(f"<b>₹{total_actual_spent:,.2f}</b>", td_bold_style),
        Paragraph(f"<b>₹{total_budget_limit - total_actual_spent:,.2f}</b>" if total_budget_limit > 0 else "—", td_bold_style),
        Paragraph("", td_bold_style)
    ])
    
    budget_table = Table(budget_table_data, colWidths=[2.0*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.6*inch])
    budget_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 4),
        ('TOPPADDING', (0,1), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
        ('BACKGROUND', (0,1), (-1,-2), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#eaeded')),
    ]))
    story.append(budget_table)
    story.append(Spacer(1, 15))

    # Section 4: Machine Learning Forecast
    story.append(Paragraph("4. Machine Learning Expense Forecasting", section_title_style))
    
    if ml_results.get("success", False):
        best_model = ml_results["best_model_name"]
        next_month = ml_results["next_month"]
        lr_fc = ml_results["lr_forecast"]
        rf_fc = ml_results["rf_forecast"]
        
        forecast_intro = f"Predictive analytics model trained on the monthly aggregated transaction history. " \
                         f"The recommended model is <b>{best_model}</b> based on evaluation testing metrics."
        story.append(Paragraph(forecast_intro, body_style))
        story.append(Spacer(1, 5))
        
        # Forecast Summary Block
        forecast_metrics_data = [
            [
                Paragraph("<b>Forecast Period</b>", td_bold_style),
                Paragraph(next_month, td_style)
            ],
            [
                Paragraph("<b>Linear Regression Forecast</b>", td_bold_style),
                Paragraph(f"₹{lr_fc:,.2f}", td_style)
            ],
            [
                Paragraph("<b>Random Forest Forecast</b>", td_bold_style),
                Paragraph(f"₹{rf_fc:,.2f}", td_style)
            ],
            [
                Paragraph("<b>Best Performing Model Selected</b>", td_bold_style),
                Paragraph(f"<font color='#3498db'><b>{best_model}</b></font>", td_bold_style)
            ]
        ]
        
        fc_table = Table(forecast_metrics_data, colWidths=[2.5*inch, 5.0*inch])
        fc_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
            ('PADDING', (0,0), (-1,-1), 6),
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8f9fa')),
        ]))
        story.append(fc_table)
        story.append(Spacer(1, 10))
        
        # Models performance metrics
        metrics = ml_results["metrics"]
        metrics_table_data = [
            [
                Paragraph("Model Engine", th_style),
                Paragraph("Mean Absolute Error (MAE)", th_style),
                Paragraph("Root Mean Squared Error (RMSE)", th_style),
                Paragraph("R² Coefficient", th_style)
            ],
            [
                Paragraph("Linear Regression", td_style),
                Paragraph(f"₹{metrics['lr']['MAE']:,.2f}", td_style),
                Paragraph(f"₹{metrics['lr']['RMSE']:,.2f}", td_style),
                Paragraph(f"{metrics['lr']['R2']:.4f}", td_style)
            ],
            [
                Paragraph("Random Forest Regressor", td_style),
                Paragraph(f"₹{metrics['rf']['MAE']:,.2f}", td_style),
                Paragraph(f"₹{metrics['rf']['RMSE']:,.2f}", td_style),
                Paragraph(f"{metrics['rf']['R2']:.4f}", td_style)
            ]
        ]
        
        m_table = Table(metrics_table_data, colWidths=[2.0*inch, 2.0*inch, 2.0*inch, 1.5*inch])
        m_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#34495e')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#bdc3c7')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('PADDING', (0,0), (-1,-1), 5),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        story.append(Paragraph("<b>Model Performance Metrics Comparison:</b>", body_style))
        story.append(Spacer(1, 4))
        story.append(m_table)
    else:
        # Check why it failed
        fail_msg = ml_results.get("message", "Insufficient historical monthly points to execute machine learning models. Please build a history of 6 months or more.")
        story.append(Paragraph(f"<i>Note: {fail_msg}</i>", body_style))
        
    doc.build(story)
