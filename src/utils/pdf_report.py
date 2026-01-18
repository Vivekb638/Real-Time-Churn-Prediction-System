from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch

import matplotlib.pyplot as plt
from io import BytesIO


def _create_risk_chart_image(summary_df):
    """
    Create bar chart and return it as BytesIO (NO FILE SYSTEM)
    """
    fig, ax = plt.subplots(figsize=(5, 3))

    ax.bar(
        summary_df["risk_segment"],
        summary_df["customers"],
        color=["#22c55e", "#f59e0b", "#ef4444"]
    )

    ax.set_title("Customer Risk Distribution")
    ax.set_xlabel("Risk Segment")
    ax.set_ylabel("Customers")

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png", dpi=200)
    plt.close(fig)

    buffer.seek(0)
    return buffer


def generate_churn_pdf(company_info, summary_df, output_path):
    """
    Generate enterprise churn intelligence PDF (SAFE VERSION)
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    elements = []

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------
    elements.append(
        Paragraph("<b>Customer Churn Decision Intelligence Report</b>", styles["Title"])
    )
    elements.append(Spacer(1, 0.2 * inch))

    # --------------------------------------------------
    # COMPANY INFO
    # --------------------------------------------------
    elements.append(Paragraph("<b>Company Details</b>", styles["Heading2"]))

    company_table = Table(
        [
            ["Company Name", company_info.get("name", "-")],
            ["Location", company_info.get("location", "-")],
            ["Email", company_info.get("email", "-")],
            ["Website", company_info.get("website", "-")],
        ],
        colWidths=[2.2 * inch, 3.5 * inch],
    )

    company_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )

    elements.append(company_table)
    elements.append(Spacer(1, 0.3 * inch))

    # --------------------------------------------------
    # SUMMARY TABLE
    # --------------------------------------------------
    elements.append(Paragraph("<b>Portfolio Risk Summary</b>", styles["Heading2"]))

    table_data = [["Risk Segment", "Customers", "Revenue at Risk ($)"]]

    for _, row in summary_df.iterrows():
        table_data.append(
            [
                row["risk_segment"],
                int(row["customers"]),
                f"${row['revenue_at_risk']:,.0f}",
            ]
        )

    summary_table = Table(table_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
            ]
        )
    )

    elements.append(summary_table)
    elements.append(Spacer(1, 0.4 * inch))

    # --------------------------------------------------
    # CHART (IN-MEMORY IMAGE)
    # --------------------------------------------------
    elements.append(Paragraph("<b>Risk Distribution Chart</b>", styles["Heading2"]))

    chart_buffer = _create_risk_chart_image(summary_df)

    elements.append(
        Image(
            chart_buffer,
            width=4.8 * inch,
            height=3 * inch,
        )
    )

    elements.append(Spacer(1, 0.3 * inch))

    # --------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------
    elements.append(Paragraph("<b>Executive Insights</b>", styles["Heading2"]))

    elements.append(
        Paragraph(
            """
            This report identifies customer churn risk across the portfolio.
            High-risk customers should be prioritized for retention offers,
            medium-risk customers monitored closely, and low-risk customers
            targeted for upsell opportunities.
            """,
            styles["BodyText"],
        )
    )

    # --------------------------------------------------
    # BUILD PDF
    # --------------------------------------------------
    doc.build(elements)
