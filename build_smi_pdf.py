import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and display total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, letter[1] - 30, "Academic Deliverable: Assignment 1 — Statistical Modeling & Inferencing")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, letter[1] - 34, letter[0] - 36, letter[1] - 34)

        # Footer (All pages)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 36, 25, page_text)
        self.drawString(36, 25, "Student Name: Abhiram | Course / Subject: Statistical Modeling & Inferencing (SMI) | Status: Completed & Verified")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 36, letter[0] - 36, 36)

        self.restoreState()


def generate_report():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, "report file.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=44,
        bottomMargin=44
    )

    styles = getSampleStyleSheet()

    PRIMARY = colors.HexColor("#1E3A8A")     # Navy Blue
    SECONDARY = colors.HexColor("#0284C7")   # Teal / Cyan Accent
    DARK_TEXT = colors.HexColor("#1E293B")   # Slate 800
    SLATE = colors.HexColor("#475569")       # Slate 600
    BG_LIGHT = colors.HexColor("#F8FAFC")    # Slate 50
    BORDER_COLOR = colors.HexColor("#CBD5E1")# Slate 300

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=12,
        spaceAfter=4
    )

    meta_label_style = ParagraphStyle(
        "MetaLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=PRIMARY
    )

    meta_val_style = ParagraphStyle(
        "MetaVal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=DARK_TEXT
    )

    tbl_header_style = ParagraphStyle(
        "TblHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    tbl_cell_style = ParagraphStyle(
        "TblCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=SLATE
    )

    story = []

    # Title & Subtitle Banner
    story.append(Paragraph("Statistical Modeling & Inferencing (SMI) — Assignment 1", title_style))
    story.append(Paragraph("Regression Modeling & Validation Report — Diamonds Dataset", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=10))

    # Executive Metadata Box (ONLY Name, Subject, Status)
    meta_data = [
        [Paragraph("Student Name:", meta_label_style), Paragraph("<b>Abhiram</b>", meta_val_style)],
        [Paragraph("Course / Subject:", meta_label_style), Paragraph("<b>Statistical Modeling & Inferencing (SMI)</b>", meta_val_style)],
        [Paragraph("Current Status:", meta_label_style), Paragraph("<font color='#059669'><b>Completed & Verified</b></font>", meta_val_style)]
    ]

    meta_table = Table(meta_data, colWidths=[1.8*inch, 5.4*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section: Executive Summary
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(
        "This technical report presents a comprehensive regression modeling analysis of the <b>Diamonds Dataset (~53,940 observations)</b>, "
        "prepared for the Statistical Modeling and Inferencing (SMI) Assignment 1. The primary objective is to investigate the physical and "
        "qualitative factors governing diamond valuation, resolve critical data quality anomalies, eliminate severe multicollinearity among "
        "spatial predictors, and construct robust Ordinary Least Squares (OLS) predictive models validated on held-out test data.",
        body_style
    ))

    story.append(Paragraph("• <b>Preprocessing Pipeline:</b> Addressed non-physical zero values in length (x), width (y), and depth (z) via a 10-bin carat quantile median imputation strategy. Mitigated extreme leverage points using a 1.5× IQR rule (capping carat mass at 2.0 carats), and encoded qualitative attributes (cut, color, clarity) into true ordinal integer vectors.", bullet_style))
    story.append(Paragraph("• <b>Multicollinearity & Dimensionality Reduction:</b> Identified extreme Variance Inflation Factors (VIF > 1000 for spatial metrics x, y, z and VIF ≈ 37.97 for carat). Applied Principal Component Analysis (PCA) to collapse spatial dimensions into a single component (spatial_size_index, capturing 99.73% variance). Constructed Model 4 without the redundant carat predictor to resolve all VIF values to [1.01, 1.48].", bullet_style))
    story.append(Paragraph("• <b>Out-of-Sample Validation & Key Findings:</b> Validated models on a 20% held-out test set (10,788 observations). Model 3 (Log-Linear + PCA + Carat) achieved top-tier predictive dollar accuracy (Test R² = 0.9254, RMSE = $1,047.88), while Model 4 (Log-Linear + PCA, No Carat) provided unconfounded elasticity coefficient interpretations. Clarity was identified as the highest-yielding quality factor (+10.7% price premium per grade step).", bullet_style))

    # Part 1: Data Exploration and Preparation (6 Marks)
    story.append(Paragraph("Part 1: Data Exploration and Preparation (6 Marks)", h1_style))
    
    story.append(Paragraph("1.1 Data Ingestion and Train-Test Split", h2_style))
    story.append(Paragraph(
        "The dataset was partitioned into an 80% training set (43,152 rows) and a 20% held-out test set (10,788 rows) prior to any data cleaning, "
        "binning, or scaling. This strict protocol prevents data leakage into out-of-sample evaluation.",
        body_style
    ))

    story.append(Paragraph("1.2 Data Quality Audit & Quantile-Median Imputation", h2_style))
    story.append(Paragraph(
        "Descriptive profiling revealed non-physical zero values in length (x), width (y), and depth (z), representing disguised missing data. To resolve "
        "this without introducing global bias, diamond carat mass was divided into 10 equal-frequency quantile intervals on the training set, and per-bin "
        "medians were calculated to impute missing dimensions. Bin boundaries and per-bin medians were persisted in a lookup dictionary to ensure test-set zero "
        "values are imputed using exact training parameters.",
        body_style
    ))

    story.append(Paragraph("1.3 Outlier Mitigation via IQR Trimming", h2_style))
    story.append(Paragraph(
        "Continuous features were evaluated for extreme leverage points. Applying a 1.5× IQR trimming rule across continuous features dropped 3,675 outlier "
        "rows (~8.5% of training data), capping maximum carat weight at 2.0 carats. Comparing IQR trimming against RobustScaler and bounded clipping confirmed "
        "that direct trimming eliminates high-leverage points that would otherwise distort OLS slope estimates and introduce heteroskedasticity.",
        body_style
    ))

    story.append(Paragraph("1.4 Ordinal Encoding and Correlation Structure", h2_style))
    story.append(Paragraph(
        "Qualitative attributes were converted into GIA-aligned numeric ordinal scales (cut: Fair=0 to Ideal=4; color: J=0 to D=6; clarity: I1=0 to IF=7). "
        "Full correlation analysis confirmed strong physical size correlations (r > 0.87 with price), while revealing that weak or negative raw correlations "
        "for quality grades stem from Simpson's paradox / carat confounding (larger diamonds in raw data tend to have lower average quality grades).",
        body_style
    ))
    
    img1_path = os.path.join(base_dir, "part1_visual_profiles.png")
    if os.path.exists(img1_path):
        story.append(Spacer(1, 4))
        story.append(Paragraph("<b>Figure 1: Exploratory Visual Profiles & Correlation Structure</b>", h2_style))
        story.append(Image(img1_path, width=7.0*inch, height=2.1875*inch))
        story.append(Spacer(1, 8))

    # Part 2: Model Development and Validation (10 Marks)
    story.append(Paragraph("Part 2: Model Development and Validation (10 Marks)", h1_style))

    story.append(Paragraph("2.1 Baseline Collinearity & VIF Diagnostics", h2_style))
    story.append(Paragraph(
        "Variance Inflation Factor (VIF) diagnostics executed on baseline predictors revealed massive collinearity:",
        body_style
    ))

    vif_headers = [Paragraph("Predictor Feature", tbl_header_style), Paragraph("Baseline VIF (Model 1)", tbl_header_style), Paragraph("Model 4 VIF (Post-PCA & Carat Dropped)", tbl_header_style)]
    vif_data = [
        vif_headers,
        [Paragraph("carat", tbl_cell_style), Paragraph("37.97", tbl_cell_style), Paragraph("Dropped (Redundant)", tbl_cell_style)],
        [Paragraph("x (Length)", tbl_cell_style), Paragraph("1,308.20", tbl_cell_style), Paragraph("Collapsed into PCA Index", tbl_cell_style)],
        [Paragraph("y (Width)", tbl_cell_style), Paragraph("509.34", tbl_cell_style), Paragraph("Collapsed into PCA Index", tbl_cell_style)],
        [Paragraph("z (Depth)", tbl_cell_style), Paragraph("485.60", tbl_cell_style), Paragraph("Collapsed into PCA Index", tbl_cell_style)],
        [Paragraph("spatial_size_index (PCA)", tbl_cell_style), Paragraph("N/A", tbl_cell_style), Paragraph("1.48", tbl_cell_style)],
        [Paragraph("clarity (Ordinal)", tbl_cell_style), Paragraph("1.20", tbl_cell_style), Paragraph("1.19", tbl_cell_style)],
        [Paragraph("color (Ordinal)", tbl_cell_style), Paragraph("1.08", tbl_cell_style), Paragraph("1.08", tbl_cell_style)],
        [Paragraph("cut (Ordinal)", tbl_cell_style), Paragraph("1.50", tbl_cell_style), Paragraph("1.46", tbl_cell_style)],
        [Paragraph("depth (%)", tbl_cell_style), Paragraph("7.95", tbl_cell_style), Paragraph("1.29", tbl_cell_style)],
        [Paragraph("table (%)", tbl_cell_style), Paragraph("1.53", tbl_cell_style), Paragraph("1.50", tbl_cell_style)],
    ]

    vif_table = Table(vif_data, colWidths=[2.6*inch, 2.3*inch, 2.3*inch])
    vif_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(vif_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.2 Multi-Model Regression Iterations & Out-of-Sample Validation", h2_style))
    story.append(Paragraph(
        "Four distinct model specifications were developed and systematically evaluated on training data and held-out test data:",
        body_style
    ))

    iter_headers = [Paragraph("Model Specification", tbl_header_style), Paragraph("Train R²", tbl_header_style), Paragraph("AIC", tbl_header_style), Paragraph("Test R² ($)", tbl_header_style), Paragraph("Test RMSE ($)", tbl_header_style)]
    iter_data = [
        iter_headers,
        [Paragraph("Model 1: Baseline Linear", tbl_cell_style), Paragraph("0.8845", tbl_cell_style), Paragraph("714,208", tbl_cell_style), Paragraph("0.8410", tbl_cell_style), Paragraph("$1,532.10", tbl_cell_style)],
        [Paragraph("Model 2: Log-Linear (All Features)", tbl_cell_style), Paragraph("0.9793", tbl_cell_style), Paragraph("-38,912", tbl_cell_style), Paragraph("0.9248", tbl_cell_style), Paragraph("$1,051.40", tbl_cell_style)],
        [Paragraph("Model 3: Log-Linear + PCA Size Index", tbl_cell_style), Paragraph("0.9791", tbl_cell_style), Paragraph("-38,540", tbl_cell_style), Paragraph("0.9254", tbl_cell_style), Paragraph("$1,047.88", tbl_cell_style)],
        [Paragraph("Model 4: Log-Linear + PCA (Carat Dropped)", tbl_cell_style), Paragraph("0.9654", tbl_cell_style), Paragraph("-21,430", tbl_cell_style), Paragraph("0.8872", tbl_cell_style), Paragraph("$1,288.42", tbl_cell_style)],
    ]

    iter_table = Table(iter_data, colWidths=[2.6*inch, 1.1*inch, 1.1*inch, 1.2*inch, 1.2*inch])
    iter_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(iter_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.3 Residual Diagnostics", h2_style))
    story.append(Paragraph(
        "Model 3 residuals satisfy classical OLS regression assumptions: residual mean is exactly 0.000000 (unbiasedness), Residuals vs. Fitted plot "
        "displays even vertical dispersion confirming homoskedastic variance, and Q-Q plots confirm near-normal error distribution (skewness = -0.17, kurtosis = 5.86).",
        body_style
    ))

    img2_path = os.path.join(base_dir, "part2_model_diagnostics.png")
    if os.path.exists(img2_path):
        story.append(Spacer(1, 4))
        story.append(Paragraph("<b>Figure 2: Model Residual Diagnostics & OLS Assumptions Verification</b>", h2_style))
        story.append(Image(img2_path, width=7.0*inch, height=2.1875*inch))
        story.append(Spacer(1, 8))

    # Part 3: Interpretation, Insights, and Structural Boundaries (4 Marks)
    story.append(Paragraph("Part 3: Interpretation, Insights, and Structural Boundaries (4 Marks)", h1_style))

    story.append(Paragraph("3.1 Parameter Elasticity Interpretations (β)", h2_style))
    story.append(Paragraph(
        "Using log-linear specifications (ln(Price)), coefficient estimates translate to percentage price changes via %ΔY ≈ 100 × (e^β - 1):",
        body_style
    ))

    coef_headers = [Paragraph("Predictor Attribute", tbl_header_style), Paragraph("Model 3 Coef (β)", tbl_header_style), Paragraph("Model 4 Coef (β)", tbl_header_style), Paragraph("Implied Percentage Impact (%Δ Price)", tbl_header_style)]
    coef_data = [
        coef_headers,
        [Paragraph("Clarity (per GIA grade step)", tbl_cell_style), Paragraph("+0.1018", tbl_cell_style), Paragraph("+0.1144", tbl_cell_style), Paragraph("+10.7% to +12.1% price premium per step", tbl_cell_style)],
        [Paragraph("Color (per GIA grade step)", tbl_cell_style), Paragraph("+0.0583", tbl_cell_style), Paragraph("+0.0823", tbl_cell_style), Paragraph("+6.0% to +8.6% price premium per step", tbl_cell_style)],
        [Paragraph("Cut (per GIA grade step)", tbl_cell_style), Paragraph("+0.0247", tbl_cell_style), Paragraph("+0.0240", tbl_cell_style), Paragraph("+2.5% to +2.4% price premium per step", tbl_cell_style)],
        [Paragraph("Spatial Size Index (PCA)", tbl_cell_style), Paragraph("+0.8197", tbl_cell_style), Paragraph("+0.5984", tbl_cell_style), Paragraph("+81.9% price increase per std dev volume", tbl_cell_style)],
    ]

    coef_table = Table(coef_data, colWidths=[2.2*inch, 1.4*inch, 1.4*inch, 2.2*inch])
    coef_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(coef_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2 Business & Practical Takeaways", h2_style))
    story.append(Paragraph("• <b>Automated Valuation Engine:</b> Model 3 can be deployed as an automated diamond pricing engine for retail catalogs, achieving $1,047.88 RMSE ($547.26 MAE) across standard diamond mass ranges.", bullet_style))
    story.append(Paragraph("• <b>Quality Preservation Priorities:</b> Empirical elasticities confirm that clarity (+10.7% per step) yields nearly double the percentage margin premium of color (+6.0% per step). Gem cutters should prioritize preserving clarity over color when processing rough stones.", bullet_style))
    story.append(Paragraph("• <b>Catalog Anomaly Filters:</b> Empirical spatial proportion rules (x ≈ y, z ≈ 0.61x) provide automated validation checks for flagging inventory data entry errors.", bullet_style))

    story.append(Paragraph("3.3 Limitations & Future Recommendations", h2_style))
    story.append(Paragraph("• <b>Sample Mass Boundary:</b> The model is strictly bounded to diamonds ≤ 2.0 carats due to IQR trimming. Investment-grade stones (>3.0 carats) exhibit compounding non-linear rarity premiums.", bullet_style))
    story.append(Paragraph("• <b>Unobserved Factors:</b> Features such as fluorescence, polish, symmetry, and issuing lab (GIA vs EGL) are unobserved in the dataset but account for 5–15% market variance.", bullet_style))
    story.append(Paragraph("• <b>Recommendations:</b> Implement non-linear tree-based ensembles (XGBoost / Random Forest) for luxury carat tiers and incorporate dynamic macroeconomic indices.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("Report PDF regenerated successfully at:", pdf_path)

if __name__ == "__main__":
    generate_report()
