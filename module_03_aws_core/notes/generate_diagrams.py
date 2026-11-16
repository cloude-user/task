"""
Generates high-resolution architectural diagrams for AWS Module 03:
Infused with relatable Tollywood Cinema, Sandhya 70mm, and Telangana Kirana Shop analogies
alongside enterprise AWS technical specifications for TASK non-tech students.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs(r"e:\trainer\task\module_03_aws_core\notes\diagrams", exist_ok=True)
output_dir = r"e:\trainer\task\module_03_aws_core\notes\diagrams"

def generate_vpc_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    c_aws_navy = "#232F3E"
    c_aws_orange = "#FF9900"
    c_vpc_bg = "#F8FAFC"
    c_pub_subnet = "#E0F2FE"
    c_priv_subnet = "#FEF3C7"

    # Title
    ax.text(50, 96.5, "AWS VPC ARCHITECTURE · THE TOLLYWOOD CINEMA COMPOUND ANALOGY", 
            fontsize=14, fontweight='bold', color=c_aws_navy, ha='center')
    ax.text(50, 93.5, "VPC CIDR: 10.0.0.0/16 ('Sandhya 70mm Multiplex Compound') | 5 Reserved IPs per Subnet (.0, .1, .2, .3, .255)", 
            fontsize=9, color="#475569", ha='center', style='italic')

    # Internet Box (Top)
    internet_box = patches.FancyBboxPatch((30, 82), 40, 8, boxstyle="round,pad=0.5", 
                                          ec="#2563EB", fc="#EFF6FF", lw=2)
    ax.add_patch(internet_box)
    ax.text(50, 86, "PUBLIC INTERNET (0.0.0.0/0)\n[RTC X Roads National Highway - Open to All Fans]", 
            fontsize=9, fontweight='bold', color="#1E40AF", ha='center', va='center')

    # IGW Gateway
    igw_box = patches.FancyBboxPatch((36, 71.5), 28, 7, boxstyle="square,pad=0.3", 
                                     ec=c_aws_orange, fc="#FFFBEB", lw=2)
    ax.add_patch(igw_box)
    ax.text(50, 75, "INTERNET GATEWAY (IGW)\n'Main Double-Door Highway Gate (2-Way Entry)'", 
            fontsize=8, fontweight='bold', color="#B45309", ha='center', va='center')

    # Connect Internet to IGW
    ax.annotate('', xy=(50, 78.5), xytext=(50, 82),
                arrowprops=dict(arrowstyle="<->", color="#2563EB", lw=2.5))

    # Outer VPC Box
    vpc_patch = patches.FancyBboxPatch((5, 4), 90, 65, boxstyle="round,pad=0.8", 
                                       ec=c_aws_navy, fc=c_vpc_bg, lw=2.5, ls="--")
    ax.add_patch(vpc_patch)
    ax.text(8, 66, "VPC: 10.0.0.0/16 ('Sandhya 70mm Cinema Compound Wall - 65,536 Total Plots')", 
            fontsize=10.5, fontweight='bold', color=c_aws_navy)

    # Route 53 Resolver Box (.2)
    dns_box = patches.FancyBboxPatch((64, 61), 28, 6.5, boxstyle="round,pad=0.3",
                                     ec="#10B981", fc="#ECFDF5", lw=1.5)
    ax.add_patch(dns_box)
    ax.text(78, 64.25, "DNS RESOLVER: 10.0.0.2 (VPC Base + 2)\n'Theatre Enquiry Counter Desk'", 
            fontsize=7.2, fontweight='bold', color="#065F46", ha='center', va='center')

    # Public Subnet
    pub_box = patches.FancyBboxPatch((8, 38), 84, 21.5, boxstyle="round,pad=0.5",
                                     ec="#0284C7", fc=c_pub_subnet, lw=1.8)
    ax.add_patch(pub_box)
    ax.text(12, 57, "PUBLIC SUBNET (10.0.1.0/24) · 'Front Ticket Counter & Canteen' (Route: 0.0.0.0/0 ➔ IGW)", 
            fontsize=9.2, fontweight='bold', color="#0369A1")

    # Inside Public Subnet: ALB and NAT Gateway
    alb_box = patches.FancyBboxPatch((12, 40.5), 33, 14, boxstyle="round,pad=0.3",
                                     ec="#2563EB", fc="#FFFFFF", lw=1.2)
    ax.add_patch(alb_box)
    ax.text(28.5, 48.5, "Application Load Balancer (ALB)\n'Multiplex Chief Manager'", 
            fontsize=8, fontweight='bold', color="#1E40AF", ha='center')
    ax.text(28.5, 43, "Public IP + Checks Tickets (Port 80/443)", fontsize=7.2, color="#64748B", ha='center')

    nat_box = patches.FancyBboxPatch((51, 40.5), 38, 14, boxstyle="round,pad=0.3",
                                     ec="#D97706", fc="#FFFFFF", lw=1.2)
    ax.add_patch(nat_box)
    ax.text(70, 48.5, "NAT GATEWAY (Elastic IP Attached)\n'Theatre Boy with Outbound Gate Pass'", 
            fontsize=8, fontweight='bold', color="#B45309", ha='center')
    ax.text(70, 43, "Fetches Kirana/Swiggy lunch; blocks outsiders from entering", fontsize=6.8, color="#64748B", ha='center')

    # Connect IGW to Public Subnet
    ax.annotate('', xy=(50, 59.5), xytext=(50, 71.5),
                arrowprops=dict(arrowstyle="<->", color=c_aws_orange, lw=2.5))

    # Private Subnet
    priv_box = patches.FancyBboxPatch((8, 6.5), 84, 28, boxstyle="round,pad=0.5",
                                      ec="#D97706", fc=c_priv_subnet, lw=1.8)
    ax.add_patch(priv_box)
    ax.text(12, 31.5, "PRIVATE SUBNET (10.0.2.0/24) · 'Projector Room & Producer Cash Safe (Galla Pette)' (Route: ➔ NAT GW)", 
            fontsize=9.2, fontweight='bold', color="#B45309")

    # EC2 Instances in Private Subnet
    ec2_box = patches.FancyBboxPatch((12, 9), 38, 19, boxstyle="round,pad=0.3",
                                     ec="#475569", fc="#FFFFFF", lw=1.2)
    ax.add_patch(ec2_box)
    ax.text(31, 24, "EC2 App Server ('Movie Operator Desk')", fontsize=8.2, fontweight='bold', color=c_aws_navy, ha='center')
    ax.text(31, 19.5, "• Private IP: 10.0.2.15 (Internal Seat No.)\n• Guarded by Bouncer Anna (Stateful SG)", 
            fontsize=7.2, color="#334155", ha='center')
    ax.text(31, 13.5, "Outbound movie patch downloads route ➔ NAT GW", fontsize=6.8, color="#D97706", ha='center')

    # RDS in Private Subnet
    rds_box = patches.FancyBboxPatch((53, 9), 36, 19, boxstyle="round,pad=0.3",
                                     ec="#7C3AED", fc="#FFFFFF", lw=1.2)
    ax.add_patch(rds_box)
    ax.text(71, 24, "Amazon RDS ('Producer Money Safe - Galla Pette')", fontsize=8, fontweight='bold', color="#6D28D9", ha='center')
    ax.text(71, 19.5, "• Multi-AZ Standby copy in 2nd theatre (10.0.3.x)\n• SG allows Port 5432 from App EC2 only", 
            fontsize=7.2, color="#334155", ha='center')
    ax.text(71, 13.5, "Strictly Locked Inside Private Safe", fontsize=7.2, color="#059669", ha='center')

    # Arrows between Tiers
    ax.annotate('', xy=(31, 28), xytext=(28.5, 40.5),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2))
    ax.annotate('', xy=(53, 18.5), xytext=(50, 18.5),
                arrowprops=dict(arrowstyle="<->", color="#7C3AED", lw=2))
    ax.annotate('', xy=(70, 40.5), xytext=(38, 28),
                arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.8, ls="--"))

    plt.tight_layout()
    path = os.path.join(output_dir, "01_vpc_networking_architecture.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print("Generated:", path)

def generate_dns_flow_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 5.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    c_navy = "#232F3E"
    c_blue = "#1D4ED8"
    c_green = "#047857"

    ax.text(50, 94, "HOW AMAZON VPC DNS RESOLVER WORKS (10.0.0.2 / VPC Base + 2)", 
            fontsize=13, fontweight='bold', color=c_navy, ha='center')
    ax.text(50, 89, "The Theatre Enquiry Desk: Resolving Internal Walkie-Talkie Calls vs External BookMyShow", 
            fontsize=9, color="#64748B", ha='center')

    # Step 1: EC2 Instance
    ec2_box = patches.FancyBboxPatch((5, 42), 24, 32, boxstyle="round,pad=0.4", ec=c_navy, fc="#F8FAFC", lw=1.5)
    ax.add_patch(ec2_box)
    ax.text(17, 68, "EC2 Operator Desk\n(IP: 10.0.2.15)", fontsize=8.5, fontweight='bold', color=c_navy, ha='center')
    ax.text(17, 53, "Staff calls name:\n1. 'safe.producer.internal'\n2. 'bookmyshow.com'", fontsize=7.8, color="#334155", ha='center')

    # Step 2: VPC DNS Resolver (AmazonProvidedDNS)
    resolver_box = patches.FancyBboxPatch((36, 35), 28, 45, boxstyle="round,pad=0.4", ec="#059669", fc="#ECFDF5", lw=2)
    ax.add_patch(resolver_box)
    ax.text(50, 74, "Route 53 Resolver\n(10.0.0.2 / VPC Base + 2)\n'Theatre Enquiry Counter'", fontsize=8.5, fontweight='bold', color="#065F46", ha='center')
    ax.text(50, 58, "1. Checks local registry\n2. Looks up Private Zone\n3. If public, recurses\n   to external internet", 
            fontsize=7.5, color="#047857", ha='center')
    ax.text(50, 42, "Always VPC Base + 2\n(Inside the Theatre)", fontsize=7.2, color="#64748B", ha='center')

    # Step 3A: Route 53 Private Hosted Zone
    phz_box = patches.FancyBboxPatch((72, 57), 25, 23, boxstyle="round,pad=0.4", ec="#7C3AED", fc="#F5F3FF", lw=1.5)
    ax.add_patch(phz_box)
    ax.text(84.5, 73, "Private Hosted Zone\n'Staff Intercom List'", fontsize=8.2, fontweight='bold', color="#6D28D9", ha='center')
    ax.text(84.5, 63, "'safe.producer.internal' ➔\n10.0.3.50 (Galla Pette)", fontsize=7.5, color="#4C1D95", ha='center')

    # Step 3B: Public Internet Root DNS
    pubdns_box = patches.FancyBboxPatch((72, 18), 25, 23, boxstyle="round,pad=0.4", ec="#2563EB", fc="#EFF6FF", lw=1.5)
    ax.add_patch(pubdns_box)
    ax.text(84.5, 34, "Public Internet DNS\n'Public Yellow Pages'", fontsize=8.2, fontweight='bold', color="#1E40AF", ha='center')
    ax.text(84.5, 25, "'bookmyshow.com' ➔\n140.82.121.6 (Public IP)", fontsize=7.5, color="#1E3A8A", ha='center')

    # Arrows
    ax.annotate('1. Ask Name', xy=(36, 62), xytext=(29, 62),
                arrowprops=dict(arrowstyle="->", color=c_blue, lw=1.5), fontsize=8, color=c_blue)
    ax.annotate('4. Return IP', xy=(29, 50), xytext=(36, 50),
                arrowprops=dict(arrowstyle="->", color=c_green, lw=1.5), fontsize=8, color=c_green)
    ax.annotate('2A. Internal lookup', xy=(72, 68), xytext=(64, 68),
                arrowprops=dict(arrowstyle="<->", color="#7C3AED", lw=1.5), fontsize=7.2, color="#7C3AED")
    ax.annotate('2B. External recursive', xy=(72, 30), xytext=(64, 44),
                arrowprops=dict(arrowstyle="<->", color="#2563EB", lw=1.5), fontsize=7.2, color="#2563EB")

    ax.text(50, 7, "Prerequisite: Set 'enableDnsSupport = true' and 'enableDnsHostnames = true' in VPC Settings!",
            fontsize=8.2, fontweight='bold', color="#DC2626", ha='center')

    plt.tight_layout()
    path = os.path.join(output_dir, "02_dns_resolver_flow.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print("Generated:", path)

def generate_ec2_types_diagram():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    c_navy = "#232F3E"

    ax.text(50, 95, "AMAZON EC2 INSTANCE FAMILIES · THE TOLLYWOOD TRANSPORT FLEET", 
            fontsize=13, fontweight='bold', color=c_navy, ha='center')
    ax.text(50, 90, "Match your server engine horsepower to the exact shooting requirement", 
            fontsize=9, color="#64748B", ha='center')

    families = [
        ("General Purpose (T, M)", "The Hero's Everyday City Sedan (Swift / Auto)", "Balanced CPU & RAM. t3.micro (Free Tier) with burstable CPU credits. Perfect for web servers, dev/testing.", "#0284C7", "#E0F2FE", 74),
        ("Compute Optimized (C)", "The Action Chase Formula 1 Sports Car", "High CPU-to-memory ratio. Raw compute horsepower. Media transcoding, high-speed gaming, batch calculation.", "#DC2626", "#FEE2E2", 56),
        ("Memory Optimized (R, X)", "The 100-Member Lavish Wedding Dance Troupe Bus", "Massive RAM memory capacity per vCPU. In-memory data caches (Redis/Memcached), SAP HANA, real-time analytics.", "#7C3AED", "#EDE9FE", 38),
        ("Storage Optimized (I, D)", "The 10-Ton Heavy Freight Goods Lorry", "Massive sequential read/write IOPS directly on NVMe SSD. Big data warehouses, Cassandra, Elasticsearch.", "#D97706", "#FEF3C7", 20),
        ("Accelerated / GPU (P, G)", "The Bahubali / RRR VFX Rendering Supercomputer", "Hardware GPU accelerators. Deep learning model training, generative AI, 3D computer vision CGI rendering.", "#059669", "#ECFDF5", 2)
    ]

    for title, vehicle, desc, ec, fc, y in families:
        patch = patches.FancyBboxPatch((5, y), 90, 15, boxstyle="round,pad=0.4", ec=ec, fc=fc, lw=1.5)
        ax.add_patch(patch)
        ax.text(8, y + 10.5, title, fontsize=9.2, fontweight='bold', color=ec)
        ax.text(8, y + 6.5, f"Tollywood Analogy: {vehicle}", fontsize=8.2, fontweight='bold', color="#1F2937")
        ax.text(8, y + 2.5, desc, fontsize=7.2, color="#374151")

    plt.tight_layout()
    path = os.path.join(output_dir, "03_ec2_instance_types.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print("Generated:", path)

def generate_storage_triad_diagram():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    c_navy = "#232F3E"

    ax.text(50, 95, "AWS STORAGE TRIAD: POCKET vs BIRYANI THALI vs D-MART WAREHOUSE", 
            fontsize=13, fontweight='bold', color=c_navy, ha='center')
    ax.text(50, 90, "EBS (Block) vs EFS (File) vs S3 (Object) Comparison & Decision Triggers", 
            fontsize=9, color="#64748B", ha='center')

    # Card 1: EBS
    ebs = patches.FancyBboxPatch((4, 8), 28, 76, boxstyle="round,pad=0.5", ec="#2563EB", fc="#EFF6FF", lw=2)
    ax.add_patch(ebs)
    ax.text(18, 79, "Amazon EBS\n(Block Storage)", fontsize=11, fontweight='bold', color="#1E40AF", ha='center')
    ax.text(18, 70, "'Your Personal Jeans Pocket'", fontsize=8.2, fontweight='bold', color="#1D4ED8", ha='center')
    ebs_text = (
        "• Scope: Single AZ only\n"
        "• Attachment: 1 EC2 instance\n"
        "• Protocol: Virtual SCSI Block\n"
        "• Latency: < 1ms ultra-low\n"
        "• 4 KB Block modification: Edit\n"
        "  1 word in 1 GB -> only 4 KB\n"
        "  block is rewritten!\n"
        "• OS Boot Disk: YES (Mandatory)\n\n"
        "🎯 BEST FOR:\n"
        "• OS root boot drives\n"
        "• High-speed SQL databases"
    )
    ax.text(6, 36, ebs_text, fontsize=7.2, color="#1E293B")

    # Card 2: EFS
    efs = patches.FancyBboxPatch((36, 8), 28, 76, boxstyle="round,pad=0.5", ec="#D97706", fc="#FFFBEB", lw=2)
    ax.add_patch(efs)
    ax.text(50, 79, "Amazon EFS\n(File Storage)", fontsize=11, fontweight='bold', color="#B45309", ha='center')
    ax.text(50, 70, "'Shared Family Biryani Thali'", fontsize=8.2, fontweight='bold', color="#D97706", ha='center')
    efs_text = (
        "• Scope: Regional (Multi-AZ)\n"
        "• Attachment: 1000s of EC2s\n"
        "• Protocol: NFSv4 (POSIX)\n"
        "• Latency: ~3-5ms (File locking)\n"
        "• Elastic Pay-as-you-go: Grows\n"
        "  automatically, shrink bill on delete\n"
        "• OS Boot Disk: NO\n"
        "• Port: 2049 (NFS)\n\n"
        "🎯 BEST FOR:\n"
        "• Shared WordPress /wp-content/\n"
        "• Distributed content media"
    )
    ax.text(38, 36, efs_text, fontsize=7.2, color="#1E293B")

    # Card 3: S3
    s3 = patches.FancyBboxPatch((68, 8), 28, 76, boxstyle="round,pad=0.5", ec="#059669", fc="#ECFDF5", lw=2)
    ax.add_patch(s3)
    ax.text(82, 79, "Amazon S3\n(Object Storage)", fontsize=11, fontweight='bold', color="#065F46", ha='center')
    ax.text(82, 70, "'Giant D-Mart Central Godown'", fontsize=8.2, fontweight='bold', color="#059669", ha='center')
    s3_text = (
        "• Scope: Regional / Global\n"
        "• Attachment: Web URL / HTTPS\n"
        "• Durability: 99.999999999% (11 9s)\n"
        "• Capacity: Infinite Petabytes\n"
        "• 7 Storage Tiers: Standard to\n"
        "  Deep Archive (Rs. 80 / TB / mo)\n"
        "• Security: Block Public Access\n\n"
        "🎯 BEST FOR:\n"
        "• Static websites & media assets\n"
        "• Database backups & data lakes"
    )
    ax.text(70, 36, s3_text, fontsize=7.2, color="#1E293B")

    plt.tight_layout()
    path = os.path.join(output_dir, "04_storage_triad_comparison.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print("Generated:", path)

def generate_database_decision_diagram():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    c_navy = "#232F3E"

    ax.text(50, 95, "AWS DATABASES & CACHING · KIRANA SHOP & BOX OFFICE ACCOUNTS", 
            fontsize=13, fontweight='bold', color=c_navy, ha='center')
    ax.text(50, 90, "Matching Data Patterns to the Optimal Managed Cloud Engine", 
            fontsize=9, color="#64748B", ha='center')

    cards = [
        ("Amazon RDS", "Traditional Baddi Khatavahi Ledger", 
         "• Strict columns & rows with ACID transactions\n• Multi-AZ standby copy (Carbon-copy ledger at home)\n• Read Replicas (up to 15) to scale reading\n• Port: 5432 (Postgres), 3306 (MySQL)\n\nBEST FOR: Financial ERP, banking ledgers,\ncomplex multi-table JOIN queries.", "#2563EB", "#EFF6FF", 4, 48),

        ("Amazon Aurora", "High-Speed Barcode Billing at D-Mart", 
         "• 5x faster than MySQL, 3x faster than Postgres\n• Storage replicates 6 copies across 3 AZs\n• Storage auto-expands up to 128 TiB\n• Aurora Serverless v2 auto-scaling\n\nBEST FOR: High-volume SaaS, critical banking,\nzero data loss enterprise SQL.", "#7C3AED", "#F5F3FF", 52, 48),

        ("Amazon DynamoDB", "Swiggy / Zomato Live Token Counter", 
         "• Single-digit millisecond latency at any scale\n• Serverless NoSQL (Partition Key & Sort Key)\n• Scales to 10 lakh orders during IPL match\n• Seamless On-Demand capacity\n\nBEST FOR: User shopping carts, gaming sessions,\nIoT telemetry, high-velocity clickstreams.", "#D97706", "#FFFBEB", 4, 4),

        ("Amazon ElastiCache", "Kirana Counter Chillar Box & Front Tray", 
         "• Microsecond response time in RAM\n• Sits in front of RDS/DynamoDB (Cache-Aside)\n• Solves database query bottlenecks\n• Stores user auth tokens & live leaderboards\n\nBEST FOR: Eliminating slow DB query repeat,\nsession cache, live sports scores.", "#059669", "#ECFDF5", 52, 4)
    ]

    for title, subtitle, content, ec, fc, x, y in cards:
        patch = patches.FancyBboxPatch((x, y), 44, 40, boxstyle="round,pad=0.4", ec=ec, fc=fc, lw=1.8)
        ax.add_patch(patch)
        ax.text(x + 3, y + 35, title, fontsize=9.5, fontweight='bold', color=ec)
        ax.text(x + 3, y + 31, subtitle, fontsize=8, fontweight='bold', color="#374151")
        ax.text(x + 3, y + 14, content, fontsize=7, color="#1F2937")

    plt.tight_layout()
    path = os.path.join(output_dir, "05_database_decision_matrix.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print("Generated:", path)

if __name__ == "__main__":
    generate_vpc_diagram()
    generate_dns_flow_diagram()
    generate_ec2_types_diagram()
    generate_storage_triad_diagram()
    generate_database_decision_diagram()
    print("All 5 Tollywood & Kirana shop diagrams generated successfully!")
