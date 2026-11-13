"""
Generates the Project 01 Cloud Portfolio Manual PDF for students.
Trainer: Sundeep Hiremat
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#5A6578"))

        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 750, 558, 750)
            self.drawString(54, 755, "TASK Telangana · Cloud Software Developer  |  Mini Project 1: Cloud Portfolio")
            self.drawRightString(558, 755, "Trainer: Sundeep Hiremat")

            self.line(54, 45, 558, 45)
            self.drawString(54, 33, "Nalgonda Training Center  |  AWS EC2 Ubuntu 24.04 + Nginx + GitHub")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 33, page_text)

        self.restoreState()

def build_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=54
    )

    styles = getSampleStyleSheet()
    AWS_NAVY = colors.HexColor("#232F3E")
    AWS_ORANGE = colors.HexColor("#FF9900")
    CODE_BG = colors.HexColor("#0F172A")
    LIGHT_BLUE = colors.HexColor("#EFF6FF")

    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=AWS_NAVY, spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=AWS_NAVY,
        spaceBefore=12, spaceAfter=5, keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#1A202C"), spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=12.5, textColor=colors.HexColor("#1A202C"),
        leftIndent=12, firstLineIndent=-8, spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom', parent=styles['Normal'],
        fontName='Courier', fontSize=8, leading=10.5, textColor=colors.HexColor("#F8FAFC"), spaceAfter=3
    )

    story = []

    # Title & Header
    story.append(Paragraph("TASK TELANGANA · CLOUD SOFTWARE DEVELOPER TRAINING", ParagraphStyle(
        'SubHeader', fontName='Helvetica-Bold', fontSize=10, textColor=AWS_ORANGE, spaceAfter=4
    )))
    story.append(Paragraph("Mini Project 1: Deploying a Cloud Portfolio on AWS EC2", title_style))
    story.append(Paragraph("<b>Step-by-Step Hands-on Guide: Ubuntu 24.04 LTS + Nginx + Git + GitHub</b>", ParagraphStyle(
        'Sub', fontName='Helvetica', fontSize=11, leading=14, textColor=colors.HexColor("#475569"), spaceAfter=8
    )))
    story.append(HRFlowable(width="100%", thickness=2, color=AWS_ORANGE, spaceAfter=10))

    meta_text = "<b>Trainer:</b> Sundeep Hiremat &nbsp;|&nbsp; <b>Center:</b> Nalgonda Training Center &nbsp;|&nbsp; <b>Level:</b> Production Lab"
    story.append(Paragraph(meta_text, ParagraphStyle('Meta', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#64748B"), spaceAfter=10)))

    # Callout Box
    callout_data = [
        [Paragraph("<b>PROJECT OBJECTIVE:</b> Every student will launch an enterprise-grade Ubuntu 24.04 LTS instance on AWS Free Tier, configure the high-performance Nginx web server, clone their developer portfolio from GitHub, fix Linux permissions (<code>www-data</code>), and test the live public URL.", ParagraphStyle('Call', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#1E3A8A")))]
    ]
    t_call = Table(callout_data, colWidths=[504])
    t_call.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BLUE),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_call)
    story.append(Spacer(1, 10))

    # Architecture Overview
    story.append(Paragraph("1. System Architecture Flow", h1_style))
    story.append(Paragraph("Internet (Recruiters) ➔ Security Group (Port 80) ➔ Ubuntu EC2 ➔ Nginx ➔ /var/www/html (GitHub Portfolio)", body_style))

    # Steps Table
    story.append(Paragraph("2. Step-by-Step Execution Playbook", h1_style))

    steps_data = [
        [Paragraph("<b>Step #</b>", bullet_style), Paragraph("<b>Action Item</b>", bullet_style), Paragraph("<b>Terminal Commands / Console Actions</b>", bullet_style)],
        [
            Paragraph("<b>1</b>", body_style),
            Paragraph("<b>Launch EC2</b>", body_style),
            Paragraph("• Name: <code>gauri-portfolio</code><br/>• AMI: <b>Ubuntu Server 24.04 LTS</b><br/>• Type: <code>t2.micro</code> or <code>t3.micro</code> (Free Tier)<br/>• Key Pair: Select your key pair<br/>• Auto-assign Public IP: <b>Enable</b><br/>• Security Group: <b>SSH Port 22 (My IP)</b> + <b>HTTP Port 80 (0.0.0.0/0)</b>", body_style)
        ],
        [
            Paragraph("<b>2</b>", body_style),
            Paragraph("<b>Connect</b>", body_style),
            Paragraph("AWS Console ➔ Select Instance ➔ Click <b>Connect</b> ➔ <b>EC2 Instance Connect</b> ➔ Connect as <code>ubuntu</code>.", body_style)
        ],
        [
            Paragraph("<b>3</b>", body_style),
            Paragraph("<b>Update OS</b>", body_style),
            Paragraph("<code>sudo apt update</code><br/><code>sudo apt upgrade -y</code>", body_style)
        ],
        [
            Paragraph("<b>4</b>", body_style),
            Paragraph("<b>Install Tools</b>", body_style),
            Paragraph("<code>sudo apt install git nginx -y</code><br/>Check status: <code>sudo systemctl status nginx</code> (Active: running)", body_style)
        ],
        [
            Paragraph("<b>5</b>", body_style),
            Paragraph("<b>Test Nginx</b>", body_style),
            Paragraph("Open in browser: <code>http://&lt;YOUR_EC2_PUBLIC_IP&gt;</code><br/>Verify the default 'Welcome to nginx!' page loads.", body_style)
        ],
        [
            Paragraph("<b>6</b>", body_style),
            Paragraph("<b>Deploy GitHub Portfolio</b>", body_style),
            Paragraph("<code>cd /var/www/html</code><br/><code>sudo rm -f index.nginx-debian.html</code><br/><code>sudo git clone https://github.com/gauri-abc/gauri-yadav-cloud-portfolio.git .</code><br/><i>(Or clone your own GitHub repository URL)</i>", body_style)
        ],
        [
            Paragraph("<b>7</b>", body_style),
            Paragraph("<b>Fix Permissions</b>", body_style),
            Paragraph("<code>sudo chown -R www-data:www-data /var/www/html</code><br/><code>sudo chmod -R 755 /var/www/html</code>", body_style)
        ],
        [
            Paragraph("<b>8</b>", body_style),
            Paragraph("<b>Restart Nginx</b>", body_style),
            Paragraph("<code>sudo systemctl restart nginx</code><br/><code>sudo systemctl enable nginx</code>", body_style)
        ],
        [
            Paragraph("<b>9</b>", body_style),
            Paragraph("<b>Final Verification</b>", body_style),
            Paragraph("Hard-refresh browser: <code>http://&lt;YOUR_EC2_PUBLIC_IP&gt;</code><br/>Your personal portfolio website is now live on AWS!", body_style)
        ]
    ]

    t_steps = Table(steps_data, colWidths=[45, 120, 339])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AWS_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 10))

    # Troubleshooting & Best Practices
    story.append(Paragraph("3. Common Pitfalls & Troubleshooting", h1_style))
    story.append(Paragraph("• <b>Browser Timeout:</b> Verify Security Group has Inbound HTTP Port 80 open to <code>0.0.0.0/0</code>.", bullet_style))
    story.append(Paragraph("• <b>403 Forbidden:</b> Re-run permissions command: <code>sudo chown -R www-data:www-data /var/www/html && sudo chmod -R 755 /var/www/html</code>.", bullet_style))
    story.append(Paragraph("• <b>Still seeing Nginx default page:</b> Ensure <code>index.nginx-debian.html</code> was removed before cloning.", bullet_style))
    story.append(Paragraph("• <b>HTTPS redirection error:</b> Type <code>http://</code> explicitly in your browser, as free EC2 instances do not have an SSL certificate installed by default.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled Project 01 PDF: {output_filename}")

if __name__ == "__main__":
    out_pdf = r"F:\Task( Telangana )\Nalgonda\Projects\task\mini_projects\project_01_cloud_portfolio\Project_01_Cloud_Portfolio_Manual.pdf"
    build_pdf(out_pdf)

