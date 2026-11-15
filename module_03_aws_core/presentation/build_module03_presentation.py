"""
Script to generate the expanded 3-Day Module 03 AWS Core Services Masterclass Presentation.
Fixes code block text visibility with high-contrast colors.
Covers:
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
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    AWS_NAVY = RGBColor(0x23, 0x2F, 0x3E)      # #232F3E
    AWS_SQUID = RGBColor(0x16, 0x1E, 0x2D)     # #161E2D
    AWS_ORANGE = RGBColor(0xFF, 0x99, 0x00)    # #FF9900
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    DARK_TEXT = RGBColor(0x1A, 0x20, 0x2C)     # #1A202C
    MUTED_TEXT = RGBColor(0x5A, 0x65, 0x78)    # #5A6578
    CARD_BG = RGBColor(0xF4, 0xF6, 0xF8)       # #F4F6F8
    CARD_BORDER = RGBColor(0xD5, 0xDB, 0xDB)   # #D5DBDB

    # Code card styling (HIGH CONTRAST)
    TERMINAL_BG = RGBColor(0x0F, 0x17, 0x2A)   # #0F172A (Deep midnight slate)
    CODE_GREEN = RGBColor(0x4A, 0xDE, 0x80)    # #4ADE80 (Bright terminal green)
    CODE_CYAN = RGBColor(0x38, 0xBD, 0xF8)     # #38BDF8 (Sky blue)
    CODE_YELLOW = RGBColor(0xFB, 0xBF, 0x24)   # #FBBF24 (Bright amber)
    CODE_WHITE = RGBColor(0xF8, 0xFA, 0xFC)    # #F8FAFC (Crisp off-white)
    CODE_COMMENT = RGBColor(0x94, 0xA3, 0xB8)  # #94A3B8 (Light slate comment)

    def add_header(slide, title_text, day_tag="DAY 1", category_text="TASK TELANGANA · CLOUD SOFTWARE DEVELOPER"):
        # Header banner
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = AWS_NAVY
        header_shape.line.fill.background()

        # Accent line under header
        line_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.15), Inches(13.333), Inches(0.06))
        line_shape.fill.solid()
        line_shape.fill.fore_color.rgb = AWS_ORANGE
        line_shape.line.fill.background()

        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.95))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0)
        tf.margin_left = Inches(0)

        p_cat = tf.paragraphs[0]
        p_cat.text = f"{category_text.upper()}  |  {day_tag}"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = AWS_ORANGE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(21)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

    def add_footer(slide, current_page=None, total_pages=30):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_top = Inches(0)
        p = tf.paragraphs[0]
        p.text = "Trainer: Sundeep Hiremat  |  Nalgonda Training Center  |  AWS DVA-C02 Alignment  |  3-Day Masterclass"
        p.font.size = Pt(10)
        p.font.color.rgb = MUTED_TEXT

        if current_page:
            p2 = tf.add_paragraph()
            p2.text = f"{current_page} / {total_pages}"
            p2.alignment = PP_ALIGN.RIGHT
            p2.font.size = Pt(10)
            p2.font.color.rgb = MUTED_TEXT

    def add_card(slide, left, top, width, height, title, items, card_bg=CARD_BG, border_color=CARD_BORDER, title_color=AWS_NAVY, text_color=DARK_TEXT, is_bullet=True):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = card_bg
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tx = slide.shapes.add_textbox(Inches(left + 0.22), Inches(top + 0.18), Inches(width - 0.44), Inches(height - 0.36))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0)
        tf.margin_left = Inches(0)

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(15)
        p0.font.bold = True
        p0.font.color.rgb = title_color

        for item in items:
            p = tf.add_paragraph()
            if is_bullet:
                p.text = f"• {item}"
            else:
                p.text = item
            p.font.size = Pt(11)
            p.font.color.rgb = text_color
            p.space_before = Pt(3)

    def add_code_card(slide, left, top, width, height, title, lines):
        """Adds a high-contrast terminal code box with crystal clear light text."""
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = TERMINAL_BG
        card.line.color.rgb = RGBColor(0x33, 0x41, 0x55)
        card.line.width = Pt(1.5)

        tx = slide.shapes.add_textbox(Inches(left + 0.22), Inches(top + 0.18), Inches(width - 0.44), Inches(height - 0.36))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0)
        tf.margin_left = Inches(0)

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = AWS_ORANGE

        for line in lines:
            p = tf.add_paragraph()
            p.text = line
            p.font.name = "Consolas"
            p.font.size = Pt(9.5)
            p.space_before = Pt(2)
            if line.startswith("#"):
                p.font.color.rgb = CODE_COMMENT
            elif any(line.strip().startswith(cmd) for cmd in ["aws", "docker", "systemctl", "dnf", "curl", "chmod", "ssh"]):
                p.font.color.rgb = CODE_CYAN
            elif "{" in line or "}" in line or ":" in line:
                p.font.color.rgb = CODE_YELLOW
            else:
                p.font.color.rgb = CODE_WHITE

    # =================================================================
    # SLIDE 1: Title Slide (Grand Course Header)
    # =================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = AWS_SQUID
    bg.line.fill.background()

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.18), Inches(3.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = AWS_ORANGE
    bar.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11.0), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "TASK TELANGANA · CLOUD SOFTWARE DEVELOPER TRAINING"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AWS_ORANGE

    p2 = tf.add_paragraph()
    p2.text = "Module 03: AWS Core Services & Infrastructure"
    p2.font.size = Pt(34)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "The 3-Day Comprehensive Masterclass\nEC2, Storage Triad, Databases, VPC Networking, Containers (Docker/ECR/ECS) & IaC CloudFormation"
    p3.font.size = Pt(17)
    p3.font.color.rgb = RGBColor(0xD1, 0xD5, 0xDB)
    p3.space_before = Pt(10)

    p4 = tf.add_paragraph()
    p4.text = "Trainer: Sundeep Hiremat  |  Nalgonda Center  |  AWS DVA-C02 Alignment  |  Vehicle Metaphor Guide"
    p4.font.size = Pt(13)
    p4.font.color.rgb = AWS_ORANGE
    p4.space_before = Pt(20)

    # =================================================================
    # SLIDE 2: 3-Day Course Delivery Roadmap
    # =================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "3-Day Masterclass Roadmap & Learning Architecture", "ROADMAP")
    add_footer(s2, 2, 30)

    add_card(s2, 0.8, 1.5, 3.6, 5.2, "Day 1: Compute & Storage", [
        "Global Infrastructure: Regions, AZs, Edge.",
        "What is Multi-AZ vs Multi-Region.",
        "EC2: AMI, Types, Key Pair, Security Groups.",
        "Bootstrapping automation with User Data.",
        "Custom AMIs (Golden Images) & Lifecycles.",
        "Storage Triad: Block (EBS) vs File (EFS) vs Object (S3).",
        "S3 Security: Block Public Access & HTTPS Policies."
    ], card_bg=RGBColor(0xEA, 0xF2, 0xF8))

    add_card(s2, 4.8, 1.5, 3.6, 5.2, "Day 2: DBs, Network & Edge", [
        "Databases: RDS vs Aurora vs DynamoDB.",
        "In-Memory Caching with ElastiCache (Redis).",
        "VPC Isolation: CIDR blocks (10.0.0.0/16).",
        "Public Subnets vs Private Subnets.",
        "Internet Gateway (IGW) vs NAT Gateway.",
        "Security Groups (Stateful) vs NACLs (Stateless).",
        "ALB vs NLB, CloudFront CDN & AWS WAF.",
        "Enterprise 3-Tier Web Architecture Pattern."
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    add_card(s2, 8.8, 1.5, 3.7, 5.2, "Day 3: Containers & IaC", [
        "Containers & Docker 101 fundamentals.",
        "Amazon ECR: CLI build, tag, login & push.",
        "Amazon ECS: EC2 Launch Type vs AWS Fargate.",
        "ECS Containers vs AWS Lambda Containers.",
        "Infrastructure as Code (IaC) with CloudFormation.",
        "CloudFormation Anatomy: Parameters, Resources, Outputs.",
        "CloudFormation Drift Detection & Remediation.",
        "Student Decommission & Cost Shield."
    ], card_bg=RGBColor(0xEA, 0xFA, 0xEA))

    # =================================================================
    # SLIDE 3: The Grand Vehicle Metaphor (The Anchor)
    # =================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Grand Vehicle Metaphor: The Cloud as an Automobile Fleet", "DAY 1")
    add_footer(s3, 3, 30)

    add_card(s3, 0.8, 1.5, 2.7, 5.2, "EC2 = Rental Car", [
        "Rent an engine on-demand.",
        "AMI = Car Blueprint (Ubuntu/Linux).",
        "Instance Type = Horsepower (t3.micro).",
        "Key Pair = Physical ignition key.",
        "User Data = Pre-ignition accessories."
    ], card_bg=RGBColor(0xEA, 0xF2, 0xF8))

    add_card(s3, 3.8, 1.5, 2.7, 5.2, "EBS = Car Trunk", [
        "Personal hard drive bolted to 1 car.",
        "High speed local block storage.",
        "Luggage stays safe when car stops.",
        "Snapshot = Backup copy sent to central warehouse."
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    add_card(s3, 6.8, 1.5, 2.7, 5.2, "EFS = Fleet Cargo Rack", [
        "Shared roof rack for 100+ cars.",
        "All cars in different garages (AZs) access simultaneously.",
        "NFS protocol: real-time updates."
    ], card_bg=RGBColor(0xEA, 0xFA, 0xEA))

    add_card(s3, 9.8, 1.5, 2.7, 5.2, "S3 = Global Warehouse", [
        "Infinite shipping depot outside the car.",
        "Buckets = Storage bays.",
        "Objects = Cargo boxes.",
        "Reachable from any highway (HTTPS).",
        "11 9's durability (practically indestructible)."
    ], card_bg=RGBColor(0xFD, 0xED, 0xEC))

    # =================================================================
    # SLIDE 4: Global Infrastructure: Regions, AZs, Edge & Multi-AZ
    # =================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Global Infrastructure: Regions, AZs, Multi-AZ & Multi-Region", "DAY 1")
    add_footer(s4, 4, 30)

    add_card(s4, 0.8, 1.5, 5.6, 5.2, "Regions vs Availability Zones (AZs)", [
        "AWS Region: A distinct physical geographical location around the world (e.g. ap-south-1 Mumbai, us-east-1 N. Virginia).",
        "Availability Zone (AZ): One or more discrete data centers with redundant power, networking, and connectivity within a Region.",
        "• Each Region contains at least 3 AZs (e.g. ap-south-1a, 1b, 1c).",
        "• AZs are connected via ultra-low latency private optical fiber.",
        "How to Choose a Region:",
        "1. Latency: Pick the region physically closest to your end users.",
        "2. Compliance / Data Sovereignty: Indian citizen data stored in India.",
        "3. Service Availability: Newest AI/Cloud features release in us-east-1 first.",
        "4. Cost: Pricing varies slightly across regions due to local taxes."
    ])

    add_card(s4, 6.8, 1.5, 5.7, 5.2, "What is Multi-AZ vs Multi-Region?", [
        "Multi-AZ Architecture (High Availability within 1 Region):",
        "• Resources deployed across 2 or 3 AZs in the same city.",
        "• Synchronous replication: If lightning destroys data center AZ-a, the standby in AZ-b takes over in 60 seconds with ZERO data loss!",
        "• SLA: 99.99% availability.",
        "",
        "Multi-Region Architecture (Disaster Recovery & Global Scale):",
        "• Resources duplicated across different continents (e.g. Mumbai + Frankfurt).",
        "• Asynchronous replication: Protects against country-wide outages.",
        "• Edge Locations: 600+ points of presence running CloudFront CDN closer to users to cache static media and lower latency."
    ])

    # =================================================================
    # SLIDE 5: EC2 Anatomy & Components
    # =================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Anatomy of an EC2 Instance: The 5 Essential Pillars", "DAY 1")
    add_footer(s5, 5, 30)

    add_card(s5, 0.8, 1.5, 5.6, 2.5, "1. AMI (Amazon Machine Image) — The Chassis", [
        "Pre-packaged template with OS, initial software, and base configurations.",
        "Options: Amazon Linux 2023, Ubuntu 22.04/24.04, Windows Server, Red Hat.",
        "Custom AMIs: You can install tools, configure apps, and snapshot your own custom AMI!"
    ])

    add_card(s5, 6.8, 1.5, 5.7, 2.5, "2. Instance Type — The Engine Size", [
        "Naming syntax: <Family><Generation>.<Size> (e.g., t3.micro, c5.xlarge).",
        "General Purpose (t3, m5) — Balanced compute, memory, and networking.",
        "Compute Optimized (c5, c6g) — High CPU for compute-intensive tasks.",
        "Memory Optimized (r5, r6g) — Heavy RAM for in-memory DBs and caching."
    ])

    add_card(s5, 0.8, 4.3, 5.6, 2.5, "3. Key Pair (.pem / .ppk) — The Ignition Key", [
        "Asymmetric cryptography: AWS holds Public Key; You download Private Key.",
        "AWS NEVER saves a copy of your private key — if lost, SSH access is gone!",
        ".pem format for OpenSSH (Linux/Mac/PowerShell), .ppk for PuTTY on Windows."
    ])

    add_card(s5, 6.8, 4.3, 5.7, 2.5, "4. Security Group & 5. Storage (EBS Root)", [
        "Security Group: Virtual firewall controlling inbound & outbound network traffic.",
        "Default Inbound: Everything blocked! You must explicitly allow SSH (22) or HTTP (80).",
        "Root EBS Volume: The primary operating system disk (typically 8 GB – 30 GB gp3)."
    ])

    # =================================================================
    # SLIDE 6: EC2 Lifecycle & Billing State Machine
    # =================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "EC2 Lifecycle & Billing: The State Transition Machine", "DAY 1")
    add_footer(s6, 6, 30)

    add_card(s6, 0.8, 1.5, 3.6, 5.2, "States & Transitions", [
        "1. Pending: Provisioning on underlying physical host.",
        "2. Running: OS booted; compute & storage billing active.",
        "3. Stopping: Graceful OS shutdown in progress.",
        "4. Stopped: Engine off! Compute charge stops ($0/hr). Only EBS disk billed.",
        "5. Shutting-Down: Permanent teardown initiated.",
        "6. Terminated: Permanently deleted. Root EBS volume released."
    ])

    add_card(s6, 4.8, 1.5, 3.6, 5.2, "Parking vs Scrapping the Car", [
        "Stop = Turning off car engine & parking in garage.",
        "• Compute meter stops ticking ($0/hr).",
        "• Small rent paid for parked car's trunk (EBS).",
        "• Public IP address changes when restarted!",
        "Terminate = Sending car to scrap crusher.",
        "• Disk destroyed, instance permanently deleted, all billing ceases."
    ])

    add_card(s6, 8.8, 1.5, 3.7, 5.2, "Student Cost Rules", [
        "Always STOP instances at the end of every lab!",
        "Always TERMINATE throwaway test instances.",
        "Verify your region is set to ap-south-1 consistently.",
        "Keep root volume within AWS Free Tier limits (30 GB EBS free/month).",
        "Set an AWS Billing Alarm at $0.01."
    ])

    # =================================================================
    # SLIDE 7: EC2 Bootstrapping with User Data (FIXED CODE VISIBILITY)
    # =================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "EC2 Automation: Bootstrapping with User Data", "DAY 1")
    add_footer(s7, 7, 30)

    add_card(s7, 0.8, 1.5, 5.4, 5.2, "What is User Data?", [
        "A startup shell script that executes automatically on first boot as root.",
        "Eliminates manual SSH login to install packages or start web servers.",
        "Vehicle Analogy: The pre-delivery checklist that automatically fuels the car, tunes the radio, and turns on the AC before you touch the wheel.",
        "Runs only ONCE when the instance boots for the first time.",
        "Log files saved at: /var/log/cloud-init-output.log for debugging."
    ])

    add_code_card(s7, 6.6, 1.5, 5.9, 5.2, "Sample Production Bootstrap Script", [
        "#!/bin/bash",
        "# 1. Update OS packages",
        "dnf update -y",
        "",
        "# 2. Install Apache web server & Python",
        "dnf install -y httpd python3 git",
        "",
        "# 3. Start & enable web server service",
        "systemctl start httpd",
        "systemctl enable httpd",
        "",
        "# 4. Fetch dynamic instance ID using IMDSv2",
        "TOKEN=$(curl -s -X PUT 'http://169.254.169.254/latest/api/token' \\",
        "  -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600')",
        "IID=$(curl -s -H 'X-aws-ec2-metadata-token: '$TOKEN \\",
        "  http://169.254.169.254/latest/meta-data/instance-id)",
        "",
        "# 5. Create rich welcome landing page",
        "echo '<h1>Welcome to TASK Cloud Lab: '$IID'</h1>' \\",
        "  > /var/www/html/index.html"
    ])

    # =================================================================
    # SLIDE 8: Connecting to EC2 (SSH, Putty & Instance Connect)
    # =================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Connecting to Your EC2 Instance: 3 Methods", "DAY 1")
    add_footer(s8, 8, 30)

    add_card(s8, 0.8, 1.5, 3.6, 5.2, "1. EC2 Instance Connect", [
        "Browser-based terminal inside AWS Management Console.",
        "No software installation needed on student laptops.",
        "Pushes temporary 60-second SSH keys via AWS API.",
        "Requirements: Instance needs Public IP and Port 22 open.",
        "Best for beginners & restricted college labs!"
    ])

    add_card(s8, 4.8, 1.5, 3.6, 5.2, "2. Native SSH (Terminal / Mac / Linux)", [
        "1. Open terminal where key is saved.",
        "2. Set permissions (Linux/Mac):",
        "   chmod 400 task-key.pem",
        "3. Connect:",
        "   ssh -i task-key.pem ec2-user@<IP>",
        "",
        "Default usernames:",
        "• Amazon Linux: ec2-user",
        "• Ubuntu: ubuntu",
        "• Red Hat: ec2-user"
    ])

    add_card(s8, 8.8, 1.5, 3.7, 5.2, "3. PuTTY on Windows", [
        "For older Windows systems:",
        "1. Convert .pem to .ppk using PuTTYgen.",
        "2. Open PuTTY.",
        "3. Host Name: ec2-user@<IP>",
        "4. Auth -> Credentials -> Browse .ppk.",
        "5. Click Open to launch session."
    ])

    # =================================================================
    # SLIDE 9: Custom AMIs & Golden Images
    # =================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Custom AMIs: Baking Golden Images for Scalability", "DAY 1")
    add_footer(s9, 9, 30)

    add_card(s9, 0.8, 1.5, 5.6, 5.2, "Why Create a Custom AMI?", [
        "Problem: Installing Python, libraries, and web apps manually on every new EC2 instance takes 15 minutes each time.",
        "Solution: Bake a Golden Image! Configure one instance perfectly, then snapshot it into an AMI.",
        "Vehicle Analogy: Modifying a base car into an emergency ambulance with sirens, medical gear, and stretchers. Then using that ambulance blueprint to manufacture 50 identical ambulances in minutes!",
        "Key Benefits:",
        "• Near-instant boot time for Auto Scaling fleets.",
        "• Consistency: Every server runs identical software versions.",
        "• Disaster recovery: Re-launch full application in another AZ in minutes."
    ])

    add_card(s9, 6.8, 1.5, 5.7, 5.2, "Step-by-Step: Baking an AMI in Console", [
        "Step 1: Launch base EC2 instance (Amazon Linux 2023).",
        "Step 2: Connect via SSH and install your application stack:",
        "   sudo dnf install -y python3-pip git nginx",
        "   git clone https://github.com/cloude-user/task.git",
        "Step 3: Test that application runs smoothly.",
        "Step 4: In AWS Console: Select Instance -> Actions -> Image and templates -> Create image.",
        "Step 5: Name image: task-golden-ami-v1.",
        "Step 6: Click Create Image (AWS takes clean disk snapshot).",
        "Step 7: Launch 10 new instances using task-golden-ami-v1 instantly!"
    ])

    # =================================================================
    # SLIDE 10: Storage Shootout: EBS vs EFS vs S3
    # =================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Storage Shootout: Block (EBS) vs File (EFS) vs Object (S3)", "DAY 1")
    add_footer(s10, 10, 30)

    add_card(s10, 0.8, 1.5, 3.6, 5.2, "Amazon EBS (Block)", [
        "Analogy: Built-in Car Trunk",
        "Scope: Bound to a SINGLE AZ.",
        "Attachment: Mounted to 1 EC2 instance at a time (like a USB drive).",
        "Protocol: Block-level (ext4, xfs, NTFS).",
        "Speed: Ultra-low millisecond latency; high IOPS.",
        "Best for: OS boot disks, databases (Postgres, MySQL)."
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    add_card(s10, 4.8, 1.5, 3.6, 5.2, "Amazon EFS (File)", [
        "Analogy: Shared Fleet Roof Cargo",
        "Scope: Regional (Multi-AZ automatically).",
        "Attachment: Mounted by HUNDREDS of EC2 instances concurrently across AZs.",
        "Protocol: Network File System (NFSv4). Standard folder hierarchy.",
        "Scalability: Grows and shrinks automatically.",
        "Best for: Shared web uploads, WordPress, CMS."
    ], card_bg=RGBColor(0xEA, 0xFA, 0xEA))

    add_card(s10, 8.8, 1.5, 3.7, 5.2, "Amazon S3 (Object)", [
        "Analogy: Global Shipping Depot",
        "Scope: Global web-accessible URL via HTTPS.",
        "Attachment: NOT a disk drive; accessed via REST API / SDK / CLI.",
        "Structure: Flat namespace (Buckets & Objects).",
        "Durability: 99.999999999% (11 9's) across 3+ AZs.",
        "Best for: Media files, datasets, backups."
    ], card_bg=RGBColor(0xFD, 0xED, 0xEC))

    # =================================================================
    # SLIDE 11: Amazon S3 Security & HTTPS Policy (FIXED CODE VISIBILITY)
    # =================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Amazon S3 Security: Block Public Access & HTTPS Policies", "DAY 1")
    add_footer(s11, 11, 30)

    add_card(s11, 0.8, 1.5, 5.4, 5.2, "S3 Core Security Controls", [
        "1. Bucket Naming Rules:",
        "• Globally unique across all AWS accounts in the world!",
        "• 3–63 characters, lowercase letters, numbers, and hyphens.",
        "2. Block Public Access (BPA):",
        "• Enabled by DEFAULT on every new bucket.",
        "• Prevents accidental leaks of confidential student files or company data.",
        "3. Default Encryption:",
        "• Encrypted server-side using SSE-S3 (AES-256) at zero extra cost.",
        "4. Bucket Policies:",
        "• JSON resource-based policy attached directly to bucket."
    ])

    add_code_card(s11, 6.6, 1.5, 5.9, 5.2, "JSON Policy: Enforcing HTTPS/TLS Only", [
        "{",
        '  "Version": "2012-10-17",',
        '  "Statement": [',
        "    {",
        '      "Sid": "EnforceTLSRequestsOnly",',
        '      "Effect": "Deny",',
        '      "Principal": "*",',
        '      "Action": "s3:*",',
        '      "Resource": [',
        '        "arn:aws:s3:::task-nalgonda-bucket",',
        '        "arn:aws:s3:::task-nalgonda-bucket/*"',
        "      ],",
        '      "Condition": {',
        '        "Bool": { "aws:SecureTransport": "false" }',
        "      }",
        "    }",
        "  ]",
        "}"
    ])

    # =================================================================
    # SLIDE 12: Database Decision Framework (RDS vs Aurora vs DynamoDB)
    # =================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Databases: RDS vs Aurora vs DynamoDB vs ElastiCache", "DAY 2")
    add_footer(s12, 12, 30)

    add_card(s12, 0.8, 1.5, 2.7, 5.2, "Amazon RDS (SQL)", [
        "Engines: Postgres, MySQL, MariaDB, Oracle, SQL Server.",
        "Multi-AZ: Synchronous standby in 2nd AZ for automatic failover.",
        "Read Replicas: Up to 15 async read copies to offload read reports.",
        "Managed: Automated daily backups, OS patching, minor version updates."
    ], card_bg=RGBColor(0xEA, 0xF2, 0xF8))

    add_card(s12, 3.8, 1.5, 2.7, 5.2, "Amazon Aurora", [
        "Cloud-native PostgreSQL & MySQL compatible engine.",
        "Architecture: 6-way replication of storage across 3 AZs.",
        "Performance: 5x faster than MySQL, 3x faster than standard Postgres.",
        "Aurora Serverless v2: Instant scaling from 0.5 to 128 ACUs in milliseconds!"
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    add_card(s12, 6.8, 1.5, 2.7, 5.2, "Amazon DynamoDB", [
        "Fully managed, serverless NoSQL Key-Value & Document store.",
        "Performance: Single-digit millisecond latency at any scale.",
        "Primary Keys: Partition Key (PK) & Sort Key (SK).",
        "Global Tables: Active-active multi-region replication."
    ], card_bg=RGBColor(0xEA, 0xFA, 0xEA))

    add_card(s12, 9.8, 1.5, 2.7, 5.2, "ElastiCache (Redis)", [
        "In-Memory Caching engine.",
        "Sub-millisecond response time by caching frequent SQL query results in RAM.",
        "Data structures: Strings, hashes, lists, sets, sorted sets.",
        "Ideal for user login session caches & real-time leaderboards."
    ], card_bg=RGBColor(0xFD, 0xED, 0xEC))

    # =================================================================
    # SLIDE 13: Database Decision Tree
    # =================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Database Selection Guide: When to Choose Which Service", "DAY 2")
    add_footer(s13, 13, 30)

    add_card(s13, 0.8, 1.5, 5.6, 5.2, "When to Choose Which Database?", [
        "Need Complex Relational Queries (JOINs) & ACID transactions?",
        "➔ Choose Amazon RDS (PostgreSQL/MySQL).",
        "",
        "Need Maximum Enterprise Throughput & Auto-Scaling SQL?",
        "➔ Choose Amazon Aurora (For enterprise workloads with high read traffic).",
        "",
        "Need High-Speed Scalable Key-Value / JSON Document storage?",
        "➔ Choose Amazon DynamoDB (E-commerce shopping cart, gaming profiles, telemetry).",
        "",
        "Need Sub-Millisecond Speed for Frequent Queries or Session State?",
        "➔ Choose Amazon ElastiCache (Redis) (Placed in front of RDS as a cache layer)."
    ])

    add_card(s13, 6.8, 1.5, 5.7, 5.2, "Architectural Comparison Table", [
        "Service | Data Model | Latency | Scaling",
        "--------------------------------------------------",
        "RDS | Relational SQL | Milliseconds | Vertical + Read Replicas",
        "Aurora | Relational SQL | Low-ms | Auto-storage + Serverless v2",
        "DynamoDB | NoSQL Key-Value | Single-digit ms | Horizontal auto-partition",
        "ElastiCache | In-Memory (RAM) | Microseconds | In-memory clustering",
        "S3 | Object / Files | Tens of ms | Infinite horizontal"
    ], is_bullet=False)

    # =================================================================
    # SLIDE 14: Amazon VPC: Your Private Highway System
    # =================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Amazon VPC: Your Isolated Private Highway System", "DAY 2")
    add_footer(s14, 14, 30)

    add_card(s14, 0.8, 1.5, 5.6, 5.2, "What is a VPC?", [
        "A logically isolated section of the AWS Cloud where you launch AWS resources in a virtual network you define.",
        "Vehicle Analogy: Your private gated business park / private racing circuit.",
        "CIDR Block (Classless Inter-Domain Routing):",
        "• Determines the IP address range for your entire private cloud.",
        "• Standard Production Range: 10.0.0.0/16 (Yields 65,536 private IP addresses).",
        "• AWS reserves 5 IP addresses in every subnet (.0 network, .1 router, .2 DNS, .3 reserved, .255 broadcast)."
    ])

    add_card(s14, 6.8, 1.5, 5.7, 5.2, "Core Networking Building Blocks", [
        "1. Subnets: Slices of the VPC assigned to specific Availability Zones.",
        "2. Internet Gateway (IGW): The 2-way front gate connecting VPC to public Internet.",
        "3. Route Tables: Road signs telling network packets where to travel next.",
        "4. NAT Gateway: One-way security tunnel allowing private instances to fetch internet updates without accepting incoming connections.",
        "5. Elastic IP (EIP): Static public IPv4 address that never changes when instance restarts."
    ])

    # =================================================================
    # SLIDE 15: Public vs Private Subnets (Route Table Logic)
    # =================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Public vs Private Subnets: The Route Table Decides!", "DAY 2")
    add_footer(s15, 15, 30)

    add_card(s15, 0.8, 1.5, 5.6, 5.2, "Public Subnet (The Front Showroom)", [
        "Definition: A subnet whose Route Table contains a direct route to an Internet Gateway (IGW).",
        "Route Table Entry:",
        "• Destination: 0.0.0.0/0 (All outside traffic)",
        "• Target: igw-xxxxxxxx (Internet Gateway)",
        "Use Cases:",
        "• Application Load Balancers (ALB) receiving public user web requests.",
        "• Public Bastion Hosts / Jump boxes.",
        "• Public-facing web servers.",
        "Every resource must have a Public IPv4 address to reach the internet."
    ], card_bg=RGBColor(0xEA, 0xF2, 0xF8))

    add_card(s15, 6.8, 1.5, 5.7, 5.2, "Private Subnet (The VIP Garage / Vault)", [
        "Definition: A subnet whose Route Table DOES NOT point to an IGW.",
        "Route Table Entry (For outbound internet access only):",
        "• Destination: 0.0.0.0/0",
        "• Target: nat-xxxxxxxx (NAT Gateway residing in a Public Subnet)",
        "Use Cases:",
        "• Backend microservices & application servers.",
        "• Databases (RDS MySQL/Postgres, Aurora, DynamoDB VPC endpoints).",
        "• Internal machine learning training nodes.",
        "Benefit: Completely protected from direct malicious hackers on the Internet!"
    ], card_bg=RGBColor(0xEA, 0xFA, 0xEA))

    # =================================================================
    # SLIDE 16: Security Groups vs NACLs
    # =================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Security Groups vs Network ACLs: Personal Bodyguard vs Gate Barrier", "DAY 2")
    add_footer(s16, 16, 30)

    add_card(s16, 0.8, 1.5, 5.6, 5.2, "Security Groups (Personal Bodyguard)", [
        "Level: Operates at the INSTANCE (ENI) level.",
        "State: STATEFUL.",
        "• If inbound traffic is allowed, outbound return traffic is automatically allowed, regardless of outbound rules!",
        "Rules:",
        "• ALLOW rules only (No explicit DENY rules).",
        "• All rules evaluated before decision.",
        "Analogy: A personal bodyguard sitting in the passenger seat who remembers who you invited inside."
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    add_card(s16, 6.8, 1.5, 5.7, 5.2, "Network ACLs - NACL (Toll Gate Barrier)", [
        "Level: Operates at the SUBNET boundary level.",
        "State: STATELESS.",
        "• Inbound and outbound traffic MUST be explicitly allowed in both directions!",
        "Rules:",
        "• Supports both ALLOW and DENY rules.",
        "• Evaluated in strict numerical order (Rule 100 before Rule 200). First match wins!",
        "Analogy: A highway toll gate barrier that checks every license plate entering and exiting the district."
    ], card_bg=RGBColor(0xFD, 0xED, 0xEC))

    # =================================================================
    # SLIDE 17: ALB vs NLB & CloudFront Edge Delivery
    # =================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Traffic Routing & Acceleration: ALB, NLB & CloudFront", "DAY 2")
    add_footer(s17, 17, 30)

    add_card(s17, 0.8, 1.5, 5.6, 5.2, "Load Balancers: ALB vs NLB", [
        "Application Load Balancer (ALB) — Layer 7 (HTTP/HTTPS):",
        "• Intelligent routing: Routes traffic based on URL path (/api vs /images) or hostname.",
        "• SSL/TLS termination: Offloads encryption certificate handling from backend EC2s.",
        "• Target Groups: Distributes traffic across EC2s, ECS containers, and Lambda.",
        "",
        "Network Load Balancer (NLB) — Layer 4 (TCP/UDP/TLS):",
        "• Ultra-high performance: Millions of requests/second with ultra-low latency.",
        "• Provides static IP addresses per AZ.",
        "• Best for gaming servers, financial trading, and raw TCP streams."
    ])

    add_card(s17, 6.8, 1.5, 5.7, 5.2, "Amazon CloudFront (Global CDN)", [
        "Global network of 600+ Edge Locations closer to end users.",
        "Caches static files (images, video, JS/CSS, HTML) from S3 origin.",
        "Accelerates dynamic API requests via optimized AWS private backbone.",
        "Time To Live (TTL): Defines how long edge servers cache objects before re-fetching from origin.",
        "Cache Invalidation: Clear outdated files immediately (e.g., /* or /app.js).",
        "Forces HTTPS and integrates with ACM free SSL certificates."
    ])

    # =================================================================
    # SLIDE 18: AWS WAF & AWS Shield Perimeter Protection
    # =================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Perimeter Security: AWS WAF & AWS Shield Defense", "DAY 2")
    add_footer(s18, 18, 30)

    add_card(s18, 0.8, 1.5, 5.6, 5.2, "AWS WAF (Web Application Firewall)", [
        "Level: Operates at Layer 7 (HTTP/HTTPS) inspection.",
        "Attachment: Attaches to ALB, Amazon API Gateway, AWS AppSync, and CloudFront.",
        "Protection Capabilities:",
        "• SQL Injection (SQLi) protection.",
        "• Cross-Site Scripting (XSS) attack blocks.",
        "• Bad bot control and web scrapers.",
        "• Rate-based Rules: Automatically blocks any IP sending > 100 requests in 5 minutes (prevents brute-force login attacks!)."
    ])

    add_card(s18, 6.8, 1.5, 5.7, 5.2, "AWS Shield (DDoS Protection)", [
        "Level: Operates at Layer 3 (Network) and Layer 4 (Transport).",
        "AWS Shield Standard (Free for all customers):",
        "• Automatic mitigation of SYN floods, UDP reflection attacks, and HTTP slowloris attacks at no charge.",
        "",
        "AWS Shield Advanced (Paid enterprise tier):",
        "• 24/7 direct access to AWS DDoS Response Team (DRT).",
        "• Detailed attack diagnostics and forensic reporting.",
        "• Financial 'DDoS Cost Protection' refunding spike costs on EC2/ALB during an attack."
    ])

    # =================================================================
    # SLIDE 19: Enterprise 3-Tier Production Architecture
    # =================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Enterprise 3-Tier Web Architecture: Defense in Depth", "DAY 2")
    add_footer(s19, 19, 30)

    add_card(s19, 0.8, 1.5, 3.6, 5.2, "Tier 1: Web / Edge Tier (Public)", [
        "Route 53 DNS + CloudFront + Application Load Balancer (ALB).",
        "Subnet: Public Subnets across AZ-a and AZ-b.",
        "Security Group:",
        "• Inbound: Allow Port 80/443 (HTTP/HTTPS) from 0.0.0.0/0.",
        "Function: Absorbs traffic spikes, terminates SSL, routes requests to private app servers."
    ])

    add_card(s19, 4.8, 1.5, 3.6, 5.2, "Tier 2: App / Compute Tier (Private)", [
        "Auto Scaling Group of EC2 instances running FastAPI / Node.js.",
        "Subnet: Private App Subnets across AZ-a and AZ-b.",
        "Security Group:",
        "• Inbound: Allow Port 8000 ONLY from ALB Security Group!",
        "Function: Executes business logic; completely shielded from the internet."
    ])

    add_card(s19, 8.8, 1.5, 3.7, 5.2, "Tier 3: Database Tier (Isolated)", [
        "Amazon RDS Multi-AZ / Aurora + ElastiCache Redis cluster.",
        "Subnet: Isolated Private DB Subnets.",
        "Security Group:",
        "• Inbound: Allow Port 5432 ONLY from App Tier Security Group!",
        "Function: High availability, automated daily snapshots, zero public route."
    ])

    # =================================================================
    # SLIDE 20: Containers 101: Docker Fundamentals
    # =================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Containers 101: Virtual Machines vs Docker Containers", "DAY 3")
    add_footer(s20, 20, 30)

    add_card(s20, 0.8, 1.5, 5.6, 5.2, "What is a Container?", [
        "A standardized, lightweight unit of software that packages up code and all its dependencies so the application runs quickly and reliably across different computing environments.",
        "Virtual Machine (EC2) vs Container (Docker):",
        "• Virtual Machine: Packages entire Guest OS + Virtual Hardware + App. Heavy (GBs), takes minutes to boot.",
        "• Docker Container: Shares the Host OS Kernel! Packages only application + user libraries. Extremely light (MBs), starts in under 2 seconds!",
        "The Docker Trinity:",
        "1. Dockerfile: Text recipe file describing how to build your image.",
        "2. Docker Image: The compiled read-only blueprint (like a golden AMI).",
        "3. Docker Container: The live running instance of an image."
    ])

    add_code_card(s20, 6.6, 1.5, 5.9, 5.2, "Sample Production Dockerfile", [
        "# 1. Base official Python slim runtime",
        "FROM python:3.11-slim",
        "",
        "# 2. Set container working directory",
        "WORKDIR /app",
        "",
        "# 3. Copy dependencies and install",
        "COPY requirements.txt .",
        "RUN pip install --no-cache-dir -r requirements.txt",
        "",
        "# 4. Copy application source code",
        "COPY . .",
        "",
        "# 5. Expose application port & run command",
        "EXPOSE 8000",
        "CMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
    ])

    # =================================================================
    # SLIDE 21: Amazon ECR: Build, Authenticate & Push via AWS CLI (FIXED CODE)
    # =================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Amazon ECR: Pushing Docker Images via AWS CLI", "DAY 3")
    add_footer(s21, 21, 30)

    add_card(s21, 0.8, 1.5, 5.4, 5.2, "What is Amazon ECR?", [
        "Amazon Elastic Container Registry (ECR):",
        "• Fully managed, secure, high-performance Docker container registry in AWS.",
        "• Integrates with AWS IAM for granular team permissions.",
        "• Scans images automatically for Common Vulnerabilities and Exposures (CVEs).",
        "• Private repository URL format:",
        "  <account_id>.dkr.ecr.<region>.amazonaws.com/<repo-name>",
        "",
        "The 4-Step Push Workflow:",
        "1. Authenticate Docker client to AWS ECR.",
        "2. Build Docker container image locally.",
        "3. Tag image with AWS ECR repository URI.",
        "4. Push image to Amazon ECR."
    ])

    add_code_card(s21, 6.6, 1.5, 5.9, 5.2, "Step-by-Step AWS CLI Terminal Commands", [
        "# Step 1: Authenticate Docker to AWS ECR",
        "aws ecr get-login-password --region ap-south-1 | \\",
        "  docker login --username AWS --password-stdin \\",
        "  123456789012.dkr.ecr.ap-south-1.amazonaws.com",
        "",
        "# Step 2: Build local Docker image",
        "docker build -t task-cloud-app:latest .",
        "",
        "# Step 3: Tag image with full ECR repository URI",
        "docker tag task-cloud-app:latest \\",
        "  123456789012.dkr.ecr.ap-south-1.amazonaws.com/task-cloud-app:latest",
        "",
        "# Step 4: Push image to Amazon ECR",
        "docker push \\",
        "  123456789012.dkr.ecr.ap-south-1.amazonaws.com/task-cloud-app:latest"
    ])

    # =================================================================
    # SLIDE 22: Amazon ECS: EC2 Launch Type vs AWS Fargate
    # =================================================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "Amazon ECS: EC2 Launch Type vs AWS Fargate Serverless", "DAY 3")
    add_footer(s22, 22, 30)

    add_card(s22, 0.8, 1.5, 5.6, 5.2, "Option A: EC2 Launch Type", [
        "Architecture: You manage the underlying EC2 cluster VMs that run Docker.",
        "Responsibilities:",
        "• You must patch the operating systems, update Docker agent, and scale EC2 capacity.",
        "When to Choose:",
        "• When you need deep hardware customization (e.g. specialized GPUs or custom kernel modules).",
        "• When leveraging existing EC2 Reserved Instances or Spot fleets for maximum cost savings.",
        "• Large existing container clusters running 24/7 at high baseline utilization."
    ], card_bg=RGBColor(0xEA, 0xF2, 0xF8))

    add_card(s22, 6.8, 1.5, 5.7, 5.2, "Option B: AWS Fargate (Serverless)", [
        "Architecture: ZERO server management! AWS manages the underlying infrastructure.",
        "Responsibilities:",
        "• You simply specify required CPU and Memory per Task (e.g. 0.5 vCPU, 1 GB RAM).",
        "• AWS provisions, patches, and scales compute seamlessly behind the scenes.",
        "When to Choose:",
        "• Recommended default for modern cloud applications!",
        "• Teams that want to focus 100% on application code without OS maintenance.",
        "• Pay strictly for the exact seconds your container tasks run."
    ], card_bg=RGBColor(0xEA, 0xFA, 0xEA))

    # =================================================================
    # SLIDE 23: ECS Containers vs AWS Lambda Container Images
    # =================================================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "Architecture Showdown: Amazon ECS vs AWS Lambda Containers", "DAY 3")
    add_footer(s23, 23, 30)

    add_card(s23, 0.8, 1.5, 5.6, 5.2, "Amazon ECS (Fargate / EC2)", [
        "Execution Duration: Indefinite / Unlimited (Can run continuously 24 hours/day, 365 days/year).",
        "Model: Long-running services, background worker daemons, and persistent web APIs.",
        "Container Size: Large images up to dozens of GBs.",
        "Networking: Persistent Elastic Network Interface (ENI) with dedicated private IP.",
        "Cost Model: Billed per second for allocated vCPU and RAM as long as the task is running.",
        "Best for: Web application servers, continuous background queues, streaming APIs."
    ])

    add_card(s23, 6.8, 1.5, 5.7, 5.2, "AWS Lambda Container Images", [
        "Execution Duration: Strict 15-Minute Maximum Timeout!",
        "Model: Event-Driven Serverless (Triggered by S3 upload, API Gateway HTTP, DynamoDB stream).",
        "Container Size: Maximum 10 GB container image packaged with Lambda Runtime Interface Client.",
        "Scale-to-Zero: When no requests arrive, ZERO servers are running and cost is exactly $0.00!",
        "Cost Model: Billed strictly per millisecond of actual execution time.",
        "Best for: Image resizing on S3 upload, webhook handlers, sporadic cron jobs, ETL transforms."
    ])

    # =================================================================
    # SLIDE 24: Infrastructure as Code (IaC) with AWS CloudFormation
    # =================================================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "Infrastructure as Code: Why CloudFormation Beats Console Clicking", "DAY 3")
    add_footer(s24, 24, 30)

    add_card(s24, 0.8, 1.5, 5.6, 5.2, "Why IaC? (No More ClickOps)", [
        "The Problem with Manual AWS Console Clicking ('ClickOps'):",
        "• Error-prone: Forgetting to open Port 80 in Security Group causes mystery outages.",
        "• Not reproducible: Re-creating infrastructure in another region takes days of clicking.",
        "• No version control: Impossible to see who changed a setting or when.",
        "",
        "The Solution: AWS CloudFormation",
        "• Model your entire cloud infrastructure in a declarative JSON or YAML text file.",
        "• Stored in Git: Peer-reviewed via Pull Requests just like application code!",
        "• Spin up a complete production environment in 5 minutes with a single command."
    ])

    add_card(s24, 6.8, 1.5, 5.7, 5.2, "Core CloudFormation Concepts", [
        "1. Template: The declarative YAML or JSON blueprint defining desired resources.",
        "2. Stack: The instantiated collection of AWS resources managed as a single unit.",
        "• Creating a stack provisions all resources.",
        "• Deleting a stack deletes ALL associated resources cleanly (prevents orphan costs!).",
        "3. Change Sets: A preview of changes CloudFormation will make before executing an update (prevents accidental database deletions!).",
        "4. Rollback: If any resource fails during creation, CloudFormation automatically rolls back and cleans up."
    ])

    # =================================================================
    # SLIDE 25: CloudFormation Template Anatomy (YAML) (FIXED CODE)
    # =================================================================
    s25 = prs.slides.add_slide(blank_layout)
    add_header(s25, "CloudFormation Anatomy: Parameters, Resources & Outputs", "DAY 3")
    add_footer(s25, 25, 30)

    add_card(s25, 0.8, 1.5, 5.4, 5.2, "The 3 Core Template Sections", [
        "1. Parameters: Dynamic inputs passed at launch time (e.g. InstanceType, KeyName) so one template works for Dev, Test, and Prod.",
        "2. Resources (MANDATORY): The AWS services to provision (EC2, S3, VPC).",
        "• Must specify Type (e.g. AWS::EC2::Instance) and Properties.",
        "3. Outputs: Values returned after stack creation (e.g. Web URL, Public IP) for other stacks to import via Fn::ImportValue.",
        "Intrinsic Functions:",
        "• Ref: Returns parameter value or resource ID.",
        "• Fn::GetAtt: Fetches attribute (e.g. PublicIp).",
        "• Fn::Sub: Interpolates string variables."
    ])

    add_code_card(s25, 6.6, 1.5, 5.9, 5.2, "Sample Production CloudFormation Template", [
        "AWSTemplateFormatVersion: '2010-09-09'",
        "Description: TASK Telangana EC2 Web Server Stack",
        "",
        "Parameters:",
        "  InstanceType:",
        "    Type: String",
        "    Default: t3.micro",
        "",
        "Resources:",
        "  TaskWebServer:",
        "    Type: AWS::EC2::Instance",
        "    Properties:",
        "      InstanceType: !Ref InstanceType",
        "      ImageId: ami-03f4878e83fed34a0 # Amazon Linux 2023",
        "      Tags:",
        "        - Key: Name",
        "          Value: task-cfn-webserver",
        "",
        "Outputs:",
        "  WebServerPublicIP:",
        "    Description: Public IP of Web Server",
        "    Value: !GetAtt TaskWebServer.PublicIp"
    ])

    # =================================================================
    # SLIDE 26: CloudFormation Drift Detection
    # =================================================================
    s26 = prs.slides.add_slide(blank_layout)
    add_header(s26, "CloudFormation Drift Detection: Catching Manual Out-of-Band Edits", "DAY 3")
    add_footer(s26, 26, 30)

    add_card(s26, 0.8, 1.5, 5.6, 5.2, "What is Infrastructure Drift?", [
        "Definition: Drift occurs when a human engineer logs into the AWS Console and manually alters a resource (e.g., changes an EC2 instance type from t3.micro to m5.large, or opens Port 22 in a Security Group) without updating the CloudFormation template!",
        "Why is Drift Dangerous?",
        "• Template is no longer the single source of truth.",
        "• Next stack update might accidentally overwrite or conflict with manual changes.",
        "• Security compliance is violated without audit trail."
    ])

    add_card(s26, 6.8, 1.5, 5.7, 5.2, "How CloudFormation Drift Detection Works", [
        "1. Run Drift Detection: In AWS Console, select Stack ➔ Stack actions ➔ Detect drift (or run `aws cloudformation detect-stack-drift`).",
        "2. AWS compares current actual live resource properties against expected template properties.",
        "3. Drift Status Results:",
        "• IN_SYNC: Real-world infrastructure matches template 100%.",
        "• DRIFTED: One or more properties have been modified out-of-band.",
        "4. Remediation Options:",
        "• Option A: Revert manual changes in AWS Console to match template.",
        "• Option B: Update template to reflect new configuration and run CloudFormation update with Change Set."
    ])

    # =================================================================
    # SLIDE 27: 3-Day Hands-on Lab Action Plan
    # =================================================================
    s27 = prs.slides.add_slide(blank_layout)
    add_header(s27, "Classroom Practice: 3-Day Hands-on Lab Master Plan", "LABS")
    add_footer(s27, 27, 30)

    add_card(s27, 0.8, 1.5, 3.6, 5.2, "Day 1 Practical Labs", [
        "Lab 1: Launch EC2 with User Data web server script.",
        "Lab 2: Test SSH connection with .pem keypair.",
        "Lab 3: Bake Custom AMI task-golden-v1.",
        "Lab 4: Create 5GB gp3 EBS volume, attach & format.",
        "Lab 5: Create S3 bucket & attach HTTPS-only policy."
    ], card_bg=RGBColor(0xEA, 0xF2, 0xF8))

    add_card(s27, 4.8, 1.5, 3.6, 5.2, "Day 2 Practical Labs", [
        "Lab 6: Build Custom VPC 10.0.0.0/16 from scratch.",
        "Lab 7: Carve Public (10.0.1.0/24) & Private (10.0.2.0/24) subnets.",
        "Lab 8: Attach Internet Gateway & configure Route Table.",
        "Lab 9: Security Group stateful test vs NACL stateless drop.",
        "Lab 10: Provision RDS database inside private DB subnet."
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    add_card(s27, 8.8, 1.5, 3.7, 5.2, "Day 3 Practical Labs", [
        "Lab 11: Write Dockerfile and build container image.",
        "Lab 12: Authenticate AWS CLI & push image to Amazon ECR.",
        "Lab 13: Deploy ECS Fargate task running your container.",
        "Lab 14: Deploy EC2 web server using CloudFormation template.",
        "Lab 15: Perform Stack Drift Detection and remediate drift."
    ], card_bg=RGBColor(0xEA, 0xFA, 0xEA))

    # =================================================================
    # SLIDE 28: Summary & Final Student Certification Checklist
    # =================================================================
    s28 = prs.slides.add_slide(blank_layout)
    add_header(s28, "Module 03 Graduation: Certification & Core Takeaways", "SUMMARY")
    add_footer(s28, 28, 30)

    add_card(s28, 0.8, 1.5, 5.6, 5.2, "Core Architectures to Remember", [
        "1. The Vehicle Metaphor:",
        "   EC2 = Engine | EBS = Personal Trunk | EFS = Fleet Cargo | S3 = Global Depot | VPC = Gated Highway",
        "2. Multi-AZ is about HIGH AVAILABILITY with automatic failover.",
        "3. Security Groups are STATEFUL; Network ACLs are STATELESS.",
        "4. Route Table decides if a subnet is Public (0.0.0.0/0 -> IGW) or Private.",
        "5. ECS is for long-running services; Lambda has a 15-minute execution limit.",
        "6. CloudFormation Drift Detection catches dangerous un-tracked console edits."
    ], card_bg=RGBColor(0xEA, 0xF2, 0xF8))

    add_card(s28, 6.8, 1.5, 5.7, 5.2, "Zero-Dollar Student Sunset Rule", [
        "Every student must verify these 4 steps before leaving the lab:",
        "1. STOP or TERMINATE all test EC2 instances.",
        "2. DELETE unattached EBS volumes in 'available' status.",
        "3. DELETE custom CloudFormation stacks when practical is finished.",
        "4. RELEASE any allocated Elastic IPs (EIPs).",
        "",
        "Keep your AWS account at $0.00 balance!",
        "Trainer: Sundeep Hiremat | Nalgonda Center"
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    prs.save(output_path)
    print(f"Successfully generated expanded 28-slide Masterclass presentation at: {output_path}")

if __name__ == "__main__":
    out_file = r"F:\Task( Telangana )\Nalgonda\Projects\task\module_03_aws_core\presentation\Module_03_AWS_Core_Services_Masterclass_v2.pptx"
    create_deck(out_file)
