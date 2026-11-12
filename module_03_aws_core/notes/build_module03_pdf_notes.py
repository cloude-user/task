"""
Builds the comprehensive 3-Day Module 03 AWS Core Services Master Handbook.
Includes:
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
from reportlab.lib.units import inch
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
            self.drawRightString(558, 755, "Trainer: Sundeep Hiremath")

            self.line(54, 45, 558, 45)
            self.drawString(54, 33, "Nalgonda Training Center  |  AWS DVA-C02 Alignment  |  3-Day Curriculum Handbook")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 33, page_text)

        self.restoreState()

def build_pdf(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
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
        fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=AWS_NAVY,
        spaceBefore=14, spaceAfter=6, keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor("#0F172A"),
        spaceBefore=9, spaceAfter=4, keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13, textColor=DARK_TEXT, spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=12.5, textColor=DARK_TEXT,
        leftIndent=12, firstLineIndent=-8, spaceAfter=3
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

    # =========================================================================
    # HEADER BANNER
    # =========================================================================
    story.append(Paragraph("TASK TELANGANA · CLOUD SOFTWARE DEVELOPER TRAINING", ParagraphStyle(
        'SubHeader', fontName='Helvetica-Bold', fontSize=10, textColor=AWS_ORANGE, spaceAfter=4
    )))
    story.append(Paragraph("Module 03: AWS Core Services & Infrastructure Master Handbook", title_style))
    story.append(Paragraph("<b>The 3-Day Technical Deep Dive: Compute, Storage Triad, Databases, VPC Networking, Containers (Docker/ECR/ECS) & IaC CloudFormation</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=AWS_ORANGE, spaceAfter=10))

    meta_text = "<b>Trainer:</b> Sundeep Hiremath &nbsp;|&nbsp; <b>Center:</b> Nalgonda Training Center &nbsp;|&nbsp; <b>Duration:</b> 3-Day Course Delivery &nbsp;|&nbsp; <b>Alignment:</b> AWS DVA-C02"
    story.append(Paragraph(meta_text, ParagraphStyle('Meta', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor("#64748B"), spaceAfter=10)))

    # Callout Box
    intro_callout = [
        [Paragraph("<b>TRAINER OVERVIEW:</b> This master guide is compiled specifically for the Nalgonda training cohort. It covers the full technical breadth required for enterprise cloud engineering and AWS Certified Developer (DVA-C02) standards. Concepts are grounded in <b>The Grand Vehicle Metaphor</b> so students can quickly bridge real-world hardware intuition to enterprise AWS services.", callout_style)]
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

    # =========================================================================
    # SECTION 1: THE GRAND VEHICLE METAPHOR
    # =========================================================================
    story.append(Paragraph("1. The Grand Vehicle Metaphor: The Cloud as an Automobile Fleet", h1_style))
    story.append(Paragraph("To eliminate confusion among dozens of cloud services, think of AWS as an on-demand vehicle rental and logistics agency:", body_style))

    analogy_data = [
        [Paragraph("<b>AWS Service</b>", bullet_style), Paragraph("<b>Vehicle Metaphor</b>", bullet_style), Paragraph("<b>Real-World Function</b>", bullet_style)],
        [Paragraph("<b>Amazon EC2</b>", body_style), Paragraph("<b>The Car Engine & Chassis</b>", body_style), Paragraph("Rent an engine on-demand. Choose horsepower (Instance Type: <i>t3.micro</i>), model (AMI: <i>Amazon Linux</i>), and ignition key (Key Pair <i>.pem</i>).", body_style)],
        [Paragraph("<b>Amazon EBS</b>", body_style), Paragraph("<b>The Car's Personal Trunk</b>", body_style), Paragraph("Local hard drive bolted to 1 car chassis in a parking garage (AZ). Data stays safe when engine turns off.", body_style)],
        [Paragraph("<b>Amazon EFS</b>", body_style), Paragraph("<b>The Shared Fleet Roof Cargo</b>", body_style), Paragraph("Shared roof rack accessed simultaneously by 100+ cars across multiple garages via NFS protocol.", body_style)],
        [Paragraph("<b>Amazon S3</b>", body_style), Paragraph("<b>The Global Container Depot</b>", body_style), Paragraph("Infinite worldwide warehouse outside the vehicle. Store objects in buckets; reachable via web URLs (HTTPS). 11 9's durability.", body_style)],
        [Paragraph("<b>Amazon VPC</b>", body_style), Paragraph("<b>The Gated Industrial Campus</b>", body_style), Paragraph("Private gated corporate park with secure perimeter walls. Only authorized vehicles enter.", body_style)],
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

    # =========================================================================
    # SECTION 2: GLOBAL INFRASTRUCTURE & MULTI-AZ
    # =========================================================================
    story.append(Paragraph("2. Global Infrastructure: Regions, Availability Zones & Multi-AZ", h1_style))
    story.append(Paragraph("• <b>AWS Region:</b> A distinct geographic location (e.g. <code>ap-south-1</code> Mumbai, <code>us-east-1</code> N. Virginia). Criteria to choose: 1) Latency to end-users, 2) Data sovereignty/compliance laws, 3) Service feature availability, 4) Regional cost variations.", bullet_style))
    story.append(Paragraph("• <b>Availability Zone (AZ):</b> One or more isolated data centers with independent power and networking within a Region (e.g. <code>ap-south-1a</code>, <code>1b</code>, <code>1c</code>). Connected by private sub-millisecond optical fiber.", bullet_style))
    story.append(Paragraph("• <b>Multi-AZ Architecture:</b> Deploying redundant resources across 2 or more AZs in the same region. Features <b>synchronous replication</b>: if one data center floods, automatic failover shifts traffic to the standby AZ in seconds with zero data loss (99.99% availability).", bullet_style))
    story.append(Paragraph("• <b>Multi-Region Architecture:</b> Duplicating resources across continents (e.g. Mumbai + Frankfurt) with asynchronous replication for ultimate disaster recovery.", bullet_style))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 3: EC2 & STORAGE TRIAD
    # =========================================================================
    story.append(Paragraph("3. Amazon EC2 & The Storage Triad (EBS, EFS, S3)", h1_style))
    story.append(Paragraph("• <b>EC2 Lifecycle:</b> <i>Pending</i> ➔ <i>Running</i> ➔ <i>Stopping</i> ➔ <i>Stopped</i> (Compute billing drops to $0.00/hr, storage remains billed, public IP is released) ➔ <i>Terminated</i> (Permanently destroyed).", bullet_style))
    story.append(Paragraph("• <b>Storage Shootout:</b> <b>EBS</b> is local block storage bound to 1 AZ for OS and databases. <b>EFS</b> is a multi-AZ network file system mounted by 100+ servers concurrently via NFS. <b>S3</b> is an infinite global object store accessed via REST API with 11 9's durability.", bullet_style))
    story.append(Paragraph("• <b>S3 Security:</b> Always keep <b>Block Public Access (BPA)</b> ON. Attach an HTTPS-enforced bucket policy to prevent unencrypted transmissions.", bullet_style))

    # =========================================================================
    # SECTION 4: DATABASES DEEP DIVE
    # =========================================================================
    story.append(Paragraph("4. Databases: RDS vs Aurora vs DynamoDB vs ElastiCache (Redis)", h1_style))
    story.append(Paragraph("AWS provides specialized database engines tailored for specific data access patterns:", body_style))

    db_data = [
        [Paragraph("<b>Database</b>", bullet_style), Paragraph("<b>Model</b>", bullet_style), Paragraph("<b>Key Architectural Feature</b>", bullet_style), Paragraph("<b>Ideal Use Case</b>", bullet_style)],
        [Paragraph("<b>Amazon RDS</b>", body_style), Paragraph("Relational SQL", body_style), Paragraph("Managed Postgres/MySQL with Multi-AZ automated synchronous standby failover.", body_style), Paragraph("Transactional enterprise ERP, financial ledgers, legacy SQL schemas.", body_style)],
        [Paragraph("<b>Amazon Aurora</b>", body_style), Paragraph("Relational SQL", body_style), Paragraph("6-way distributed replication across 3 AZs. 5x faster than standard MySQL. Serverless v2.", body_style), Paragraph("High-throughput enterprise web applications and auto-scaling APIs.", body_style)],
        [Paragraph("<b>Amazon DynamoDB</b>", body_style), Paragraph("NoSQL Key-Val", body_style), Paragraph("Serverless, single-digit millisecond latency at any scale. Partition Key + Sort Key.", body_style), Paragraph("E-commerce carts, user profiles, gaming leaderboards, IoT sensor telemetry.", body_style)],
        [Paragraph("<b>Amazon ElastiCache</b>", body_style), Paragraph("In-Memory (Redis)", body_style), Paragraph("Sub-millisecond read/write by caching frequently requested data in RAM.", body_style), Paragraph("Web session caches, real-time analytics counters, database read-offloading.", body_style)]
    ]
    t_db = Table(db_data, colWidths=[95, 80, 165, 164])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AWS_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_db)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: VPC NETWORKING, EDGE & SECURITY
    # =========================================================================
    story.append(Paragraph("5. VPC Networking, Edge Delivery & Perimeter Security", h1_style))
    story.append(Paragraph("• <b>VPC & Subnets:</b> Standard VPC CIDR <code>10.0.0.0/16</code> (65,536 private IPs). <b>A subnet is Public ONLY if its route table points <code>0.0.0.0/0</code> to an Internet Gateway (IGW).</b> Private subnets route outbound traffic via a <b>NAT Gateway</b> residing in a public subnet.", bullet_style))
    story.append(Paragraph("• <b>Security Groups vs NACLs:</b> Security Groups are <b>stateful</b> and operate at the instance level (allow rules only). Network ACLs are <b>stateless</b> and operate at the subnet boundary (allow and deny rules, evaluated in numerical order).", bullet_style))
    story.append(Paragraph("• <b>ALB vs NLB:</b> Application Load Balancer operates at Layer 7 (HTTP/HTTPS URL path routing). Network Load Balancer operates at Layer 4 (ultra-low latency TCP/UDP millions of requests/sec).", bullet_style))
    story.append(Paragraph("• <b>CloudFront & AWS WAF:</b> CloudFront caches static media at 600+ edge locations. AWS WAF inspects Layer 7 traffic to block SQL Injection, XSS, and rate-limits brute force attacks.", bullet_style))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: CONTAINERS & ECR / ECS vs LAMBDA
    # =========================================================================
    story.append(Paragraph("6. Containers: Docker, Amazon ECR & Amazon ECS vs AWS Lambda", h1_style))
    story.append(Paragraph("A Docker container packages code and dependencies into a lightweight unit that shares the host OS kernel, starting in seconds compared to heavy virtual machines.", body_style))

    story.append(Paragraph("6.1 Pushing Docker Images to Amazon ECR via AWS CLI", h2_style))
    ecr_code = [
        [Paragraph(
            "# 1. Authenticate Docker CLI to your private Amazon ECR registry<br/>"
            "aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.ap-south-1.amazonaws.com<br/>"
            "# 2. Build your local Docker image<br/>"
            "docker build -t task-cloud-app:latest .<br/>"
            "# 3. Tag image with ECR repository URI<br/>"
            "docker tag task-cloud-app:latest 123456789012.dkr.ecr.ap-south-1.amazonaws.com/task-cloud-app:latest<br/>"
            "# 4. Push to Amazon ECR<br/>"
            "docker push 123456789012.dkr.ecr.ap-south-1.amazonaws.com/task-cloud-app:latest",
            code_style
        )]
    ]
    t_ecr = Table(ecr_code, colWidths=[504])
    t_ecr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#334155")),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ecr)
    story.append(Spacer(1, 6))

    story.append(Paragraph("6.2 Architecture Showdown: Amazon ECS vs AWS Lambda Container Images", h2_style))
    container_comp = [
        [Paragraph("<b>Architectural Metric</b>", bullet_style), Paragraph("<b>Amazon ECS (Fargate / EC2)</b>", bullet_style), Paragraph("<b>AWS Lambda Container Images</b>", bullet_style)],
        [Paragraph("<b>Execution Timeout</b>", body_style), Paragraph("<b>Unlimited / Indefinite</b> (Runs 24/7/365)", body_style), Paragraph("<b>Strict 15-Minute Maximum</b>", body_style)],
        [Paragraph("<b>Compute Model</b>", body_style), Paragraph("Persistent web services, background daemons", body_style), Paragraph("Event-driven, serverless execution (scale-to-zero)", body_style)],
        [Paragraph("<b>Max Image Size</b>", body_style), Paragraph("Dozens of Gigabytes supported", body_style), Paragraph("Maximum 10 GB container image", body_style)],
        [Paragraph("<b>Billing</b>", body_style), Paragraph("Per-second of allocated vCPU & RAM", body_style), Paragraph("Per-millisecond of actual execution time ($0 if idle)", body_style)],
        [Paragraph("<b>Best Use Case</b>", body_style), Paragraph("Continuous REST APIs, web apps, message queues", body_style), Paragraph("S3 image processing, webhooks, scheduled cron ETL", body_style)]
    ]
    t_cc = Table(container_comp, colWidths=[120, 190, 194])
    t_cc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AWS_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cc)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: IAC & CLOUDFORMATION DRIFT DETECTION
    # =========================================================================
    story.append(Paragraph("7. Infrastructure as Code (IaC) & CloudFormation Drift Detection", h1_style))
    story.append(Paragraph("<b>Infrastructure as Code (IaC)</b> replaces error-prone manual console clicking with version-controlled YAML/JSON templates. CloudFormation manages the full lifecycle of your stacks, providing automatic rollback on failure and preview Change Sets.", body_style))

    story.append(Paragraph("7.1 Understanding & Catching Infrastructure Drift", h2_style))
    drift_box = [
        [Paragraph(
            "<b>WHAT IS DRIFT?</b> Drift occurs when an engineer makes out-of-band manual changes in the AWS Console (e.g. changing an EC2 instance type from <code>t3.micro</code> to <code>m5.large</code> or opening Port 22 in a Security Group) without modifying the CloudFormation template.<br/><br/>"
            "<b>HOW TO DETECT & REMEDIATE DRIFT:</b><br/>"
            "1. Run <b>Detect stack drift</b> in the CloudFormation Console (or CLI: <code>aws cloudformation detect-stack-drift --stack-name &lt;name&gt;</code>).<br/>"
            "2. Review the drift report: AWS flags drifted properties in red side-by-side with template expected values.<br/>"
            "3. <b>Remediation:</b> Either revert the manual console change back to the template baseline, OR update the CloudFormation YAML template to adopt the new configuration and deploy via a Change Set.",
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

    # =========================================================================
    # SECTION 8: CLEANUP CHECKLIST
    # =========================================================================
    story.append(Paragraph("8. Student Zero-Dollar Sunset Checklist", h1_style))
    story.append(Paragraph("1. Stop or Terminate all practice EC2 instances.<br/>"
                           "2. Delete orphan EBS volumes in 'available' status.<br/>"
                           "3. Delete custom CloudFormation stacks (automatically cleans up all child resources!).<br/>"
                           "4. Release any unallocated Elastic IPs.<br/>"
                           "5. Check AWS Billing Dashboard to verify $0.00 balance.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled expanded 3-Day PDF guide: {output_filename}")

if __name__ == "__main__":
    out_pdf = r"F:\Task( Telangana )\Nalgonda\Projects\task\module_03_aws_core\notes\Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf"
    build_pdf(out_pdf)
