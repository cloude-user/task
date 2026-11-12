"""
Builds a high-impact, professional PDF master handbook for Module 03.
Utilizes ReportLab Platypus with a custom NumberedCanvas for dynamic total page count.
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

        # Skip headers on cover page (page 1)
        if self._pageNumber > 1:
            # Header rule
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 750, 558, 750)
            self.drawString(54, 755, "TASK Telangana · Cloud Software Developer  |  Module 03: AWS Core Services Handbook")
            self.drawRightString(558, 755, "Trainer: Sundeep Hiremath")

            # Footer rule
            self.line(54, 45, 558, 45)
            self.drawString(54, 33, "Nalgonda Training Center  |  AWS DVA-C02 Alignment  |  Confidential Student Notes")
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

    # Custom styles
    AWS_NAVY = colors.HexColor("#232F3E")
    AWS_ORANGE = colors.HexColor("#FF9900")
    DARK_TEXT = colors.HexColor("#1A202C")
    CODE_BG = colors.HexColor("#F1F5F9")
    LIGHT_BLUE = colors.HexColor("#EFF6FF")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=AWS_NAVY,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=AWS_NAVY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=DARK_TEXT,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # =========================================================================
    # COVER / HEADER BANNER
    # =========================================================================
    story.append(Paragraph("TASK TELANGANA · CLOUD SOFTWARE DEVELOPER TRAINING", ParagraphStyle(
        'SubHeader', fontName='Helvetica-Bold', fontSize=10, textColor=AWS_ORANGE, spaceAfter=4
    )))
    story.append(Paragraph("Module 03: AWS Core Services & Infrastructure Handbook", title_style))
    story.append(Paragraph("<b>Demystifying EC2, EBS, EFS, S3 & VPC Networking Through The Grand Vehicle Metaphor</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=AWS_ORANGE, spaceAfter=12))

    meta_text = "<b>Trainer:</b> Sundeep Hiremath &nbsp;|&nbsp; <b>Center:</b> Nalgonda Training Center &nbsp;|&nbsp; <b>Curriculum:</b> AWS DVA-C02 Alignment"
    story.append(Paragraph(meta_text, ParagraphStyle('Meta', fontName='Helvetica', fontSize=9, textColor=colors.HexColor("#64748B"), spaceAfter=14)))

    # Callout Box: What is this guide?
    intro_callout = [
        [Paragraph("<b>STUDENT ORIENTATION NOTE:</b> This comprehensive handbook is tailored specifically for students at the Nalgonda Training Center. It uses an intuitive <i>Automobile / Vehicle Fleet Analogy</i> to connect complex cloud services (servers, hard drives, network file systems, global storage, and private highway firewalls) to everyday mechanical concepts that are immediately understandable and unforgettable in technical interviews.", callout_style)]
    ]
    t_intro = Table(intro_callout, colWidths=[504])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BLUE),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 1: THE GRAND VEHICLE METAPHOR
    # =========================================================================
    story.append(Paragraph("1. The Grand Vehicle Metaphor: The Entire Cloud as an Automobile Fleet", h1_style))
    story.append(Paragraph("When students first encounter AWS, the sheer number of acronyms (EC2, EBS, EFS, S3, VPC, IGW, NAT, NACL) can feel overwhelming. To master them permanently, remember that <b>AWS is nothing more than a giant on-demand vehicle rental and logistics agency</b>:", body_style))

    analogy_data = [
        [Paragraph("<b>AWS Cloud Service</b>", bullet_style), Paragraph("<b>Vehicle Component</b>", bullet_style), Paragraph("<b>Metaphor & Function in Simple Terms</b>", bullet_style)],
        [
            Paragraph("<b>Amazon EC2</b><br/>(Virtual Server)", body_style),
            Paragraph("<b>The Car Engine & Chassis</b>", body_style),
            Paragraph("Instead of manufacturing your own vehicle factory, you rent an engine on-demand. You choose its horsepower (Instance Type: <i>t3.micro</i> vs <i>c5.xlarge</i>), body blueprint (AMI: <i>Amazon Linux</i> or <i>Ubuntu</i>), and ignition key (Key Pair <i>.pem</i>).", body_style)
        ],
        [
            Paragraph("<b>Amazon EBS</b><br/>(Block Storage)", body_style),
            Paragraph("<b>The Car's Built-in Trunk</b>", body_style),
            Paragraph("Directly bolted to one specific car chassis in the parking garage (Availability Zone). High speed. When the car turns off, your luggage inside stays safe. Cannot be opened by other cars on the road simultaneously.", body_style)
        ],
        [
            Paragraph("<b>Amazon EFS</b><br/>(File Storage)", body_style),
            Paragraph("<b>The Shared Fleet Roof Cargo</b>", body_style),
            Paragraph("A shared roof rack that a whole fleet of 100+ cars across multiple garages can access at the same time using standard network ropes (NFS protocol). Everyone sees shared files instantaneously.", body_style)
        ],
        [
            Paragraph("<b>Amazon S3</b><br/>(Object Storage)", body_style),
            Paragraph("<b>The Global Shipping Container Depot</b>", body_style),
            Paragraph("Not inside any car at all! An unlimited worldwide warehouse. You place cargo boxes (Objects) into large shipping bays (Buckets). Reachable from anywhere via the national highway (Internet HTTPS URL). 99.999999999% durable.", body_style)
        ],
        [
            Paragraph("<b>Amazon VPC</b><br/>(Private Cloud)", body_style),
            Paragraph("<b>The Gated Industrial Campus</b>", body_style),
            Paragraph("Your private compound with secure perimeter walls. Only authorized vehicles enter.", body_style)
        ],
        [
            Paragraph("<b>Internet Gateway (IGW)</b>", body_style),
            Paragraph("<b>The Main Highway Gate</b>", body_style),
            Paragraph("Two-way highway exit permitting cars to travel out to the world and public visitors to enter.", body_style)
        ],
        [
            Paragraph("<b>NAT Gateway</b>", body_style),
            Paragraph("<b>The One-Way Security Escort</b>", body_style),
            Paragraph("Allows private secret cars in the back vault to fetch fuel/software from the internet, but strictly prevents outside internet cars from driving in.", body_style)
        ],
        [
            Paragraph("<b>Security Group</b>", body_style),
            Paragraph("<b>Car's Personal Bodyguard</b>", body_style),
            Paragraph("Stateful guard at each car door. If someone is authorized to get in, they can step out freely.", body_style)
        ],
        [
            Paragraph("<b>Network ACL (NACL)</b>", body_style),
            Paragraph("<b>District Highway Toll Booth</b>", body_style),
            Paragraph("Stateless barrier across the road. Inspects license plates on entrance AND on exit.", body_style)
        ]
    ]

    t_analogy = Table(analogy_data, colWidths=[110, 110, 284])
    t_analogy.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AWS_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_analogy)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 2: AMAZON EC2 DEEP DIVE
    # =========================================================================
    story.append(Paragraph("2. Amazon EC2 (Elastic Compute Cloud): Core Virtual Compute", h1_style))
    story.append(Paragraph("Amazon EC2 provides resizable compute capacity in the cloud. It eliminates the need to invest in physical hardware up front, enabling rapid development and deployment of scalable software systems.", body_style))

    story.append(Paragraph("2.1 The Five Essential Pillars of an EC2 Instance", h2_style))
    story.append(Paragraph("• <b>AMI (Amazon Machine Image):</b> The foundational template providing the OS, patch level, and application stack. Options include Amazon Linux 2023, Ubuntu, and Red Hat. You can also bake <b>Custom AMIs</b> (Golden Images) with your software pre-installed.", bullet_style))
    story.append(Paragraph("• <b>Instance Type:</b> Defines vCPU, memory (RAM), disk performance, and network bandwidth. Format: <code>t3.micro</code> (Family = t, Generation = 3, Size = micro). Free tier utilizes <code>t2.micro</code> or <code>t3.micro</code> (1 vCPU, 1 GiB RAM).", bullet_style))
    story.append(Paragraph("• <b>Key Pair (.pem / .ppk):</b> An asymmetric cryptographic key used to authenticate SSH sessions. AWS retains the Public Key; the developer downloads the Private Key. AWS never stores a copy of your private key!", bullet_style))
    story.append(Paragraph("• <b>Security Group:</b> The virtual firewall attached to the instance's virtual network interface (ENI). By default, ALL inbound traffic is blocked. Outbound is fully open.", bullet_style))
    story.append(Paragraph("• <b>Storage (EBS Root Volume):</b> The physical operating system disk where the kernel, binaries, and system libraries reside (typically 8 GB – 30 GB gp3).", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2.2 EC2 Lifecycle & Billing State Machine", h2_style))
    story.append(Paragraph("Understanding what state an instance is in is critical for budget management and cloud architecture:", body_style))

    lifecycle_data = [
        [Paragraph("<b>State</b>", bullet_style), Paragraph("<b>Compute Billed?</b>", bullet_style), Paragraph("<b>EBS Storage Billed?</b>", bullet_style), Paragraph("<b>Public IP Address</b>", bullet_style), Paragraph("<b>Action / Real-World Meaning</b>", bullet_style)],
        [
            Paragraph("<b>Pending</b>", body_style), Paragraph("No", body_style), Paragraph("Yes", body_style), Paragraph("Allocating", body_style),
            Paragraph("AWS is provisioning physical host and attaching virtual hardware.", body_style)
        ],
        [
            Paragraph("<b>Running</b>", body_style), Paragraph("<b>YES</b>", body_style), Paragraph("<b>YES</b>", body_style), Paragraph("Active", body_style),
            Paragraph("Instance is powered on; OS is active; workloads running.", body_style)
        ],
        [
            Paragraph("<b>Stopping</b>", body_style), Paragraph("No", body_style), Paragraph("Yes", body_style), Paragraph("Releasing", body_style),
            Paragraph("Graceful shutdown in progress (closing processes, flushing cache).", body_style)
        ],
        [
            Paragraph("<b>Stopped</b>", body_style), Paragraph("<b>$0.00 / hr</b>", body_style), Paragraph("<b>YES (storage)</b>", body_style), Paragraph("<b>Released!</b>", body_style),
            Paragraph("Engine is off. Data on EBS is safe. Public IP is surrendered unless using Elastic IP.", body_style)
        ],
        [
            Paragraph("<b>Terminated</b>", body_style), Paragraph("<b>$0.00 / hr</b>", body_style), Paragraph("<b>$0.00 (Deleted)</b>", body_style), Paragraph("None", body_style),
            Paragraph("Instance permanently destroyed. Root EBS disk deleted by default.", body_style)
        ]
    ]

    t_lifecycle = Table(lifecycle_data, colWidths=[65, 75, 80, 84, 200])
    t_lifecycle.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AWS_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_lifecycle)
    story.append(Spacer(1, 10))

    # User Data
    story.append(Paragraph("2.3 Automated Bootstrapping: EC2 User Data", h2_style))
    story.append(Paragraph("Instead of logging into every instance manually, you pass a startup shell script in the <b>User Data</b> field during launch. It executes with <code>root</code> privileges on the first system boot:", body_style))

    code_sample_1 = [
        [Paragraph(
            "#!/bin/bash<br/>"
            "# 1. Update OS package repositories<br/>"
            "dnf update -y<br/>"
            "# 2. Install web server, git, and python runtime<br/>"
            "dnf install -y httpd python3 git<br/>"
            "# 3. Start Apache HTTP daemon and configure boot persistence<br/>"
            "systemctl start httpd<br/>"
            "systemctl enable httpd<br/>"
            "# 4. Fetch instance metadata and publish student landing page<br/>"
            "TOKEN=$(curl -s -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600')<br/>"
            "IID=$(curl -s -H 'X-aws-ec2-metadata-token: '$TOKEN http://169.254.169.254/latest/meta-data/instance-id)<br/>"
            "echo '&lt;h1&gt;TASK Telangana Cloud Lab · EC2 Instance '$IID'&lt;/h1&gt;' &gt; /var/www/html/index.html",
            code_style
        )]
    ]
    t_code1 = Table(code_sample_1, colWidths=[504])
    t_code1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_code1)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 3: STORAGE TRIAD (EBS vs EFS vs S3)
    # =========================================================================
    story.append(Paragraph("3. Storage Shootout: Block (EBS) vs File (EFS) vs Object (S3)", h1_style))
    story.append(Paragraph("Choosing the wrong storage service is the #1 cause of cloud cost overruns and latency bottlenecks. AWS provides three distinct storage archetypes:", body_style))

    storage_compare = [
        [Paragraph("<b>Dimension</b>", bullet_style), Paragraph("<b>Amazon EBS</b>", bullet_style), Paragraph("<b>Amazon EFS</b>", bullet_style), Paragraph("<b>Amazon S3</b>", bullet_style)],
        [
            Paragraph("<b>Analogy</b>", body_style),
            Paragraph("Car's Built-in Trunk", body_style),
            Paragraph("Shared Fleet Roof Rack", body_style),
            Paragraph("Global Shipping Depot", body_style)
        ],
        [
            Paragraph("<b>Storage Type</b>", body_style),
            Paragraph("Block Storage", body_style),
            Paragraph("File Storage (Hierarchical)", body_style),
            Paragraph("Object Storage (Flat key-val)", body_style)
        ],
        [
            Paragraph("<b>Protocol</b>", body_style),
            Paragraph("NVMe / SCSI raw blocks", body_style),
            Paragraph("NFSv4 network share", body_style),
            Paragraph("REST API (HTTP / HTTPS)", body_style)
        ],
        [
            Paragraph("<b>Scope / Availability</b>", body_style),
            Paragraph("Bound to single AZ", body_style),
            Paragraph("Multi-AZ (Regional)", body_style),
            Paragraph("Multi-AZ (Global API)", body_style)
        ],
        [
            Paragraph("<b>Concurrent Mounts</b>", body_style),
            Paragraph("1 EC2 (unless Multi-Attach io2)", body_style),
            Paragraph("1000s of EC2s simultaneously", body_style),
            Paragraph("Unlimited HTTP clients", body_style)
        ],
        [
            Paragraph("<b>Durability</b>", body_style),
            Paragraph("99.8% to 99.999%", body_style),
            Paragraph("99.999999999% (11 9's)", body_style),
            Paragraph("99.999999999% (11 9's)", body_style)
        ],
        [
            Paragraph("<b>Primary Use Case</b>", body_style),
            Paragraph("OS Boot drives, DB files", body_style),
            Paragraph("Shared web uploads, CMS", body_style),
            Paragraph("Media assets, backups, big data", body_style)
        ]
    ]

    t_store = Table(storage_compare, colWidths=[95, 130, 135, 144])
    t_store.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AWS_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_store)
    story.append(Spacer(1, 10))

    # S3 Security & Bucket Policy
    story.append(Paragraph("3.1 Amazon S3 Security: Block Public Access & HTTPS Bucket Policy", h2_style))
    story.append(Paragraph("Every student bucket must be protected using industry security baselines. Since 2023, AWS enables <b>Block Public Access (BPA)</b> automatically. Below is the production-grade JSON policy to enforce secure in-transit encryption (HTTPS/TLS) across all client operations:", body_style))

    code_policy = [
        [Paragraph(
            "{\n"
            '  "Version": "2012-10-17",\n'
            '  "Statement": [\n'
            "    {\n"
            '      "Sid": "EnforceHTTPSRequestsOnly",\n'
            '      "Effect": "Deny",\n'
            '      "Principal": "*",\n'
            '      "Action": "s3:*",\n'
            '      "Resource": [\n'
            '        "arn:aws:s3:::task-nalgonda-demo-bucket",\n'
            '        "arn:aws:s3:::task-nalgonda-demo-bucket/*"\n'
            "      ],\n"
            '      "Condition": {\n'
            '        "Bool": { "aws:SecureTransport": "false" }\n'
            "      }\n"
            "    }\n"
            "  ]\n"
            "}",
            code_style
        )]
    ]
    t_policy = Table(code_policy, colWidths=[504])
    t_policy.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_policy)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 4: VPC NETWORKING
    # =========================================================================
    story.append(Paragraph("4. Amazon VPC: Building Your Isolated Private Network", h1_style))
    story.append(Paragraph("A <b>Virtual Private Cloud (VPC)</b> is your dedicated virtual network in AWS. It closely resembles a traditional on-premises data center network, but offers the elastic scalability of AWS infrastructure.", body_style))

    story.append(Paragraph("4.1 Core Networking Components", h2_style))
    story.append(Paragraph("• <b>CIDR Block:</b> Defines the total IP range. Standard: <code>10.0.0.0/16</code> = 65,536 private IPv4 addresses.", bullet_style))
    story.append(Paragraph("• <b>Subnets:</b> Distinct IP segments bound to specific Availability Zones (e.g., <code>10.0.1.0/24</code> in <i>ap-south-1a</i>). AWS reserves 5 IP addresses in every subnet (.0 network, .1 router, .2 DNS, .3 reserved, .255 broadcast).", bullet_style))
    story.append(Paragraph("• <b>Internet Gateway (IGW):</b> Highly available horizontally scaled component that provides direct 2-way routing to the public internet.", bullet_style))
    story.append(Paragraph("• <b>Route Tables:</b> Routing rules determining where packets flow. <b>A subnet is Public ONLY if its route table points <code>0.0.0.0/0</code> to an IGW.</b> Otherwise, it is Private!", bullet_style))
    story.append(Paragraph("• <b>NAT Gateway:</b> Network Address Translation service placed in a Public Subnet that lets instances in Private Subnets connect outbound to the internet (for package updates) while keeping them invisible to incoming internet probes.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("4.2 Security Groups vs Network ACLs (NACL)", h2_style))

    sec_data = [
        [Paragraph("<b>Feature</b>", bullet_style), Paragraph("<b>Security Group (Instance Level)</b>", bullet_style), Paragraph("<b>Network ACL (Subnet Level)</b>", bullet_style)],
        [
            Paragraph("<b>Analogy</b>", body_style),
            Paragraph("Personal car bodyguard in the passenger seat", body_style),
            Paragraph("Toll booth barrier at district highway gate", body_style)
        ],
        [
            Paragraph("<b>Operates At</b>", body_style),
            Paragraph("Network Interface (ENI) / Instance level", body_style),
            Paragraph("Subnet boundary level", body_style)
        ],
        [
            Paragraph("<b>Statefulness</b>", body_style),
            Paragraph("<b>STATEFUL:</b> Return traffic is automatically allowed!", body_style),
            Paragraph("<b>STATELESS:</b> Inbound and Outbound must be explicitly opened!", body_style)
        ],
        [
            Paragraph("<b>Rule Types</b>", body_style),
            Paragraph("ALLOW rules only (No deny rules)", body_style),
            Paragraph("ALLOW and DENY rules supported", body_style)
        ],
        [
            Paragraph("<b>Evaluation Order</b>", body_style),
            Paragraph("All rules evaluated before permit decision", body_style),
            Paragraph("Strict numerical order (Rule 100 before 200). First match wins!", body_style)
        ]
    ]

    t_sec = Table(sec_data, colWidths=[110, 195, 199])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AWS_NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_sec)
    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 5: STEP-BY-STEP HANDS-ON LAB GUIDE
    # =========================================================================
    story.append(Paragraph("5. Step-by-Step Hands-on Student Lab Guide", h1_style))
    story.append(Paragraph("Follow these exact steps in the AWS Management Console during class. All steps are designed strictly within the AWS Free Tier:", body_style))

    story.append(Paragraph("<b>Lab 1: Launch an EC2 Web Server with Automated User Data</b>", h2_style))
    story.append(Paragraph("1. Log in to the AWS Console and select Region <b>ap-south-1 (Mumbai)</b>.", bullet_style))
    story.append(Paragraph("2. Navigate to <b>EC2 Dashboard</b> and click <b>Launch Instance</b>.", bullet_style))
    story.append(Paragraph("3. <b>Name:</b> <code>task-web-server-01</code>.", bullet_style))
    story.append(Paragraph("4. <b>Application and OS Images (AMI):</b> Select <b>Amazon Linux 2023 AMI</b> (Free tier eligible).", bullet_style))
    story.append(Paragraph("5. <b>Instance Type:</b> Select <code>t2.micro</code> or <code>t3.micro</code>.", bullet_style))
    story.append(Paragraph("6. <b>Key Pair:</b> Click <i>Create new key pair</i> -> Name: <code>task-key</code> -> Key pair type: <code>RSA</code> -> Private key format: <code>.pem</code> -> Click <i>Create key pair</i> (browser downloads <code>task-key.pem</code>).", bullet_style))
    story.append(Paragraph("7. <b>Network Settings:</b> Click <i>Edit</i> -> Check <i>Allow SSH traffic from Anywhere (or My IP)</i> -> Check <i>Allow HTTP traffic from the internet</i>.", bullet_style))
    story.append(Paragraph("8. <b>Advanced Details:</b> Scroll to the very bottom to <b>User data</b>. Paste the bash script from Section 2.3 of this handbook.", bullet_style))
    story.append(Paragraph("9. Click <b>Launch Instance</b>. Wait 60 seconds until <i>Instance State = Running</i>.", bullet_style))
    story.append(Paragraph("10. Copy the <b>Public IPv4 address</b>, open a new browser tab, and paste: <code>http://&lt;PUBLIC-IP&gt;</code>. You should see your custom welcome page!", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Lab 2: Create a Custom AMI (Golden Image)</b>", h2_style))
    story.append(Paragraph("1. In EC2 Instances list, select <code>task-web-server-01</code>.", bullet_style))
    story.append(Paragraph("2. Click <b>Actions</b> -> <b>Image and templates</b> -> <b>Create image</b>.", bullet_style))
    story.append(Paragraph("3. <b>Image name:</b> <code>task-golden-ami-v1</code>.", bullet_style))
    story.append(Paragraph("4. Click <b>Create image</b>. Navigate to <b>AMIs</b> on the left sidebar to watch it change to <i>available</i>.", bullet_style))
    story.append(Paragraph("5. Select your new AMI and click <b>Launch instance from AMI</b>. Your new instance will start with Apache and Python pre-configured in under 30 seconds!", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Lab 3: S3 Bucket Creation & HTTPS Policy Enforcement</b>", h2_style))
    story.append(Paragraph("1. Navigate to <b>Amazon S3</b> and click <b>Create bucket</b>.", bullet_style))
    story.append(Paragraph("2. <b>Bucket name:</b> <code>task-nalgonda-&lt;your-name&gt;-2026</code> (Must be globally unique!).", bullet_style))
    story.append(Paragraph("3. Leave <b>Block all public access</b> CHECKED (Never uncheck this in class!).", bullet_style))
    story.append(Paragraph("4. Click <b>Create bucket</b>. Upload a small image or text file.", bullet_style))
    story.append(Paragraph("5. Click the <b>Permissions</b> tab -> Scroll to <b>Bucket policy</b> -> Click <b>Edit</b>.", bullet_style))
    story.append(Paragraph("6. Paste the HTTPS-only JSON policy from Section 3.1 of this handbook (replace bucket name with your actual bucket name).", bullet_style))
    story.append(Paragraph("7. Click <b>Save changes</b>. Your bucket is now secured against insecure HTTP transmission!", bullet_style))

    story.append(Spacer(1, 14))

    # =========================================================================
    # SECTION 6: COST SHIELD & CLEANUP CHECKLIST
    # =========================================================================
    story.append(Paragraph("6. Daily Cost Shield: Zero-Dollar Student Hygiene", h1_style))
    story.append(Paragraph("To ensure students never incur any AWS credit card charges, follow the <b>Daily Sunset Checklist</b> before leaving the college lab:", body_style))

    cleanup_box = [
        [Paragraph(
            "<b>DAILY LAB DECOMMISSION CHECKLIST:</b><br/>"
            "1. <b>STOP or TERMINATE EC2 Instances:</b> Select instance -> <i>Instance State</i> -> <i>Stop Instance</i> (or <i>Terminate</i> if lab complete).<br/>"
            "2. <b>DELETE Unattached EBS Volumes:</b> Go to <i>Volumes</i> -> Check for volumes in <i>available</i> state -> <i>Actions</i> -> <i>Delete volume</i>.<br/>"
            "3. <b>RELEASE Elastic IPs:</b> Unallocated Elastic IPs cost $0.005/hr if not attached to a running instance! Go to <i>Elastic IPs</i> -> <i>Actions</i> -> <i>Release Elastic IP</i>.<br/>"
            "4. <b>EMPTY & DELETE Test S3 Buckets:</b> If test buckets are no longer needed, click <i>Empty</i>, then click <i>Delete</i>.<br/>"
            "5. <b>CHECK BILLING DASHBOARD:</b> Open <i>AWS Billing and Cost Management</i> once every week to verify $0.00 balance.",
            callout_style
        )]
    ]
    t_clean = Table(cleanup_box, colWidths=[504])
    t_clean.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_clean)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled professional PDF guide: {output_filename}")

if __name__ == "__main__":
    out_pdf = r"F:\Task( Telangana )\Nalgonda\Projects\task\module_03_aws_core\notes\Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf"
    build_pdf(out_pdf)
