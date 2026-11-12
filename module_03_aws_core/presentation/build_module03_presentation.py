"""
Script to generate the Module 03 AWS Core Services Masterclass Presentation.
Includes the Vehicle Analogy, EC2, EBS, EFS, S3, and VPC Networking.
"""

import sys
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
    ACCENT_BLUE = RGBColor(0x00, 0x73, 0xBB)   # #0073BB
    ACCENT_GREEN = RGBColor(0x1D, 0x81, 0x02)  # #1D8102

    def add_header(slide, title_text, category_text="TASK TELANGANA · CLOUD SOFTWARE DEVELOPER · MODULE 03"):
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
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = AWS_ORANGE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE

    def add_footer(slide, current_page=None, total_pages=20):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_top = Inches(0)
        p = tf.paragraphs[0]
        p.text = "Trainer: Sundeep Hiremath  |  Nalgonda Training Center  |  AWS Core Compute, Storage & Networking"
        p.font.size = Pt(10)
        p.font.color.rgb = MUTED_TEXT

        if current_page:
            p2 = tf.add_paragraph()
            p2.text = f"{current_page} / {total_pages}"
            p2.alignment = PP_ALIGN.RIGHT
            p2.font.size = Pt(10)
            p2.font.color.rgb = MUTED_TEXT

    def add_card(slide, left, top, width, height, title, items, card_bg=CARD_BG, border_color=CARD_BORDER, title_color=AWS_NAVY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = card_bg
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        tx = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.18), Inches(width - 0.4), Inches(height - 0.36))
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
            p.text = f"• {item}"
            p.font.size = Pt(12)
            p.font.color.rgb = DARK_TEXT
            p.space_before = Pt(4)

    # -----------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -----------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = AWS_SQUID
    bg.line.fill.background()

    # Orange accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.18), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = AWS_ORANGE
    bar.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "TASK TELANGANA · CLOUD SOFTWARE DEVELOPER"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = AWS_ORANGE

    p2 = tf.add_paragraph()
    p2.text = "Module 03: AWS Core Services Masterclass"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "EC2 Compute, Block (EBS), File (EFS), Object (S3) & VPC Networking\nDemystified Through The Grand Vehicle Metaphor"
    p3.font.size = Pt(18)
    p3.font.color.rgb = RGBColor(0xD1, 0xD5, 0xDB)
    p3.space_before = Pt(12)

    p4 = tf.add_paragraph()
    p4.text = "Trainer: Sundeep Hiremath  |  Nalgonda Training Center  |  AWS DVA-C02 Alignment"
    p4.font.size = Pt(13)
    p4.font.color.rgb = AWS_ORANGE
    p4.space_before = Pt(24)

    # -----------------------------------------------------------------
    # SLIDE 2: Learning Outcomes (From User Images)
    # -----------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Module 03 Learning Objectives & Roadmap")
    add_footer(s2, 2)

    add_card(s2, 0.8, 1.5, 3.6, 5.2, "1. Core Compute (EC2)", [
        "Launch, stop, start, terminate EC2 instances.",
        "Anatomy: AMI, Instance Type, Key Pair, Security Group, and Root EBS.",
        "Inject startup automation with User Data scripts.",
        "Bake Custom AMIs (Golden Images) from configured servers.",
        "Container preview: ECR repository & ECS Fargate serverless tasks."
    ])

    add_card(s2, 4.8, 1.5, 3.6, 5.2, "2. Storage Triad (EBS, EFS, S3)", [
        "Block vs File vs Object storage shootout.",
        "EBS: Attach, format, resize, and snapshot personal volumes.",
        "EFS: Multi-AZ elastic file share mounted by 100+ servers concurrently.",
        "S3: Buckets, objects, 11 9's durability.",
        "S3 Security: Block Public Access & HTTPS Bucket Policies."
    ])

    add_card(s2, 8.8, 1.5, 3.7, 5.2, "3. VPC Networking & Defense", [
        "VPC isolation: CIDR blocks & subnets.",
        "Public vs Private subnets (Route Table logic).",
        "Internet Gateway (IGW) vs NAT Gateway.",
        "Security Groups (Stateful) vs NACLs (Stateless).",
        "Classic 3-tier architecture: ALB > EC2 > RDS."
    ])

    # -----------------------------------------------------------------
    # SLIDE 3: The Grand Vehicle Metaphor
    # -----------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Grand Vehicle Metaphor: Cloud Infrastructure Explained")
    add_footer(s3, 3)

    add_card(s3, 0.8, 1.5, 2.7, 5.2, "EC2 = The Rental Car", [
        "You rent a car on-demand instead of buying a vehicle factory.",
        "AMI = Car Blueprint / Model (Sedan vs Truck = Ubuntu vs Linux).",
        "Instance Type = Engine Horsepower (t2.micro = 1 cylinder eco-car).",
        "Key Pair = Physical Ignition Key.",
        "User Data = Pre-ignition checklist (fuel additive, GPS)."
    ], card_bg=RGBColor(0xEA, 0xF2, 0xF8))

    add_card(s3, 3.8, 1.5, 2.7, 5.2, "EBS = The Car Trunk", [
        "Hard drive bolted directly to the vehicle chassis.",
        "Ultra-fast local block storage for OS and running apps.",
        "When car stops, luggage inside trunk stays intact.",
        "Snapshot = Taking a photo/copy of luggage to store in central locker."
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    add_card(s3, 6.8, 1.5, 2.7, 5.2, "EFS = Shared Cargo Rack", [
        "A shared roof rack that a whole fleet of cars can access together.",
        "100+ cars (EC2s) in different parking garages (AZs) read/write concurrently.",
        "Standard NFS protocol: everyone sees real-time file updates."
    ], card_bg=RGBColor(0xEA, 0xFA, 0xEA))

    add_card(s3, 9.8, 1.5, 2.7, 5.2, "S3 = Global Warehouse", [
        "World-scale container depot, not bolted inside the car.",
        "Store unlimited boxes (Objects) in huge shipping bays (Buckets).",
        "Accessible from anywhere via highway web URL (HTTPS).",
        "99.999999999% (11 9's) durability: virtually indestructible!"
    ], card_bg=RGBColor(0xFD, 0xED, 0xEC))

    # -----------------------------------------------------------------
    # SLIDE 4: EC2 Anatomy & Components
    # -----------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Anatomy of an EC2 Instance: The 5 Essential Pillars")
    add_footer(s4, 4)

    add_card(s4, 0.8, 1.5, 5.6, 2.5, "1. AMI (Amazon Machine Image) — The Chassis", [
        "Pre-packaged template with OS, initial software, and base configurations.",
        "Options: Amazon Linux 2023, Ubuntu 22.04/24.04, Windows Server, Red Hat.",
        "Custom AMIs: You can install tools, configure apps, and snapshot your own custom AMI!"
    ])

    add_card(s4, 6.8, 1.5, 5.7, 2.5, "2. Instance Type — The Engine Size", [
        "Naming syntax: <Family><Generation>.<Size> (e.g., t3.micro, c5.xlarge).",
        "General Purpose (t3, m5) — Balanced compute, memory, and networking.",
        "Compute Optimized (c5, c6g) — High CPU for compute-intensive tasks.",
        "Memory Optimized (r5, r6g) — Heavy RAM for in-memory DBs and caching."
    ])

    add_card(s4, 0.8, 4.3, 5.6, 2.5, "3. Key Pair (.pem / .ppk) — The Ignition Key", [
        "Asymmetric cryptography: AWS holds Public Key; You download Private Key.",
        "AWS NEVER saves a copy of your private key — if lost, SSH access is gone!",
        ".pem format for OpenSSH (Linux/Mac/PowerShell), .ppk for PuTTY on Windows."
    ])

    add_card(s4, 6.8, 4.3, 5.7, 2.5, "4. Security Group & 5. Storage (EBS Root)", [
        "Security Group: Virtual firewall controlling inbound & outbound network traffic.",
        "Default Inbound: Everything blocked! You must explicitly allow SSH (22) or HTTP (80).",
        "Root EBS Volume: The primary operating system disk (typically 8 GB – 30 GB gp3)."
    ])

    # -----------------------------------------------------------------
    # SLIDE 5: EC2 Lifecycle & Billing State Machine
    # -----------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "EC2 Lifecycle & Billing: The State Transition Machine")
    add_footer(s5, 5)

    add_card(s5, 0.8, 1.5, 3.6, 5.2, "States & Transitions", [
        "1. Pending: Instance is provisioning on underlying physical hardware.",
        "2. Running: OS is booted; compute & storage billing is active.",
        "3. Stopping: OS graceful shutdown.",
        "4. Stopped: Engine turned off. Compute charge stops! Only EBS storage billed.",
        "5. Shutting-Down: Initiating permanent teardown.",
        "6. Terminated: Permanently deleted. Root EBS volume released."
    ])

    add_card(s5, 4.8, 1.5, 3.6, 5.2, "Vehicle Analogy: Parking vs Scrapping", [
        "Stop = Turning off car engine and parking in garage.",
        "• Compute meter stops ticking ($0/hr for CPU/RAM).",
        "• You only pay small garage rent for the parked car's trunk (EBS).",
        "• Public IP address changes when restarted (unless using Elastic IP)!",
        "Terminate = Sending the car to the junkyard scrap crusher.",
        "• Disk destroyed, instance permanently deleted, all billing ceases."
    ])

    add_card(s5, 8.8, 1.5, 3.7, 5.2, "Golden Cost Savings Rules for Students", [
        "Always STOP instances at the end of every classroom lab!",
        "Always TERMINATE throwaway test instances when practice is done.",
        "Verify your region is set to ap-south-1 (Mumbai) or us-east-1 consistently.",
        "Keep root volume size within AWS Free Tier limits (up to 30 GB EBS free/month).",
        "Check AWS Cost Explorer weekly to ensure $0 balance."
    ])

    # -----------------------------------------------------------------
    # SLIDE 6: Bootstrapping with User Data
    # -----------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "EC2 Automation: Bootstrapping with User Data")
    add_footer(s6, 6)

    add_card(s6, 0.8, 1.5, 5.6, 5.2, "What is User Data?", [
        "A startup shell script that executes automatically on first boot as root.",
        "Eliminates manual SSH login to install packages or start web servers.",
        "Vehicle Analogy: The pre-delivery checklist that automatically fuels the car, tunes the radio, and turns on the AC before you touch the wheel.",
        "Runs only ONCE when the instance boots for the first time.",
        "Log files saved at: /var/log/cloud-init-output.log for debugging."
    ])

    add_card(s6, 6.8, 1.5, 5.7, 5.2, "Sample Production Bootstrap Script", [
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
        "# 4. Write dynamic web page with metadata",
        "INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)",
        "echo '<h1>Welcome to TASK Cloud Lab - Instance: '$INSTANCE_ID'</h1>' > /var/www/html/index.html"
    ], card_bg=RGBColor(0x1E, 0x29, 0x3B), title_color=AWS_ORANGE)

    # -----------------------------------------------------------------
    # SLIDE 7: How to Connect: SSH, Putty & EC2 Instance Connect
    # -----------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Connecting to Your EC2 Instance: 3 Methods")
    add_footer(s7, 7)

    add_card(s7, 0.8, 1.5, 3.6, 5.2, "Method 1: EC2 Instance Connect (Easiest)", [
        "Browser-based terminal inside AWS Management Console.",
        "No software installation required on student laptops.",
        "Uses temporary 60-second SSH keys pushed via AWS API.",
        "Requirements: Instance must have a Public IP and Security Group Port 22 open.",
        "Best for beginners and campus lab machines with restricted software permissions!"
    ])

    add_card(s7, 4.8, 1.5, 3.6, 5.2, "Method 2: Native SSH (PowerShell / Mac / Linux)", [
        "1. Locate your downloaded key: my-key.pem",
        "2. Fix file permissions (Linux/Mac):",
        "   chmod 400 my-key.pem",
        "3. Connect using standard command:",
        "   ssh -i my-key.pem ec2-user@<PUBLIC-IP>",
        "",
        "Default usernames:",
        "• Amazon Linux: ec2-user",
        "• Ubuntu: ubuntu",
        "• Red Hat: ec2-user or root"
    ])

    add_card(s7, 8.8, 1.5, 3.7, 5.2, "Method 3: PuTTY on Windows", [
        "For older Windows machines without native SSH client:",
        "1. Convert .pem to .ppk using PuTTYgen.",
        "   (Load .pem -> Save private key as .ppk)",
        "2. Open PuTTY.",
        "3. Host Name: ec2-user@<PUBLIC-IP>",
        "4. Connection -> SSH -> Auth -> Credentials -> Browse .ppk file.",
        "5. Click Open to launch terminal session."
    ])

    # -----------------------------------------------------------------
    # SLIDE 8: Custom AMIs & Golden Images
    # -----------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Custom AMIs: Baking Golden Images for Scalability")
    add_footer(s8, 8)

    add_card(s8, 0.8, 1.5, 5.6, 5.2, "Why Create a Custom AMI?", [
        "Problem: Installing Python, libraries, and web apps on every new EC2 instance takes 10–15 minutes each time.",
        "Solution: Bake a Golden Image! Configure one instance perfectly, then snapshot it into an AMI.",
        "Vehicle Analogy: Modifying a base car into an emergency ambulance with sirens, medical gear, and stretchers. Then using that ambulance blueprint to manufacture 50 identical ambulances in minutes!",
        "Key Benefits:",
        "• Near-instant boot time for Auto Scaling fleets.",
        "• Consistency: Every server runs identical software versions.",
        "• Disaster recovery: Re-launch full application in another AZ in minutes."
    ])

    add_card(s8, 6.8, 1.5, 5.7, 5.2, "Step-by-Step: Baking an AMI in Console", [
        "Step 1: Launch base EC2 instance (Amazon Linux 2023).",
        "Step 2: Connect via SSH and install your application stack:",
        "   sudo dnf install -y python3-pip git nginx",
        "   git clone https://github.com/cloude-user/task.git",
        "Step 3: Test that application runs smoothly.",
        "Step 4: In AWS Console: Select Instance -> Actions -> Image and templates -> Create image.",
        "Step 5: Name image: task-golden-ami-v1.",
        "Step 6: Click Create Image (AWS stops instance temporarily to take clean disk snapshot).",
        "Step 7: Launch 10 new instances using task-golden-ami-v1 instantly!"
    ])

    # -----------------------------------------------------------------
    # SLIDE 9: Storage Triad Shootout (Block vs File vs Object)
    # -----------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Storage Shootout: Block (EBS) vs File (EFS) vs Object (S3)")
    add_footer(s9, 9)

    add_card(s9, 0.8, 1.5, 3.6, 5.2, "Amazon EBS (Block)", [
        "Analogy: Built-in Car Trunk",
        "Scope: Bound to a SINGLE Availability Zone (AZ).",
        "Attachment: Mounted to 1 EC2 instance at a time (like a physical USB drive).",
        "Protocol: Block-level (formatted with ext4, xfs, NTFS).",
        "Speed: Ultra-low millisecond latency; high IOPS.",
        "Best for: Operating system boot disks, databases (PostgreSQL, MySQL, SQL Server)."
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    add_card(s9, 4.8, 1.5, 3.6, 5.2, "Amazon EFS (File)", [
        "Analogy: Shared Fleet Roof Cargo",
        "Scope: Regional (Multi-AZ automatically).",
        "Attachment: Mounted by HUNDREDS of EC2 instances concurrently across AZs.",
        "Protocol: Network File System (NFSv4). Standard folder hierarchy.",
        "Scalability: Grows and shrinks automatically (pay only for GBs stored).",
        "Best for: Shared web content, WordPress uploads, data analytics clusters, shared home directories."
    ], card_bg=RGBColor(0xEA, 0xFA, 0xEA))

    add_card(s9, 8.8, 1.5, 3.7, 5.2, "Amazon S3 (Object)", [
        "Analogy: Global Shipping Depot",
        "Scope: Global web-accessible URL via HTTP/HTTPS.",
        "Attachment: NOT mounted as a disk drive; accessed via REST API / SDK / CLI.",
        "Structure: Flat namespace (Buckets & Objects with metadata and tags).",
        "Durability: 99.999999999% (11 9's) across 3+ AZs.",
        "Best for: Static website hosting, media files, datasets, backups, disaster recovery."
    ], card_bg=RGBColor(0xFD, 0xED, 0xEC))

    # -----------------------------------------------------------------
    # SLIDE 10: Amazon EBS In-Depth
    # -----------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Amazon EBS Deep Dive: Types, Volumes & Snapshots")
    add_footer(s10, 10)

    add_card(s10, 0.8, 1.5, 5.6, 5.2, "Volume Types: Choosing the Right Trunk", [
        "General Purpose SSD (gp3 — Recommended Default):",
        "• Baseline 3,000 IOPS and 125 MB/s throughput included free.",
        "• Independent scaling of storage size and performance without paying for extra disk.",
        "Provisioned IOPS SSD (io2 Block Express):",
        "• Extreme performance for critical mission databases (up to 256,000 IOPS).",
        "• 99.999% durability (5 9's).",
        "Throughput Optimized HDD (st1) & Cold HDD (sc1):",
        "• Magnetic spinning disks for sequential big data & long-term log archives."
    ])

    add_card(s10, 6.8, 1.5, 5.7, 5.2, "EBS Snapshots & Life Cycle", [
        "Snapshots are point-in-time incremental backups of EBS volumes stored in Amazon S3.",
        "Incremental = Only blocks that changed since last snapshot are billed!",
        "Snapshot Cross-AZ / Cross-Region Migration:",
        "1. Take snapshot of EBS volume in ap-south-1a.",
        "2. Create new EBS volume from snapshot in ap-south-1b.",
        "3. Attach to EC2 in ap-south-1b.",
        "Fast Snapshot Restore (FSR): Instantly hydrates blocks with zero latency on first read."
    ])

    # -----------------------------------------------------------------
    # SLIDE 11: Amazon S3 Security & Policies
    # -----------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Amazon S3 Security: Buckets, Policies & Encryption")
    add_footer(s11, 11)

    add_card(s11, 0.8, 1.5, 5.6, 5.2, "S3 Core Security Controls", [
        "1. Bucket Naming Rules:",
        "• Globally unique across all AWS accounts in the world!",
        "• 3–63 characters, lowercase letters, numbers, and hyphens only.",
        "2. Block Public Access (BPA):",
        "• Enabled by DEFAULT on every new bucket since April 2023.",
        "• Prevents accidental leaks of confidential student files or company data.",
        "3. Default Encryption:",
        "• All new objects are automatically encrypted server-side using SSE-S3 (AES-256).",
        "4. Bucket Policies:",
        "• JSON resource-based policy attached directly to the bucket."
    ])

    add_card(s11, 6.8, 1.5, 5.7, 5.2, "Sample Policy: Enforcing HTTPS/TLS Only", [
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
    ], card_bg=RGBColor(0x1E, 0x29, 0x3B), title_color=AWS_ORANGE)

    # -----------------------------------------------------------------
    # SLIDE 12: VPC Networking: The Private Highway
    # -----------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Amazon VPC: Your Isolated Private Highway System")
    add_footer(s12, 12)

    add_card(s12, 0.8, 1.5, 5.6, 5.2, "What is a VPC?", [
        "A logically isolated section of the AWS Cloud where you launch AWS resources in a virtual network you define.",
        "Vehicle Analogy: Your private gated business park / private racing circuit.",
        "CIDR Block (Classless Inter-Domain Routing):",
        "• Determines the IP address range for your entire private cloud.",
        "• Standard Production Range: 10.0.0.0/16 (Yields 65,536 private IP addresses).",
        "• AWS reserves 5 IP addresses in every subnet (.0 network, .1 router, .2 DNS, .3 reserved, .255 broadcast)."
    ])

    add_card(s12, 6.8, 1.5, 5.7, 5.2, "The Core Networking Building Blocks", [
        "1. Subnets: Slices of the VPC assigned to specific Availability Zones.",
        "2. Internet Gateway (IGW): The 2-way front gate connecting VPC to public Internet.",
        "3. Route Tables: Road signs telling network packets where to travel next.",
        "4. NAT Gateway: One-way security tunnel allowing private instances to fetch internet updates without accepting incoming connections.",
        "5. Elastic IP (EIP): Static public IPv4 address that never changes when instance restarts."
    ])

    # -----------------------------------------------------------------
    # SLIDE 13: Public vs Private Subnets
    # -----------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Public vs Private Subnets: The Route Table Decides!")
    add_footer(s13, 13)

    add_card(s13, 0.8, 1.5, 5.6, 5.2, "Public Subnet (The Front Showroom)", [
        "Definition: A subnet whose Route Table contains a direct route to an Internet Gateway (IGW).",
        "Route Table Entry:",
        "• Destination: 0.0.0.0/0 (All unknown traffic)",
        "• Target: igw-xxxxxxxx (Internet Gateway)",
        "Use Cases:",
        "• Application Load Balancers (ALB) receiving user web traffic.",
        "• Public Bastion Hosts / Jump boxes.",
        "• Public-facing web servers.",
        "Every resource must possess a Public IPv4 address to communicate with Internet."
    ], card_bg=RGBColor(0xEA, 0xF2, 0xF8))

    add_card(s13, 6.8, 1.5, 5.7, 5.2, "Private Subnet (The VIP Garage / Vault)", [
        "Definition: A subnet whose Route Table DOES NOT point to an IGW.",
        "Route Table Entry (For outbound internet access only):",
        "• Destination: 0.0.0.0/0",
        "• Target: nat-xxxxxxxx (NAT Gateway residing in a Public Subnet)",
        "Use Cases:",
        "• Backend microservices & application servers.",
        "• Databases (RDS MySQL/Postgres, DynamoDB VPC endpoints).",
        "• Internal machine learning training nodes.",
        "Benefit: Completely protected from direct malicious hackers on the Internet!"
    ], card_bg=RGBColor(0xEA, 0xFA, 0xEA))

    # -----------------------------------------------------------------
    # SLIDE 14: Security Groups vs NACLs
    # -----------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Security Groups vs Network ACLs: Personal Bodyguard vs Gate Barrier")
    add_footer(s14, 14)

    add_card(s14, 0.8, 1.5, 5.6, 5.2, "Security Groups (Personal Bodyguard)", [
        "Level: Operates at the INSTANCE (ENI) level.",
        "State: STATEFUL.",
        "• If inbound traffic is allowed, outbound return traffic is automatically allowed, regardless of outbound rules!",
        "Rules:",
        "• ALLOW rules only (No explicit DENY rules).",
        "• All rules evaluated before decision.",
        "Analogy: A personal bodyguard sitting in the passenger seat who remembers who you invited inside."
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    add_card(s14, 6.8, 1.5, 5.7, 5.2, "Network ACLs - NACL (Toll Gate Barrier)", [
        "Level: Operates at the SUBNET boundary level.",
        "State: STATELESS.",
        "• Inbound and outbound traffic MUST be explicitly allowed in both directions!",
        "Rules:",
        "• Supports both ALLOW and DENY rules.",
        "• Evaluated in strict numerical order (Rule 100 before Rule 200). First match wins!",
        "Analogy: A highway toll gate barrier that checks every license plate entering and exiting the district."
    ], card_bg=RGBColor(0xFD, 0xED, 0xEC))

    # -----------------------------------------------------------------
    # SLIDE 15: 3-Tier Production Architecture (Defense in Depth)
    # -----------------------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Production 3-Tier Web Architecture: Defense in Depth")
    add_footer(s15, 15)

    add_card(s15, 0.8, 1.5, 3.6, 5.2, "Tier 1: Web / Edge Tier (Public)", [
        "Components: Route 53 DNS + CloudFront CDN + Application Load Balancer (ALB).",
        "Subnet: Public Subnets (across AZ-a and AZ-b).",
        "Security Group:",
        "• Inbound: Allow Port 80/443 (HTTP/HTTPS) from 0.0.0.0/0.",
        "Function: Terminates SSL/TLS, absorbs DDoS spikes, distributes incoming user traffic."
    ])

    add_card(s15, 4.8, 1.5, 3.6, 5.2, "Tier 2: App / Compute Tier (Private)", [
        "Components: Auto Scaling Group of EC2 instances running Python/FastAPI/Node.js.",
        "Subnet: Private App Subnets (across AZ-a and AZ-b).",
        "Security Group:",
        "• Inbound: Allow Port 8000 ONLY from the ALB's Security Group!",
        "Function: Executes business logic; cannot be reached directly by public users."
    ])

    add_card(s15, 8.8, 1.5, 3.7, 5.2, "Tier 3: Database Tier (Isolated)", [
        "Components: Amazon RDS Multi-AZ (PostgreSQL / Aurora) or DynamoDB.",
        "Subnet: Isolated Private DB Subnets.",
        "Security Group:",
        "• Inbound: Allow Port 5432 ONLY from App Tier Security Group!",
        "Function: High availability, automated daily snapshots, encrypted storage."
    ])

    # -----------------------------------------------------------------
    # SLIDE 16: Database Decision Framework (RDS vs Aurora vs DynamoDB)
    # -----------------------------------------------------------------
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Database Decision Framework: When to Choose What")
    add_footer(s16, 16)

    add_card(s16, 0.8, 1.5, 3.6, 5.2, "Amazon RDS (Standard)", [
        "Type: Relational SQL (Postgres, MySQL, MariaDB, Oracle, SQL Server).",
        "Managed Services: Automated OS patching, automated daily backups, point-in-time recovery.",
        "Multi-AZ Deployment: Synchronous standby replica in another AZ for instant disaster failover.",
        "Read Replicas: Up to 15 asynchronous read copies to offload heavy reporting read queries."
    ])

    add_card(s16, 4.8, 1.5, 3.6, 5.2, "Amazon Aurora (Cloud Native)", [
        "Compatibility: Drop-in replacement for PostgreSQL & MySQL.",
        "Architecture: Compute and storage separated into 6-way distributed replication across 3 AZs.",
        "Speed: 5x faster than MySQL, 3x faster than standard PostgreSQL.",
        "Aurora Serverless v2: Scales compute instantly from 0.5 to 128 ACUs in fractions of a second!"
    ])

    add_card(s16, 8.8, 1.5, 3.7, 5.2, "Amazon DynamoDB (NoSQL)", [
        "Type: Fully managed, serverless, ultra-fast NoSQL Key-Value & Document database.",
        "Performance: Single-digit millisecond response time at any scale.",
        "Partition Key (PK) & Sort Key (SK) design pattern.",
        "Use Cases: Shopping carts, gaming leaderboards, real-time vehicle GPS tracking, user session caches."
    ])

    # -----------------------------------------------------------------
    # SLIDE 17: Edge Delivery & WAF Security
    # -----------------------------------------------------------------
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Edge Acceleration & Perimeter Shield: CloudFront & AWS WAF")
    add_footer(s17, 17)

    add_card(s17, 0.8, 1.5, 5.6, 5.2, "Amazon CloudFront (Global CDN)", [
        "Global network of 600+ Edge Locations closer to end users.",
        "Caches static files (images, video, JS/CSS, HTML) from S3 origin.",
        "Accelerates dynamic API requests via optimized AWS private backbone.",
        "Time To Live (TTL): Defines how long edge servers cache objects before re-fetching from origin.",
        "Cache Invalidation: Clear outdated files immediately (e.g., /* or /app.js)."
    ])

    add_card(s17, 6.8, 1.5, 5.7, 5.2, "AWS WAF & AWS Shield (Perimeter Security)", [
        "AWS WAF (Web Application Firewall):",
        "• Inspects Layer 7 (HTTP/HTTPS) traffic at ALB, API Gateway, or CloudFront.",
        "• Blocks SQL Injection (SQLi), Cross-Site Scripting (XSS), and bad bots.",
        "• Rate-based Rules: Block IP addresses sending > 100 requests in 5 minutes.",
        "AWS Shield:",
        "• Shield Standard: Free, automatic Layer 3/4 DDoS protection for all AWS customers.",
        "• Shield Advanced: 24/7 DDoS Response Team (DRT) & financial cost protection."
    ])

    # -----------------------------------------------------------------
    # SLIDE 18: Containers & Serverless Preview (ECR & ECS / Fargate)
    # -----------------------------------------------------------------
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Compute Evolution: From Virtual Machines to Containers")
    add_footer(s18, 18)

    add_card(s18, 0.8, 1.5, 5.6, 5.2, "Amazon ECR & Container Packaging", [
        "Amazon ECR (Elastic Container Registry):",
        "• Highly secure, private Docker container registry in AWS.",
        "• Integrates with IAM for granular push/pull permissions.",
        "• Automated vulnerability image scanning.",
        "Development Flow:",
        "1. Build Docker image locally: docker build -t task-app .",
        "2. Authenticate to ECR: aws ecr get-login-password | docker login",
        "3. Tag & Push image: docker push <aws_account_id>.dkr.ecr.../task-app"
    ])

    add_card(s18, 6.8, 1.5, 5.7, 5.2, "ECS: EC2 Launch Type vs AWS Fargate", [
        "Amazon ECS (Elastic Container Service) Orchestration:",
        "Option A: EC2 Launch Type",
        "• You manage the underlying EC2 cluster VMs, OS updates, and scaling.",
        "• Full control over underlying hardware, instance pricing, and spot capacity.",
        "Option B: AWS Fargate (Serverless)",
        "• ZERO server management! You specify CPU and Memory per task.",
        "• AWS provisions, patches, and scales compute automatically behind the scenes.",
        "• Pay strictly for seconds of container runtime execution."
    ])

    # -----------------------------------------------------------------
    # SLIDE 19: Step-by-Step Hands-on Student Lab Checklist
    # -----------------------------------------------------------------
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Hands-on Lab Checklist: Today's Classroom Practical")
    add_footer(s19, 19)

    add_card(s19, 0.8, 1.5, 3.6, 5.2, "Lab 1: EC2 & Custom AMI", [
        "1. Launch t2.micro or t3.micro with Amazon Linux 2023.",
        "2. Add User Data script to install Python3 & Web server.",
        "3. Verify web page loads at http://<Public-IP>.",
        "4. Stop instance -> Note that public IP changes.",
        "5. Bake Custom AMI task-golden-v1.",
        "6. Launch a twin instance from task-golden-v1."
    ])

    add_card(s19, 4.8, 1.5, 3.6, 5.2, "Lab 2: S3 & Storage Security", [
        "1. Create bucket task-nalgonda-<student-name>-2026.",
        "2. Confirm Block Public Access is strictly ON.",
        "3. Upload student resume or project image.",
        "4. Attach JSON Bucket Policy enforcing HTTPS only.",
        "5. Verify that HTTP requests are blocked while HTTPS succeeds."
    ])

    add_card(s19, 8.8, 1.5, 3.7, 5.2, "Lab 3: VPC & Subnet Isolation", [
        "1. Create VPC 10.0.0.0/16 with DNS hostnames enabled.",
        "2. Carve Public Subnet (10.0.1.0/24) & Private Subnet (10.0.2.0/24).",
        "3. Attach Internet Gateway (IGW) to VPC.",
        "4. Link Public Subnet Route Table to 0.0.0.0/0 -> IGW.",
        "5. Confirm Private Subnet has NO route to IGW."
    ])

    # -----------------------------------------------------------------
    # SLIDE 20: Summary & Golden Rules
    # -----------------------------------------------------------------
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Module 03 Summary & Student Success Rules")
    add_footer(s20, 20)

    add_card(s20, 0.8, 1.5, 5.6, 5.2, "Golden Rules to Remember", [
        "1. The Vehicle Metaphor:",
        "   EC2 = Car Engine | EBS = Personal Trunk | EFS = Fleet Rack | S3 = Global Depot",
        "2. Least Privilege in Security Groups:",
        "   Never open 0.0.0.0/0 for Port 22 SSH in corporate environments. Restrict to My IP.",
        "3. Stateful vs Stateless:",
        "   Security Groups remember outgoing connections; NACLs inspect both ways.",
        "4. Cost Hygiene:",
        "   STOP EC2 instances when leaving the lab. TERMINATE unwanted test volumes."
    ], card_bg=RGBColor(0xEA, 0xF2, 0xF8))

    add_card(s20, 6.8, 1.5, 5.7, 5.2, "Next Steps: What Comes in Module 04?", [
        "• Infrastructure as Code (IaC) with AWS CloudFormation & CDK.",
        "• Automating EC2 and S3 provisioning using Python boto3 scripts.",
        "• AWS Lambda serverless functions triggered by S3 uploads.",
        "• Building a complete end-to-end cloud microservice project.",
        "",
        "Questions & Practice Time!",
        "Open your AWS Console and start Lab 1: EC2 Launch & Lifecycle!"
    ], card_bg=RGBColor(0xFE, 0xF9, 0xE7))

    prs.save(output_path)
    print(f"Successfully generated PowerPoint presentation at: {output_path}")

if __name__ == "__main__":
    out_file = r"F:\Task( Telangana )\Nalgonda\Projects\task\module_03_aws_core\presentation\Module_03_AWS_Core_Services_Masterclass.pptx"
    create_deck(out_file)
