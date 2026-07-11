import streamlit as st
import pandas as pd
from io import BytesIO, StringIO

# Try to import reportlab for PDF generation
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def get_export_section(df, schema, metrics, summary, page_name="Executive Overview"):
    """
    Renders a unified export section for any dashboard page.
    """

    st.divider()
    st.subheader("📥 Export Reports")

    col1, col2, col3 = st.columns(3)

    # ── CSV Export ──
    with col1:
        st.markdown("**CSV Data**")
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="Download Dataset (CSV)",
            data=csv_data,
            file_name=f"{page_name.lower().replace(' ', '_')}_data.csv",
            mime="text/csv",
            use_container_width=True
        )

        # KPIs as CSV
        kpi_df = pd.DataFrame([metrics])
        kpi_buffer = StringIO()
        kpi_df.to_csv(kpi_buffer, index=False)

        st.download_button(
            label="Download KPIs (CSV)",
            data=kpi_buffer.getvalue(),
            file_name=f"{page_name.lower().replace(' ', '_')}_kpis.csv",
            mime="text/csv",
            use_container_width=True
        )

    # ── TXT Export ──
    with col2:
        st.markdown("**Text Reports**")

        # Executive Summary TXT
        st.download_button(
            label="Download Summary (TXT)",
            data=summary,
            file_name=f"{page_name.lower().replace(' ', '_')}_summary.txt",
            mime="text/plain",
            use_container_width=True
        )

        # Full Report TXT
        full_report_lines = [
            "=" * 60,
            f"BUSINESS ANALYTICS REPORT — {page_name.upper()}",
            "=" * 60,
            "",
            "DATASET OVERVIEW",
            "----------------",
            f"Total Rows: {len(df):,}",
            f"Total Columns: {len(df.columns)}",
            f"Detected Schema: {schema}",
            "",
            "KEY PERFORMANCE INDICATORS",
            "--------------------------"
        ]

        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                if "revenue" in key.lower() or "value" in key.lower():
                    formatted = f"${value:,.2f}"
                else:
                    formatted = f"{value:,.1f}"
            else:
                formatted = str(value)
            full_report_lines.append(f"  {key.replace('_', ' ').title()}: {formatted}")

        full_report_lines.extend([
            "",
            "EXECUTIVE SUMMARY",
            "-" * 40,
            summary,
            "",
            "=" * 60,
            "END OF REPORT",
            "=" * 60,
            ""
        ])

        full_report = "\n".join(full_report_lines)

        st.download_button(
            label="Download Full Report (TXT)",
            data=full_report,
            file_name=f"{page_name.lower().replace(' ', '_')}_full_report.txt",
            mime="text/plain",
            use_container_width=True
        )

    # ── PDF Export ──
    with col3:
        st.markdown("**PDF Reports**")

        if REPORTLAB_AVAILABLE:
            pdf_buffer = generate_pdf_report(df, schema, metrics, summary, page_name)

            st.download_button(
                label="Download PDF Report",
                data=pdf_buffer,
                file_name=f"{page_name.lower().replace(' ', '_')}_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.info("Install `reportlab` for PDF export:")
            st.code("pip install reportlab", language="bash")

            # Offer HTML as alternative
            html_report = generate_html_report(df, schema, metrics, summary, page_name)
            st.download_button(
                label="Download HTML Report",
                data=html_report,
                file_name=f"{page_name.lower().replace(' ', '_')}_report.html",
                mime="text/html",
                use_container_width=True
            )


def generate_pdf_report(df, schema, metrics, summary, page_name):
    """
    Generate a professional PDF report using ReportLab.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )

    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f1f1f'),
        spaceAfter=30,
        alignment=1
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#0068c9'),
        spaceAfter=12,
        spaceBefore=12
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        spaceAfter=6
    )

    # Title
    elements.append(Paragraph("Business Analytics Report", title_style))
    elements.append(Paragraph(page_name, heading_style))
    elements.append(Spacer(1, 0.2*inch))

    # Dataset Info
    elements.append(Paragraph("Dataset Overview", heading_style))
    elements.append(Paragraph(f"Total Records: {len(df):,}", body_style))
    elements.append(Paragraph(f"Total Columns: {len(df.columns)}", body_style))
    elements.append(Spacer(1, 0.1*inch))

    # KPI Table
    elements.append(Paragraph("Key Performance Indicators", heading_style))

    kpi_data = [["Metric", "Value"]]
    for key, value in metrics.items():
        metric_name = key.replace('_', ' ').title()
        if isinstance(value, (int, float)):
            if "revenue" in key.lower() or "value" in key.lower() or "price" in key.lower():
                formatted = f"${value:,.2f}"
            else:
                formatted = f"{value:,.1f}"
        else:
            formatted = str(value)
        kpi_data.append([metric_name, formatted])

    kpi_table = Table(kpi_data, colWidths=[3*inch, 2*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0068c9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(1, 0.2*inch))

    # Executive Summary
    elements.append(Paragraph("Executive Summary", heading_style))
    clean_summary = summary.replace('\n', '<br/>').replace('  ', '&nbsp;&nbsp;')
    elements.append(Paragraph(clean_summary, body_style))
    elements.append(Spacer(1, 0.2*inch))

    # Schema Detection
    elements.append(Paragraph("Detected Schema", heading_style))
    schema_data = [["Field", "Column Name"]]
    for field, col_name in schema.items():
        schema_data.append([field.title(), col_name or "Not Found"])

    schema_table = Table(schema_data, colWidths=[2*inch, 3*inch])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#29b09d')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    elements.append(schema_table)

    # Footer
    elements.append(Spacer(1, 0.3*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph("Generated by Automated Business Insight Generator", footer_style))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def generate_html_report(df, schema, metrics, summary, page_name):
    """
    Generate an HTML report as fallback when ReportLab is not available.
    """

    kpi_rows = ""
    for key, value in metrics.items():
        metric_name = key.replace('_', ' ').title()
        if isinstance(value, (int, float)):
            if "revenue" in key.lower() or "value" in key.lower():
                formatted = f"${value:,.2f}"
            else:
                formatted = f"{value:,.1f}"
        else:
            formatted = str(value)
        kpi_rows += f"<tr><td>{metric_name}</td><td>{formatted}</td></tr>\n"

    schema_rows = ""
    for field, col_name in schema.items():
        schema_rows += f"<tr><td>{field.title()}</td><td>{col_name or 'Not Found'}</td></tr>\n"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Business Analytics Report — {page_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #1f1f1f; border-bottom: 3px solid #0068c9; padding-bottom: 10px; }}
        h2 {{ color: #0068c9; margin-top: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #0068c9; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #dee2e6; }}
        tr:nth-child(even) {{ background: #f8f9fa; }}
        .summary {{ background: #f8f9fa; padding: 20px; border-left: 4px solid #0068c9; white-space: pre-wrap; font-family: monospace; }}
        .footer {{ text-align: center; color: #666; margin-top: 40px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Business Analytics Report</h1>
        <h2>{page_name}</h2>

        <h2>Dataset Overview</h2>
        <p><strong>Total Records:</strong> {len(df):,}</p>
        <p><strong>Total Columns:</strong> {len(df.columns)}</p>

        <h2>Key Performance Indicators</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            {kpi_rows}
        </table>

        <h2>Executive Summary</h2>
        <div class="summary">{summary}</div>

        <h2>Detected Schema</h2>
        <table>
            <tr><th>Field</th><th>Column Name</th></tr>
            {schema_rows}
        </table>

        <div class="footer">
            Generated by Automated Business Insight Generator
        </div>
    </div>
</body>
</html>"""

    return html