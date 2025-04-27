from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

def generate_report(image_path, analysis_results, output_path):
    """
    Generate a PDF report for image forgery analysis
    
    Args:
        image_path (str): Path to the analyzed image
        analysis_results (dict): Results from the forgery analysis
        output_path (str): Path where the PDF should be saved
    """
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Container for PDF elements
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    
    # Add title
    elements.append(Paragraph("Image Forgery Detection Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Add timestamp
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    # Add image
    if os.path.exists(image_path):
        img = Image(image_path, width=4*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 12))
    
    # Add metadata section
    elements.append(Paragraph("Metadata Analysis", styles['Heading2']))
    if 'metadata' in analysis_results:
        metadata = analysis_results['metadata']
        metadata_data = [
            ["Property", "Value"],
            ["Has EXIF", str(metadata.get('has_exif', 'N/A'))],
            ["Camera Make", metadata.get('make', 'N/A')],
            ["Camera Model", metadata.get('model', 'N/A')],
            ["Date/Time", metadata.get('datetime', 'N/A')],
            ["Software", metadata.get('software', 'N/A')]
        ]
        metadata_table = Table(metadata_data, colWidths=[2*inch, 3*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(metadata_table)
    elements.append(Spacer(1, 12))
    
    # Add forgery detection results
    elements.append(Paragraph("Forgery Detection Results", styles['Heading2']))
    if 'forgery_detection' in analysis_results:
        forgery = analysis_results['forgery_detection']
        forgery_data = [
            ["Analysis Type", "Result"],
            ["ML Confidence", f"{forgery.get('ml_confidence', 'N/A')}"],
            ["Compression Artifacts", str(forgery.get('compression_artifacts', 'N/A'))],
            ["Suspicious Regions", str(forgery.get('suspicious_regions', 'N/A'))]
        ]
        forgery_table = Table(forgery_data, colWidths=[2*inch, 3*inch])
        forgery_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(forgery_table)
    elements.append(Spacer(1, 12))
    
    # Add region analysis
    elements.append(Paragraph("Region Analysis", styles['Heading2']))
    if 'region_analysis' in analysis_results and 'regions' in analysis_results['region_analysis']:
        regions = analysis_results['region_analysis']['regions']
        region_data = [["Region ID", "Position", "Mean", "Std Dev", "Entropy"]]
        for region in regions:
            pos = region['position']
            stats = region['statistics']
            region_data.append([
                str(region['region_id']),
                f"({pos['x']}, {pos['y']})",
                f"{stats['mean']:.2f}",
                f"{stats['std']:.2f}",
                f"{stats['entropy']:.2f}"
            ])
        region_table = Table(region_data, colWidths=[0.5*inch, 1.5*inch, inch, inch, inch])
        region_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(region_table)
    
    # Add conclusion
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Conclusion", styles['Heading2']))
    
    # Generate conclusion text based on analysis results
    conclusion_text = "Based on the analysis: "
    if 'forgery_detection' in analysis_results:
        forgery = analysis_results['forgery_detection']
        if forgery.get('ml_confidence', 0) > 0.7:
            conclusion_text += "The image shows strong signs of manipulation. "
        elif forgery.get('ml_confidence', 0) > 0.3:
            conclusion_text += "The image may have been manipulated. "
        else:
            conclusion_text += "No significant signs of manipulation were detected. "
            
        if forgery.get('compression_artifacts'):
            conclusion_text += "Compression artifacts were detected, suggesting possible editing. "
        if forgery.get('suspicious_regions'):
            conclusion_text += "Suspicious regions were identified that may indicate tampering. "
    
    elements.append(Paragraph(conclusion_text, styles['Normal']))
    
    # Build the PDF
    doc.build(elements)
    
    return output_path 