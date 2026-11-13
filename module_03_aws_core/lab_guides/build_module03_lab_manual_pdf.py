"""
Builds the comprehensive Module 03 Hands-on Lab Manual PDF for students.
Trainer: Sundeep Hiremat
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
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
            self.drawString(54, 755, "TASK Telangana · Cloud Software Developer  |  Module 03: Hands-on Lab Manual")
            self.drawRightString(558, 755, "Trainer: Sundeep Hiremat")

            self.line(54, 45, 558, 45)
            self.drawString(54, 33, "Nalgonda Training Center  |  AWS DVA-C02 Alignment  |  Step-by-Step Lab Playbook")
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
    DARK_TEXT = colors.HexColor("#1A202C")
    CODE_BG = colors.HexColor("#0F172A")
    LIGHT_BLUE = colors.HexColor("#EFF6FF")
    LIGHT_AMBER = colors.HexColor("#FEF3C7")

    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=AWS_NAVY, spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=AWS_NAVY,
        spaceBefore=14, spaceAfter=6, keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor("#0F172A"),
        spaceBefore=8, spaceAfter=4, keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12, textColor=DARK_TEXT, spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12, textColor=DARK_TEXT,
        leftIndent=12, firstLineIndent=-8, spaceAfter=2.5
    )

    code_style = ParagraphStyle(
        'Code_Custom', parent=styles['Normal'],
        fontName='Courier', fontSize=7.5, leading=10, textColor=colors.HexColor("#F8FAFC"), spaceAfter=3
    )

    story = []

    # Title Banner
    story.append(Paragraph("TASK TELANGANA · CLOUD SOFTWARE DEVELOPER TRAINING", ParagraphStyle(
        'SubHeader', fontName='Helvetica-Bold', fontSize=10, textColor=AWS_ORANGE, spaceAfter=4
    )))
    story.append(Paragraph("Module 03: Hands-on Lab Manual & Project Guide", title_style))
    story.append(Paragraph("<b>Complete Step-by-Step Practical Playbook: EC2, Storage (EBS/S3), Custom VPC & Mini Project 1</b>", ParagraphStyle(
        'Sub', fontName='Helvetica', fontSize=11, leading=15, textColor=colors.HexColor("#475569"), spaceAfter=8
    )))
    story.append(HRFlowable(width="100%", thickness=2, color=AWS_ORANGE, spaceAfter=10))

    meta_text = "<b>Trainer:</b> Sundeep Hiremat &nbsp;|&nbsp; <b>Center:</b> Nalgonda Training Center &nbsp;|&nbsp; <b>Curriculum:</b> AWS DVA-C02 Alignment"
    story.append(Paragraph(meta_text, ParagraphStyle('Meta', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#64748B"), spaceAfter=10)))

    # Callout
    intro_box = [
        [Paragraph("<b>LAB INSTRUCTIONS FOR STUDENTS:</b> Every lab in this manual is verified strictly within the AWS Free Tier. Follow all configuration parameters carefully (especially Availability Zones, Security Group rules, and IAM permissions). Before leaving the training room, always perform the <b>Sunset Cleanup Routine</b> to keep your billing at $0.00.", ParagraphStyle('Call', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#1E3A8A")))]
    ]
    t_in = Table(intro_box, colWidths=[504])
    t_in.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BLUE),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_in)
    story.append(Spacer(1, 10))

    # =========================================================================
    # LAB 1: EC2 & CUSTOM AMI
    # =========================================================================
    story.append(Paragraph("Lab 1: Amazon EC2 Launch, User Data Automation & Custom AMIs", h1_style))
    story.append(Paragraph("<b>Objective:</b> Launch Amazon Linux 2023 EC2 instance on Free Tier (`t2.micro` or `t3.micro`), inject User Data startup automation script, verify live web response, and bake a Custom AMI Golden Image.", body_style))

    story.append(Paragraph("<b>Step-by-Step Procedure:</b>", h2_style))
    story.append(Paragraph("1. Open <b>EC2 Dashboard</b> ➔ Click <b>Launch Instance</b>.", bullet_style))
    story.append(Paragraph("2. <b>Name:</b> <code>task-webserver-01</code> | <b>AMI:</b> <i>Amazon Linux 2023 AMI (Free tier eligible)</i>.", bullet_style))
    story.append(Paragraph("3. <b>Instance type:</b> <code>t2.micro</code> or <code>t3.micro</code> | <b>Key pair:</b> Create <code>task-nalgonda-key.pem</code> (RSA format).", bullet_style))
    story.append(Paragraph("4. <b>Security Group:</b> Allow <b>SSH (Port 22, Source: My IP)</b> and <b>HTTP (Port 80, Source: 0.0.0.0/0)</b>.", bullet_style))
    story.append(Paragraph("5. <b>User Data (Advanced Details):</b> Paste the following bootstrapping script to auto-install Apache & Python on first boot:", bullet_style))

    c1 = [
        [Paragraph(
            "#!/bin/bash<br/>"
            "dnf update -y && dnf install -y httpd python3 git<br/>"
            "systemctl start httpd && systemctl enable httpd<br/>"
            "TOKEN=$(curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600')<br/>"
            "IID=$(curl -s -H 'X-aws-ec2-metadata-token: '$TOKEN http://169.254.169.254/latest/meta-data/instance-id)<br/>"
            "echo '&lt;h1&gt;TASK Cloud Lab · Instance: '$IID'&lt;/h1&gt;' &gt; /var/www/html/index.html",
            code_style
        )]
    ]
    t_c1 = Table(c1, colWidths=[504])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#334155")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_c1)
    story.append(Spacer(1, 4))
    story.append(Paragraph("6. Click <b>Launch instance</b> ➔ Wait until state is <i>Running</i> ➔ Open <code>http://&lt;PUBLIC-IP&gt;</code> in browser.", bullet_style))
    story.append(Paragraph("7. <b>Bake Custom AMI:</b> Select instance ➔ <b>Actions</b> ➔ <b>Image and templates</b> ➔ <b>Create image</b> ➔ Name: <code>task-golden-v1</code> ➔ Click <b>Create image</b>.", bullet_style))

    story.append(Spacer(1, 10))

    # =========================================================================
    # LAB 2: EBS & S3
    # =========================================================================
    story.append(Paragraph("Lab 2: Storage Triad — EBS Formatting & Secure S3 Buckets", h1_style))
    story.append(Paragraph("<b>Objective:</b> Attach and format an EBS volume (`ext4`), create snapshots, provision an Amazon S3 bucket with Block Public Access, and enforce HTTPS via JSON Bucket Policy.", body_style))

    story.append(Paragraph("<b>Part A: EBS Volume Mount & Snapshots</b>", h2_style))
    story.append(Paragraph("1. EC2 Console ➔ <b>Volumes</b> ➔ <b>Create volume</b> ➔ 5 GiB gp3 ➔ Select the <b>SAME Availability Zone</b> as your EC2 instance.", bullet_style))
    story.append(Paragraph("2. Select Volume ➔ <b>Actions</b> ➔ <b>Attach volume</b> ➔ Attach to <code>task-webserver-01</code>.", bullet_style))
    story.append(Paragraph("3. Connect to EC2 terminal and format the block storage:", bullet_style))

    c2 = [
        [Paragraph(
            "lsblk                          # View attached block storage device (xvdf)<br/>"
            "sudo mkfs -t ext4 /dev/xvdf    # Format raw block storage with ext4 filesystem<br/>"
            "sudo mkdir -p /mnt/data        # Create mount directory<br/>"
            "sudo mount /dev/xvdf /mnt/data # Mount volume<br/>"
            "df -h /mnt/data                # Verify available storage space",
            code_style
        )]
    ]
    t_c2 = Table(c2, colWidths=[504])
    t_c2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#334155")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_c2)
    story.append(Spacer(1, 4))
    story.append(Paragraph("4. <b>EBS Snapshot:</b> In AWS Console ➔ Select Volume ➔ <b>Actions</b> ➔ <b>Create snapshot</b>.", bullet_style))

    story.append(Paragraph("<b>Part B: Amazon S3 & HTTPS Bucket Policy</b>", h2_style))
    story.append(Paragraph("1. S3 Console ➔ <b>Create bucket</b> ➔ Name: <code>task-nalgonda-&lt;rollno&gt;-2026</code> (globally unique).", bullet_style))
    story.append(Paragraph("2. Ensure <b>Block all public access</b> is CHECKED ➔ Click <b>Create bucket</b> ➔ Upload sample file.", bullet_style))
    story.append(Paragraph("3. Go to <b>Permissions</b> ➔ <b>Bucket policy</b> ➔ <b>Edit</b> ➔ Paste HTTPS enforcement JSON policy:", bullet_style))

    c3 = [
        [Paragraph(
            '{\n'
            '  "Version": "2012-10-17",\n'
            '  "Statement": [{\n'
            '    "Sid": "EnforceHTTPSOnly",\n'
            '    "Effect": "Deny",\n'
            '    "Principal": "*",\n'
            '    "Action": "s3:*",\n'
            '    "Resource": ["arn:aws:s3:::YOUR-BUCKET-NAME", "arn:aws:s3:::YOUR-BUCKET-NAME/*"],\n'
            '    "Condition": {"Bool": {"aws:SecureTransport": "false"}}\n'
            '  }]\n'
            '}',
            code_style
        )]
    ]
    t_c3 = Table(c3, colWidths=[504])
    t_c3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#334155")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_c3)

    story.append(Spacer(1, 10))

    # =========================================================================
    # LAB 3: CUSTOM VPC
    # =========================================================================
    story.append(Paragraph("Lab 3: Custom Amazon VPC, Subnets, Gateways & Security", h1_style))
    story.append(Paragraph("<b>Objective:</b> Build an isolated corporate VPC (`10.0.0.0/16`), carve Public and Private subnets, attach an Internet Gateway (IGW), configure Route Tables, and test Stateful Security Groups vs Stateless Network ACLs.", body_style))

    vpc_steps = [
        [Paragraph("<b>Component</b>", bullet_style), Paragraph("<b>CIDR / Configuration</b>", bullet_style), Paragraph("<b>Routing & Purpose</b>", bullet_style)],
        [Paragraph("<b>VPC</b>", body_style), Paragraph("<code>10.0.0.0/16</code>", body_style), Paragraph("Isolated virtual network container (65,536 private IP addresses). Enable DNS hostnames.", body_style)],
        [Paragraph("<b>Public Subnet</b>", body_style), Paragraph("<code>10.0.1.0/24</code> (AZ-1a)", body_style), Paragraph("Associated with Custom Route Table pointing <code>0.0.0.0/0</code> ➔ <b>Internet Gateway (IGW)</b>.", body_style)],
        [Paragraph("<b>Private Subnet</b>", body_style), Paragraph("<code>10.0.2.0/24</code> (AZ-1b)", body_style), Paragraph("Associated with Main Route Table (Local only: <code>10.0.0.0/16</code>). No direct route to IGW!", body_style)],
        [Paragraph("<b>Security Group</b>", body_style), Paragraph("<b>Stateful</b> (Instance Level)", body_style), Paragraph("Allow Inbound 80 HTTP; return traffic is automatically permitted out.", body_style)],
        [Paragraph("<b>Network ACL</b>", body_style), Paragraph("<b>Stateless</b> (Subnet Level)", body_style), Paragraph("Must explicitly permit BOTH Inbound (port 80) and Outbound (ports 1024–65535).", body_style)]
    ]
    t_v = Table(vpc_steps, colWidths=[95, 120, 289])
    t_v.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AWS_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_v)

    story.append(Spacer(1, 10))

    # =========================================================================
    # LAB 4: MINI PROJECT 1
    # =========================================================================
    story.append(Paragraph("Lab 4 (Mini Project 1): Live Portfolio on Ubuntu 24.04 LTS + Nginx + GitHub", h1_style))
    story.append(Paragraph("<b>Objective:</b> Launch Ubuntu 24.04 LTS, install Git and Nginx, clone personal portfolio from GitHub into <code>/var/www/html</code>, fix Linux permissions, and verify live web deployment.", body_style))

    p1_cmd = [
        [Paragraph(
            "# 1. Update OS package lists and upgrade existing software<br/>"
            "sudo apt update &amp;&amp; sudo apt upgrade -y<br/><br/>"
            "# 2. Install Git and high-performance Nginx web server<br/>"
            "sudo apt install git nginx -y<br/>"
            "sudo systemctl status nginx     # Verify: Active (running)<br/><br/>"
            "# 3. Remove default Nginx welcome placeholder<br/>"
            "cd /var/www/html &amp;&amp; sudo rm -f index.nginx-debian.html<br/><br/>"
            "# 4. Clone your GitHub portfolio into web root<br/>"
            "sudo git clone https://github.com/gauri-abc/gauri-yadav-cloud-portfolio.git .<br/><br/>"
            "# 5. Configure Linux ownership (www-data) and permissions (755)<br/>"
            "sudo chown -R www-data:www-data /var/www/html<br/>"
            "sudo chmod -R 755 /var/www/html<br/><br/>"
            "# 6. Restart &amp; enable Nginx service<br/>"
            "sudo systemctl restart nginx &amp;&amp; sudo systemctl enable nginx",
            code_style
        )]
    ]
    t_p1 = Table(p1_cmd, colWidths=[504])
    t_p1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#334155")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_p1)
    story.append(Spacer(1, 4))
    story.append(Paragraph("7. Open browser: <code>http://&lt;YOUR_EC2_PUBLIC_IP&gt;</code> to verify live portfolio!", bullet_style))

    story.append(Spacer(1, 10))

    # =========================================================================
    # LAB SUNSET CLEANUP
    # =========================================================================
    story.append(Paragraph("Student Zero-Dollar Sunset Checklist", h1_style))
    story.append(Paragraph("1. Stop practice EC2 instances (pauses compute charges).<br/>"
                           "2. Terminate throwaway instances and delete orphan EBS volumes.<br/>"
                           "3. Release any allocated Elastic IPs.<br/>"
                           "4. Delete practice CloudFormation stacks to tear down child resources cleanly.<br/>"
                           "5. Check AWS Billing Dashboard weekly to ensure $0.00 balance.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled Lab Manual PDF: {output_filename}")

if __name__ == "__main__":
    out_pdf = r"F:\Task( Telangana )\Nalgonda\Projects\task\module_03_aws_core\lab_guides\Module_03_Hands_On_Lab_Manual.pdf"
    build_pdf(out_pdf)

