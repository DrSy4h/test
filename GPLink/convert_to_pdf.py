#!/usr/bin/env python3
"""
Convert CRUD_GUIDE_BM.md to PDF
"""

import markdown2
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import re

# Read markdown file
with open('CRUD_GUIDE_BM.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Create PDF
pdf_filename = "CRUD_GUIDE_BM.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                        rightMargin=0.5*inch, leftMargin=0.5*inch,
                        topMargin=0.75*inch, bottomMargin=0.75*inch)

# Container for PDF elements
story = []

# Define styles
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#9A7D61'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#9A7D61'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontSize=13,
    textColor=colors.HexColor('#7D6450'),
    spaceAfter=10,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    leading=14
)

code_style = ParagraphStyle(
    'Code',
    parent=styles['Normal'],
    fontSize=8,
    fontName='Courier',
    textColor=colors.HexColor('#333333'),
    spaceAfter=6,
    leftIndent=20,
    rightIndent=20,
    backColor=colors.HexColor('#F5F5F5')
)

# Parse markdown and build PDF content
lines = md_content.split('\n')
i = 0
code_block = False
code_lines = []

while i < len(lines):
    line = lines[i]
    
    # Skip empty lines at start
    if not line.strip() and len(story) == 0:
        i += 1
        continue
    
    # Title
    if line.startswith('# '):
        title = line.replace('# ', '').strip()
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 0.3*inch))
    
    # Heading 1
    elif line.startswith('## '):
        heading = line.replace('## ', '').strip()
        story.append(Paragraph(heading, heading1_style))
        story.append(Spacer(1, 0.1*inch))
    
    # Heading 2
    elif line.startswith('### '):
        heading = line.replace('### ', '').strip()
        story.append(Paragraph(heading, heading2_style))
    
    # Code block
    elif line.startswith('```'):
        code_block = not code_block
        if not code_block and code_lines:
            # End of code block
            code_text = '\n'.join(code_lines)
            story.append(Spacer(1, 0.1*inch))
            story.append(Preformatted(code_text, code_style))
            story.append(Spacer(1, 0.1*inch))
            code_lines = []
        i += 1
        continue
    
    elif code_block:
        code_lines.append(line)
    
    # Table marker
    elif line.startswith('| ') and '|' in line:
        # Simple table parsing
        table_rows = []
        while i < len(lines) and '|' in lines[i]:
            cells = [cell.strip() for cell in lines[i].split('|')[1:-1]]
            table_rows.append(cells)
            i += 1
        
        if table_rows:
            # Create table
            t = Table(table_rows, colWidths=[1.2*inch]*len(table_rows[0]))
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9A7D61')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            story.append(Spacer(1, 0.1*inch))
            story.append(t)
            story.append(Spacer(1, 0.1*inch))
        
        continue
    
    # Regular text
    elif line.strip() and not line.startswith('#') and not code_block:
        # Check for bullet points
        if line.strip().startswith('-'):
            bullet_text = line.strip()[2:]
            bullet = Paragraph(f"• {bullet_text}", body_style)
            story.append(bullet)
        elif line.strip().startswith('*'):
            bullet_text = line.strip()[2:]
            bullet = Paragraph(f"• {bullet_text}", body_style)
            story.append(bullet)
        else:
            story.append(Paragraph(line.strip(), body_style))
    
    # Page break markers
    elif '---' in line:
        story.append(Spacer(1, 0.2*inch))
    
    i += 1

# Add footer
story.append(Spacer(1, 0.3*inch))
footer = Paragraph("<i>GPLink Cardio™ | DRAHMADSYAHID © 2025</i>", body_style)
story.append(footer)

# Build PDF
try:
    doc.build(story)
    print(f"✅ PDF created successfully: {pdf_filename}")
except Exception as e:
    print(f"❌ Error creating PDF: {e}")
