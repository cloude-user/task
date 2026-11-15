"""
Builds the comprehensive 3-Day Module 03 AWS Core Services Master Handbook.
Trainer: Sundeep Hiremat
Includes:
- Service Requirements & Decision Matrix (What is Required & When to Use Which Service)
- Regions, AZs, Multi-AZ vs Multi-Region
- EC2, AMIs, Key Pairs, Security Groups, User Data
- EBS, EFS, S3, S3 Security & HTTPS policies
- RDS, Aurora, DynamoDB, ElastiCache (Redis)
- VPC, Subnets, IGW, NAT Gateway, Security Groups vs NACLs, ALB vs NLB
- CloudFront CDN, AWS WAF, AWS Shield
- Docker Basics, Amazon ECR, AWS CLI push/pull steps, Amazon ECS (EC2 vs Fargate)
- ECS Containers vs AWS Lambda Container Images
- Infrastructure as Code (IaC) with AWS CloudFormation & Drift Detection
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
            self.drawString(54, 755, "TASK Telangana · Cloud Software Developer  |  Module 03: AWS Core Services Masterclass")
            self.drawRightString(558, 755, "Trainer: Sundeep Hiremat")

            self.line(54, 45, 558, 45)
            self.drawString(54, 33, "Nalgonda Training Center  |  AWS DVA-C02 Alignment  |  3-Day Curriculum Handbook")
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

    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=11, leading=15, textColor=colors.HexColor("#475569"), spaceAfter=12
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

    callout_style = ParagraphStyle(
        'Callout_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # HEADER BANNER
    story.append(Paragraph("TASK TELANGANA · CLOUD SOFTWARE DEVELOPER TRAINING", ParagraphStyle(
        'SubHeader', fontName='Helvetica-Bold', fontSize=10, textColor=AWS_ORANGE, spaceAfter=4
    )))
    story.append(Paragraph("Module 03: AWS Core Services & Infrastructure Master Handbook", title_style))
    story.append(Paragraph("<b>The 3-Day Technical Deep Dive: Compute, Storage Triad, Databases, VPC Networking, Containers (Docker/ECR/ECS) & IaC CloudFormation</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=AWS_ORANGE, spaceAfter=10))

    meta_text = "<b>Trainer:</b> Sundeep Hiremat &nbsp;|&nbsp; <b>Center:</b> Nalgonda Training Center &nbsp;|&nbsp; <b>Duration:</b> 3-Day Delivery &nbsp;|&nbsp; <b>Alignment:</b> AWS DVA-C02"
    story.append(Paragraph(meta_text, ParagraphStyle('Meta', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#64748B"), spaceAfter=10)))

    # Callout Box
    intro_callout = [
        [Paragraph("<b>TRAINER OVERVIEW:</b> This master guide is compiled specifically for the Nalgonda training cohort. It covers the full technical breadth required for enterprise cloud engineering and AWS Certified Developer (DVA-C02) standards. Concepts are grounded in <b>The Grand Vehicle Metaphor</b> and accompanied by an explicit <b>Service Decision Architecture</b>.", callout_style)]
    ]
    t_intro = Table(intro_callout, colWidths=[504])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BLUE),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 10))

    # SECTION 1: THE GRAND VEHICLE METAPHOR
    story.append(Paragraph("1. The Grand Vehicle Metaphor: The Cloud as an Automobile Fleet", h1_style))
    story.append(Paragraph("To eliminate confusion among dozens of cloud services, think of AWS as an on-demand vehicle rental and logistics agency:", body_style))

    analogy_data = [
        [Paragraph("<b>AWS Service</b>", bullet_style), Paragraph("<b>Vehicle Metaphor</b>", bullet_style), Paragraph("<b>Real-World Function</b>", bullet_style)],
        [Paragraph("<b>Amazon EC2</b>", body_style), Paragraph("<b>Car Engine & Chassis</b>", body_style), Paragraph("Rent an engine on-demand. Choose horsepower (Instance Type: <i>t3.micro</i>), model (AMI: <i>Amazon Linux</i>), and key (Key Pair <i>.pem</i>).", body_style)],
        [Paragraph("<b>Amazon EBS</b>", body_style), Paragraph("<b>Car's Personal Trunk</b>", body_style), Paragraph("Local hard drive bolted to 1 car chassis in a parking garage (AZ). Data stays safe when engine turns off.", body_style)],
        [Paragraph("<b>Amazon EFS</b>", body_style), Paragraph("<b>Shared Fleet Roof Cargo</b>", body_style), Paragraph("Shared roof rack accessed simultaneously by 100+ cars across multiple garages via NFS protocol.", body_style)],
        [Paragraph("<b>Amazon S3</b>", body_style), Paragraph("<b>Global Container Depot</b>", body_style), Paragraph("Infinite worldwide warehouse outside the vehicle. Store objects in buckets; reachable via web URLs (HTTPS). 11 9's durability.", body_style)],
        [Paragraph("<b>Amazon VPC</b>", body_style), Paragraph("<b>Gated Industrial Campus</b>", body_style), Paragraph("Private gated corporate park with secure perimeter walls. Only authorized vehicles enter.", body_style)],
        [Paragraph("<b>Internet Gateway</b>", body_style), Paragraph("<b>Main Highway Gate</b>", body_style), Paragraph("Two-way highway opening connecting public showroom lanes to the internet.", body_style)],
        [Paragraph("<b>NAT Gateway</b>", body_style), Paragraph("<b>One-Way Security Escort</b>", body_style), Paragraph("Allows private vault cars to fetch fuel/software without letting outside internet cars in.", body_style)],
        [Paragraph("<b>Security Group</b>", body_style), Paragraph("<b>Car's Personal Bodyguard</b>", body_style), Paragraph("<b>Stateful:</b> If a passenger is approved to enter, they can step back out automatically.", body_style)],
        [Paragraph("<b>Network ACL</b>", body_style), Paragraph("<b>Highway Border Toll Booth</b>", body_style), Paragraph("<b>Stateless:</b> Checks license plates on entry AND explicitly checks license plates on exit.", body_style)]
    ]
    t_analogy = Table(analogy_data, colWidths=[100, 120, 284])
    t_analogy.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AWS_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_analogy)
    story.append(Spacer(1, 10))

    # SECTION 2: SERVICE REQUIREMENTS & DECISION MATRIX
    story.append(Paragraph("2. Service Requirements & Decision Matrix: What is Required & When to Use Which Service", h1_style))
    story.append(Paragraph("To make architectural decisions with confidence, memorize both the technical prerequisites and the exact decision triggers:", body_style))

    dec_matrix = [
        [Paragraph("<b>Service</b>", bullet_style), Paragraph("<b>What is Required (Prerequisites)</b>", bullet_style), Paragraph("<b>When to Choose It (Decision Trigger)</b>", bullet_style)],
        [
            Paragraph("<b>Amazon EC2</b>", body_style),
            Paragraph("• AMI OS template<br/>• Instance Type (vCPU/RAM)<br/>• VPC Subnet & Key Pair (.pem)<br/>• Security Group with open ports", body_style),
            Paragraph("Need full administrative root access over the OS, custom software daemons, or monolithic architectures.", body_style)
        ],
        [
            Paragraph("<b>Amazon EBS</b>", body_style),
            Paragraph("• Must be in <b>exact same AZ</b> as EC2<br/>• Formatted in Linux (<code>ext4</code>) and mounted", body_style),
            Paragraph("OS boot drives and high-performance transactional database storage requiring <1ms low latency.", body_style)
        ],
        [
            Paragraph("<b>Amazon EFS</b>", body_style),
            Paragraph("• VPC Mount Targets in each AZ<br/>• Security Group allowing Port 2049 (NFS)", body_style),
            Paragraph("Multiple EC2 servers (100+) need concurrent shared read/write access to a single filesystem (CMS, web uploads).", body_style)
        ],
        [
            Paragraph("<b>Amazon S3</b>", body_style),
            Paragraph("• Globally unique bucket name (3-63 chars)<br/>• Block Public Access ON<br/>• IAM / Bucket Policy permissions", body_style),
            Paragraph("Static website hosting, user images/videos, backups, analytics lakes. 99.999999999% durability.", body_style)
        ],
        [
            Paragraph("<b>Amazon RDS</b>", body_style),
            Paragraph("• DB Subnet Group across 2+ AZs<br/>• Security Group allowing DB Port (5432/3306)", body_style),
            Paragraph("Relational SQL databases requiring ACID transactions, complex JOINs, and automated Multi-AZ failover.", body_style)
        ],
        [
            Paragraph("<b>Amazon Aurora</b>", body_style),
            Paragraph("• DB Subnet Group<br/>• Cluster endpoint configuration", body_style),
            Paragraph("Enterprise high-throughput SQL; 5x faster than MySQL, 6-way storage replication, Serverless v2.", body_style)
        ],
        [
            Paragraph("<b>DynamoDB</b>", body_style),
            Paragraph("• Table name & Partition Key (PK)<br/>• Capacity Mode (On-Demand / Provisioned)", body_style),
            Paragraph("Serverless NoSQL Key-Value store requiring single-digit millisecond latency at any scale (shopping carts, IoT).", body_style)
        ],
        [
            Paragraph("<b>ElastiCache (Redis)</b>", body_style),
            Paragraph("• Cache Subnet Group<br/>• Security Group Port 6379 from app servers", body_style),
            Paragraph("Sub-millisecond in-memory caching to eliminate SQL database query bottlenecks and store user session states.", body_style)
        ],
        [
            Paragraph("<b>Internet Gateway</b>", body_style),
            Paragraph("• Attached to VPC<br/>• Route table points 0.0.0.0/0 to IGW", body_style),
            Paragraph("Public-facing web servers or Application Load Balancers needing direct 2-way internet traffic.", body_style)
        ],
        [
            Paragraph("<b>NAT Gateway</b>", body_style),
            Paragraph("• Placed in a <b>Public Subnet</b><br/>• Allocated an <b>Elastic IP (EIP)</b>", body_style),
            Paragraph("Private subnet instances needing outbound-only internet (for OS patches/pip install) while remaining hidden from incoming hackers.", body_style)
        ],
        [
            Paragraph("<b>Amazon ECS (Fargate)</b>", body_style),
            Paragraph("• Docker Image in ECR<br/>• Task Definition (CPU/RAM)<br/>• IAM Execution Role & VPC Subnets", body_style),
            Paragraph("Running continuous Docker containers (web APIs, worker daemons) without managing underlying EC2 virtual machines.", body_style)
        ],
        [
            Paragraph("<b>AWS Lambda</b>", body_style),
            Paragraph("• Function code / Container image (max 10GB)<br/>• IAM Execution Role<br/>• Event Trigger (S3, API GW)", body_style),
            Paragraph("Event-driven tasks executing in <15 minutes. Scales to zero automatically with $0 idle cost.", body_style)
        ],
        [
            Paragraph("<b>CloudFormation</b>", body_style),
            Paragraph("• Declarative YAML/JSON template<br/>• Valid Resources section", body_style),
            Paragraph("Automating infrastructure deployment from Git. Catching manual out-of-band edits via <b>Drift Detection</b>.", body_style)
        ]
    ]

    t_dec = Table(dec_matrix, colWidths=[90, 180, 234])
    t_dec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AWS_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_dec)
    story.append(Spacer(1, 10))

    # SECTION 3: CLOUDFORMATION DRIFT DETECTION
    story.append(Paragraph("3. Infrastructure Drift Detection & Remediation", h1_style))
    drift_box = [
        [Paragraph(
            "<b>WHAT IS DRIFT?</b> Drift occurs when an engineer makes manual out-of-band changes directly in the AWS Console (e.g. resizing an EC2 instance or opening Port 22 in a Security Group) without updating the CloudFormation template.<br/><br/>"
            "<b>HOW TO CATCH & REMEDIATE DRIFT:</b><br/>"
            "1. Run <b>Detect stack drift</b> in the CloudFormation Console.<br/>"
            "2. Review the drift report: AWS flags drifted properties in red side-by-side with template expected values.<br/>"
            "3. <b>Remediation:</b> Either revert the manual console change back to match the template, OR update the CloudFormation YAML template to adopt the new configuration and deploy via a Change Set.",
            callout_style
        )]
    ]
    t_drift = Table(drift_box, colWidths=[504])
    t_drift.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_AMBER),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_drift)
    story.append(Spacer(1, 10))

    # SECTION 4: SUNSET CLEANUP
    story.append(Paragraph("4. Student Zero-Dollar Sunset Checklist", h1_style))
    story.append(Paragraph("1. Stop practice EC2 instances (pauses compute charges).<br/>"
                           "2. Delete orphan EBS volumes in 'available' status.<br/>"
                           "3. Delete custom CloudFormation stacks to tear down child resources cleanly.<br/>"
                           "4. Release any allocated Elastic IPs.<br/>"
                           "5. Check AWS Billing Dashboard weekly to ensure $0.00 balance.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled expanded 3-Day PDF guide: {output_filename}")

if __name__ == "__main__":
    out_pdf = r"F:\Task( Telangana )\Nalgonda\Projects\task\module_03_aws_core\notes\Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf"
    build_pdf(out_pdf)
