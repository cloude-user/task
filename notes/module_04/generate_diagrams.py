import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

diag_dir = "F:/Task( Telangana )/Nalgonda/Projects/task/notes/module_04/diagrams"
os.makedirs(diag_dir, exist_ok=True)

# -------------------------------------------------------------
# 1. OSI 7 Layers vs AWS Load Balancers Mapping
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title
ax.text(50, 95, "OSI 7-Layer Reference Model vs. AWS Elastic Load Balancer (ELB) Architecture", 
        fontsize=14, fontweight='bold', ha='center', color='#1F4E79')

layers = [
    ("Layer 7: Application", "HTTP, HTTPS, gRPC, WebSocket", "#1B365D", "Application Load Balancer (ALB)\nIntelligent Layer 7 content routing (/api, host, headers, cookies, query)"),
    ("Layer 6: Presentation", "SSL/TLS, ASCII, JPEG, JSON", "#2F5597", "ALB & NLB TLS Termination (ACM integration, SNI, ALPN)"),
    ("Layer 5: Session", "RPC, NetBIOS, Sockets", "#41719C", "Session stickiness, TLS connection management"),
    ("Layer 4: Transport", "TCP, UDP, TLS, QUIC", "#C55A11", "Network Load Balancer (NLB)\nUltra-high speed, millions req/sec, static Anycast/Elastic IP, sub-ms latency"),
    ("Layer 3: Network", "IP, ICMP, IPsec, GENEVE (Port 6081)", "#70AD47", "Gateway Load Balancer (GWLB)\nTransparent L3/L4 inspection, GENEVE encapsulation, appliance firewalls"),
    ("Layer 2: Data Link", "Ethernet, MAC, VLAN, ARP", "#7F7F7F", "AWS VPC Hypervisor, Elastic Network Interfaces (ENI)"),
    ("Layer 1: Physical", "Fiber, Cables, Transceivers, Bitstream", "#595959", "AWS Nitro System & Global Backbone Infrastructure")
]

y_start = 82
h = 9
spacing = 1.5

for i, (l_title, l_proto, col, aws_map) in enumerate(layers):
    cur_y = y_start - i * (h + spacing)
    # Layer box
    rect_l = patches.FancyBboxPatch((4, cur_y), 46, h, boxstyle="round,pad=0.5", 
                                   facecolor=col, edgecolor='#1F4E79', linewidth=1.5)
    ax.add_patch(rect_l)
    ax.text(6, cur_y + 5.2, l_title, fontsize=10.5, fontweight='bold', color='white', va='center')
    ax.text(6, cur_y + 2.0, f"Protocols: {l_proto}", fontsize=8.5, color='#F2F2F2', va='center')
    
    # Arrow
    ax.annotate('', xy=(54, cur_y + 4.5), xytext=(50.5, cur_y + 4.5),
                arrowprops=dict(arrowstyle="->", color='#262626', lw=1.5))
    
    # AWS Mapping box
    bg_col = "#EBF1F5" if "ALB" in aws_map else ("#FCE4D6" if "NLB" in aws_map else ("#E2EFDA" if "GWLB" in aws_map else "#F2F2F2"))
    rect_r = patches.FancyBboxPatch((55, cur_y), 41, h, boxstyle="round,pad=0.5", 
                                   facecolor=bg_col, edgecolor=col, linewidth=1.5)
    ax.add_patch(rect_r)
    ax.text(57, cur_y + 4.5, aws_map, fontsize=8.5, fontweight='bold' if "Load Balancer" in aws_map else 'normal',
            color='#1F4E79' if "ALB" in aws_map else ('#833C0C' if "NLB" in aws_map else ('#385723' if "GWLB" in aws_map else '#333333')), 
            va='center')

plt.tight_layout()
plt.savefig(f"{diag_dir}/12_osi_7_layer_model_vs_elb_mapping.png", dpi=200, bbox_inches='tight')
plt.close()
print("Generated 12_osi_7_layer_model_vs_elb_mapping.png")

# -------------------------------------------------------------
# 2. Sandhya 70mm Multiplex Telugu VPC Analogy
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 8), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 96, "Master AWS VPC Networking Analogy: Sandhya 70mm Multiplex (RTC X Roads, Hyderabad)", 
        fontsize=13, fontweight='bold', ha='center', color='#1F4E79')
ax.text(50, 92.5, "Detailed Step-by-Step Architecture: How Private IPs, Public IPs, IGW 1:1 NAT, and NAT Gateway Operate", 
        fontsize=9.5, ha='center', color='#595959')

# Public Internet / Cinema Fans outside
rect_ext = patches.FancyBboxPatch((3, 76), 20, 12, boxstyle="round,pad=0.5", facecolor='#FFF2CC', edgecolor='#D6B656', linewidth=1.5)
ax.add_patch(rect_ext)
ax.text(13, 83, "Cinema Fans on Highway\n(Public Internet Clients)", fontsize=9, fontweight='bold', ha='center', va='center')
ax.text(13, 78.5, "Public IP: 49.37.10.20\nTarget: 54.210.12.8", fontsize=7.5, ha='center', color='#7F6000')

# Multiplex Compound Wall (VPC 10.0.0.0/16)
rect_vpc = patches.FancyBboxPatch((28, 6), 69, 83, boxstyle="round,pad=1.0", facecolor='#F2F4F8', edgecolor='#1F4E79', linewidth=2.5, linestyle='--')
ax.add_patch(rect_vpc)
ax.text(32, 86, "SANDHYA 70mm MULTIPLEX COMPOUND WALL — Amazon VPC (CIDR: 10.0.0.0/16 · 65,536 Room Extensions)", 
        fontsize=10.5, fontweight='bold', color='#1F4E79')

# Internet Gateway (Grand Double Door Highway Gate)
rect_igw = patches.FancyBboxPatch((24, 76), 8, 12, boxstyle="round,pad=0.4", facecolor='#D9E1F2', edgecolor='#2F5597', linewidth=2)
ax.add_patch(rect_igw)
ax.text(28, 83, "Internet\nGateway (IGW)", fontsize=8, fontweight='bold', ha='center', va='center', color='#1F4E79')
ax.text(28, 78, "Grand Gate\n1:1 NAT Magic", fontsize=7, ha='center', color='#2F5597')

# Arrow Ext -> IGW
ax.annotate('', xy=(24, 82), xytext=(23, 82), arrowprops=dict(arrowstyle="<->", color='#C00000', lw=2))

# Public Subnet (Front Ticket Counter & Canteen)
rect_pub = patches.FancyBboxPatch((36, 52), 58, 29, boxstyle="round,pad=0.5", facecolor='#E2EFDA', edgecolor='#385723', linewidth=1.8)
ax.add_patch(rect_pub)
ax.text(38, 77.5, "PUBLIC SUBNET (10.0.1.0/24) — Front Ticket Counter & Popcorn Canteen", fontsize=9.5, fontweight='bold', color='#385723')
ax.text(38, 74.5, "Route Table points 0.0.0.0/0 -> IGW | Direct highway entry & exit allowed", fontsize=8, color='#555555')

# EC2 Web Server in Public Subnet
rect_web = patches.FancyBboxPatch((40, 56), 24, 15, boxstyle="round,pad=0.4", facecolor='#FFFFFF', edgecolor='#2F5597', linewidth=1.5)
ax.add_patch(rect_web)
ax.text(52, 67, "EC2 Web Server (Ticket Clerk)", fontsize=8.5, fontweight='bold', ha='center', color='#1F4E79')
ax.text(52, 63, "Private IP: 10.0.1.50 (OS sees this)\nPublic IP: 54.210.12.8 (Lives on IGW!)", fontsize=7.5, ha='center')
ax.text(52, 58.5, "Protected by Bouncer Anna (Security Group: Port 80/443)", fontsize=6.8, ha='center', color='#C00000', style='italic')

# NAT Gateway (Chotu the Trusted Peon)
rect_nat = patches.FancyBboxPatch((68, 56), 23, 15, boxstyle="round,pad=0.4", facecolor='#FFF2CC', edgecolor='#D6B656', linewidth=1.5)
ax.add_patch(rect_nat)
ax.text(79.5, 67, "NAT Gateway ('Chotu' Peon)", fontsize=8.5, fontweight='bold', ha='center', color='#7F6000')
ax.text(79.5, 63, "Static Elastic IP: 13.234.50.99\nLives in Public Subnet", fontsize=7.5, ha='center')
ax.text(79.5, 58.5, "Runs to market for Owner; 1-Way Outbound ONLY!", fontsize=6.8, ha='center', color='#2F5597', style='italic')

# Private Subnet (Owner Private Office & Cash Locker)
rect_priv = patches.FancyBboxPatch((36, 11), 58, 35, boxstyle="round,pad=0.5", facecolor='#FCE4D6', edgecolor='#C55A11', linewidth=1.8)
ax.add_patch(rect_priv)
ax.text(38, 42.5, "PRIVATE SUBNET (10.0.2.0/24) — Owner's Office, Projector Room & Cash Locker ('Galla Pette')", fontsize=9.5, fontweight='bold', color='#C55A11')
ax.text(38, 39.5, "Route Table points 0.0.0.0/0 -> NAT Gateway ('Chotu') | Zero direct access from outside highway!", fontsize=8, color='#555555')

# EC2 App / DB Server in Private Subnet
rect_db = patches.FancyBboxPatch((40, 16), 24, 20, boxstyle="round,pad=0.4", facecolor='#FFFFFF', edgecolor='#C55A11', linewidth=1.5)
ax.add_patch(rect_db)
ax.text(52, 31, "Private RDS / EC2 Backend", fontsize=8.5, fontweight='bold', ha='center', color='#833C0C')
ax.text(52, 27, "Private IP: 10.0.2.100 ONLY\nNO Public IP · NO IGW route", fontsize=7.5, ha='center')
ax.text(52, 22.5, "Secret Cash Locker / Customer Database", fontsize=7, ha='center', color='#595959')
ax.text(52, 18.5, "SG: Only allows port 3306 from Web Server SG!", fontsize=6.8, ha='center', color='#C00000', style='italic')

# S3 Gateway Endpoint
rect_s3ep = patches.FancyBboxPatch((68, 16), 23, 20, boxstyle="round,pad=0.4", facecolor='#EBF1F5', edgecolor='#1F4E79', linewidth=1.5)
ax.add_patch(rect_s3ep)
ax.text(79.5, 31, "VPC Gateway Endpoint (S3)", fontsize=8.5, fontweight='bold', ha='center', color='#1F4E79')
ax.text(79.5, 26.5, "Routes direct to S3 private backbone\nFREE (Bypasses NAT Gateway $0.045/GB)", fontsize=7.2, ha='center')
ax.text(79.5, 20, "Prefix List: pl-63a5400a\nNo Public IP needed!", fontsize=7, ha='center', color='#385723', style='italic')

# Internal Intercom connection (Private IP routing)
ax.annotate('Intercom Staff Call\n(10.0.1.50 -> 10.0.2.100)', xy=(52, 36), xytext=(52, 56),
            arrowprops=dict(arrowstyle="<->", color='#2F5597', lw=1.5, linestyle=':'),
            fontsize=7, ha='center', color='#2F5597', fontweight='bold')

# Outbound NAT connection
ax.annotate('Chotu fetches OS patches\n0.0.0.0/0 -> NAT Gateway', xy=(79.5, 56), xytext=(64, 26),
            arrowprops=dict(arrowstyle="->", color='#7F6000', lw=1.5),
            fontsize=7, ha='center', color='#7F6000', fontweight='bold')

# IGW to NAT
ax.annotate('', xy=(32, 80), xytext=(68, 65),
            arrowprops=dict(arrowstyle="<->", color='#1F4E79', lw=1.5))

plt.tight_layout()
plt.savefig(f"{diag_dir}/13_sandhya_70mm_multiplex_vpc_analogy_architecture.png", dpi=200, bbox_inches='tight')
plt.close()
print("Generated 13_sandhya_70mm_multiplex_vpc_analogy_architecture.png")

# -------------------------------------------------------------
# 3. AWS Transit Gateway vs Full Mesh VPC Peering
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=200)

for ax in [ax1, ax2]:
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

# Left: Full Mesh Peering
ax1.text(50, 95, "Full-Mesh VPC Peering Complexity\nN*(N-1)/2 Direct Peering Connections", fontsize=11, fontweight='bold', ha='center', color='#C00000')
ax1.text(50, 88, "Example: 5 VPCs = 10 Peering Connections · Non-Transitive Routing Dilemma", fontsize=8, ha='center', color='#595959')

coords = [(50, 72), (80, 52), (68, 22), (32, 22), (20, 52)]
v_names = ["VPC A (Prod)", "VPC B (Dev)", "VPC C (Shared)", "VPC D (Sec)", "VPC E (Data)"]

for i in range(5):
    for j in range(i+1, 5):
        ax1.plot([coords[i][0], coords[j][0]], [coords[i][1], coords[j][1]], color='#C00000', lw=1.2, linestyle=':')

for i, (x, y) in enumerate(coords):
    circle = patches.Circle((x, y), 8.5, facecolor='#FCE4D6', edgecolor='#C55A11', lw=1.8)
    ax1.add_patch(circle)
    ax1.text(x, y, v_names[i], fontsize=7, fontweight='bold', ha='center', va='center', color='#833C0C')

ax1.text(50, 8, "Problem: No transitive routing (VPC A <-> B <-> C != A <-> C)\nComplex route tables, scales poorly with enterprise growth", 
         fontsize=8, ha='center', color='#C00000', style='italic', bbox=dict(boxstyle="round,pad=0.5", facecolor='#FFF2CC', edgecolor='#D6B656'))

# Right: Transit Gateway Hub & Spoke
ax2.text(50, 95, "AWS Transit Gateway (TGW)\nHub-and-Spoke Centralized Cloud Router", fontsize=11, fontweight='bold', ha='center', color='#385723')
ax2.text(50, 88, "Telugu Analogy: RTC Central Bus Station (MGBS Imlibun) Connecting All Towns", fontsize=8, ha='center', color='#595959')

tgw_circle = patches.Circle((50, 48), 13, facecolor='#2F5597', edgecolor='#1F4E79', lw=2.5)
ax2.add_patch(tgw_circle)
ax2.text(50, 49, "AWS Transit\nGateway (TGW)", fontsize=8.5, fontweight='bold', ha='center', va='center', color='white')
ax2.text(50, 42, "Central Router", fontsize=7, ha='center', color='#D9E1F2')

for i, (x, y) in enumerate(coords):
    ax2.annotate('', xy=(50, 48), xytext=(x, y),
                 arrowprops=dict(arrowstyle="<->", color='#385723', lw=2.2))
    circle = patches.Circle((x, y), 8.5, facecolor='#E2EFDA', edgecolor='#385723', lw=1.8)
    ax2.add_patch(circle)
    ax2.text(x, y, v_names[i], fontsize=7, fontweight='bold', ha='center', va='center', color='#385723')

ax2.text(50, 8, "Benefits: Supports transitive routing, single routing hub, attaches up to 5,000 VPCs,\ninter-region peering, Direct Connect (DX) gateway integration", 
         fontsize=8, ha='center', color='#385723', style='italic', bbox=dict(boxstyle="round,pad=0.5", facecolor='#E2EFDA', edgecolor='#385723'))

plt.tight_layout()
plt.savefig(f"{diag_dir}/14_transit_gateway_hub_and_spoke_vs_full_mesh.png", dpi=200, bbox_inches='tight')
plt.close()
print("Generated 14_transit_gateway_hub_and_spoke_vs_full_mesh.png")

# -------------------------------------------------------------
# 4. Route 53 DNS & HTTPS / TLS Handshake Architecture
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=200)

for ax in [ax1, ax2]:
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

# Left: Route 53 DNS Hierarchy
ax1.text(50, 96, "Amazon Route 53: Global DNS Resolution Flow", fontsize=11, fontweight='bold', ha='center', color='#1F4E79')

dns_steps = [
    ("1. Client Browser Request", "User types: https://api.task.gov.in\nChecks local browser cache & OS resolver", "#FFF2CC"),
    ("2. Recursive Resolver", "ISP Resolver / AWS Route 53 Resolver (10.0.0.2)\nIf cache miss, queries root nameserver", "#EBF1F5"),
    ("3. Root Nameserver (.)", "Directs resolver to .in Top-Level Domain (TLD) server", "#D9E1F2"),
    ("4. TLD Nameserver (.in)", "Directs resolver to Authoritative Nameserver for task.gov.in", "#D9E1F2"),
    ("5. Route 53 Authoritative Nameservers", "Evaluates Routing Policy (Weighted, Latency, Failover)\nReturns ALIAS / A record IP to resolver", "#2F5597"),
    ("6. IP Returned to Browser", "Browser receives IPv4 (e.g. 52.66.180.25) & connects directly", "#E2EFDA")
]

for i, (title, desc, col) in enumerate(dns_steps):
    y = 82 - i * 14
    rect = patches.FancyBboxPatch((5, y), 90, 11, boxstyle="round,pad=0.4", 
                                  facecolor=col, edgecolor='#1F4E79', lw=1.2)
    ax1.add_patch(rect)
    ax1.text(8, y + 6.8, title, fontsize=8.5, fontweight='bold', color='white' if col=='#2F5597' else '#1F4E79')
    ax1.text(8, y + 2.5, desc, fontsize=7.2, color='#F2F2F2' if col=='#2F5597' else '#333333')
    if i < len(dns_steps) - 1:
        ax1.annotate('', xy=(50, y - 2.5), xytext=(50, y), arrowprops=dict(arrowstyle="->", color='#C00000', lw=1.5))

# Right: HTTPS & TLS Handshake (Asymmetric + Symmetric)
ax2.text(50, 96, "HTTPS / TLS 1.3 Cryptographic Handshake", fontsize=11, fontweight='bold', ha='center', color='#1F4E79')

tls_steps = [
    ("Phase 1: TCP 3-Way Handshake (Layer 4)", "Client SYN -> Server SYN-ACK -> Client ACK (Establishes reliable socket on Port 443)", "#F2F4F8", False),
    ("Phase 2: Client Hello (TLS Initiation)", "Supported cipher suites (AES-GCM, CHACHA20) & Client Random sent", "#FFF2CC", False),
    ("Phase 3: Server Hello & Certificate (Asymmetric)", "Server selects cipher suite, sends ACM SSL Certificate & Public Key (RSA/ECC)", "#D9E1F2", True),
    ("Phase 4: Key Exchange & Verification", "Client verifies Certificate Authority (CA) root trust chain.\nDerives Pre-Master Secret using Server Public Key.", "#FCE4D6", True),
    ("Phase 5: Symmetric Session Key Generation", "Both derive identical shared Symmetric Session Key (AES-256-GCM).\nHandshake Finished!", "#E2EFDA", True),
    ("Phase 6: High-Speed Encrypted Data Flow", "All subsequent HTTP requests & responses encrypted symmetrically.\nFast, hardware-accelerated, eavesdropping-proof!", "#2F5597", False)
]

for i, (title, desc, col, is_crypto) in enumerate(tls_steps):
    y = 82 - i * 14
    rect = patches.FancyBboxPatch((5, y), 90, 11, boxstyle="round,pad=0.4", 
                                  facecolor=col, edgecolor='#1F4E79', lw=1.2)
    ax2.add_patch(rect)
    ax2.text(8, y + 6.8, title, fontsize=8.5, fontweight='bold', color='white' if col=='#2F5597' else '#1F4E79')
    ax2.text(8, y + 2.5, desc, fontsize=7.2, color='#F2F2F2' if col=='#2F5597' else '#333333')
    if is_crypto:
        ax2.text(92, y + 5.5, "🔒 ASYMMETRIC" if "Asymmetric" in title or "Verification" in title else "🔑 SYMMETRIC", 
                 fontsize=6.5, fontweight='bold', ha='right', color='#C00000' if "ASYMMETRIC" in title or "Verification" in title else '#385723')
    if i < len(tls_steps) - 1:
        ax2.annotate('', xy=(50, y - 2.5), xytext=(50, y), arrowprops=dict(arrowstyle="->", color='#2F5597', lw=1.5))

plt.tight_layout()
plt.savefig(f"{diag_dir}/15_route_53_dns_resolution_and_routing_policies.png", dpi=200, bbox_inches='tight')
plt.close()
print("Generated 15_route_53_dns_resolution_and_routing_policies.png")

# -------------------------------------------------------------
# 5. Horizontal vs Vertical Scaling & Auto Scaling Groups (ASG)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5), dpi=200)

for ax in [ax1, ax2]:
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

# Left: Scaling Comparison
ax1.text(50, 95, "Vertical Scaling vs. Horizontal Scaling", fontsize=11, fontweight='bold', ha='center', color='#1F4E79')

# Vertical
rect_v = patches.FancyBboxPatch((5, 52), 90, 36, boxstyle="round,pad=0.5", facecolor='#FCE4D6', edgecolor='#C55A11', lw=1.5)
ax1.add_patch(rect_v)
ax1.text(8, 83, "Vertical Scaling (Scale Up / Scale Down)", fontsize=10, fontweight='bold', color='#833C0C')
ax1.text(8, 77, "• Change instance type: t3.micro (1 vCPU, 1 GB) -> m5.4xlarge (16 vCPU, 64 GB)", fontsize=8, color='#333333')
ax1.text(8, 71, "• Major Drawback: Requires stopping instance (DOWNTIME!).", fontsize=8, fontweight='bold', color='#C00000')
ax1.text(8, 65, "• Hardware Ceiling: Hit physical maximum limit of available server hardware.", fontsize=8, color='#333333')
ax1.text(8, 59, "• Single Point of Failure: If that single giant instance dies, entire app goes offline!", fontsize=8, color='#333333')

# Horizontal
rect_h = patches.FancyBboxPatch((5, 10), 90, 36, boxstyle="round,pad=0.5", facecolor='#E2EFDA', edgecolor='#385723', lw=1.5)
ax1.add_patch(rect_h)
ax1.text(8, 41, "Horizontal Scaling (Scale Out / Scale In) — CLOUD ELASTICITY", fontsize=10, fontweight='bold', color='#385723')
ax1.text(8, 35, "• Add or remove identical small/medium instances dynamically based on demand.", fontsize=8, color='#333333')
ax1.text(8, 29, "• Zero Downtime: Traffic dynamically balanced across fleet via ALB.", fontsize=8, fontweight='bold', color='#385723')
ax1.text(8, 23, "• Infinite Scaling: Add 2, 20, or 2,000 instances across Multiple Availability Zones.", fontsize=8, color='#333333')
ax1.text(8, 17, "• High Fault Tolerance: If 1 server crashes, ASG replaces it automatically without impact.", fontsize=8, color='#333333')

# Right: EC2 Auto Scaling Target Tracking Architecture
ax2.text(50, 95, "EC2 Auto Scaling Group (ASG) & Target Tracking Architecture", fontsize=11, fontweight='bold', ha='center', color='#1F4E79')

# Application Load Balancer
rect_alb = patches.FancyBboxPatch((30, 77), 40, 11, boxstyle="round,pad=0.4", facecolor='#D9E1F2', edgecolor='#2F5597', lw=1.8)
ax2.add_patch(rect_alb)
ax2.text(50, 83.5, "Application Load Balancer (ALB)", fontsize=9, fontweight='bold', ha='center', color='#1F4E79')
ax2.text(50, 79.5, "Distributes incoming traffic across healthy targets", fontsize=7.2, ha='center', color='#555555')

# ASG boundary
rect_asg = patches.FancyBboxPatch((5, 18), 90, 52, boxstyle="round,pad=0.8", facecolor='#F2F4F8', edgecolor='#1F4E79', lw=2, linestyle='--')
ax2.add_patch(rect_asg)
ax2.text(8, 66, "EC2 Auto Scaling Group (Min: 2 · Desired: 2 · Max: 10)", fontsize=9.5, fontweight='bold', color='#1F4E79')
ax2.text(8, 62, "Launch Template: Amazon Linux 2023 · Auto-replaces failed instances across AZ-a & AZ-b", fontsize=7.5, color='#555555')

# Instances in AZ-a
rect_aza = patches.FancyBboxPatch((10, 24), 36, 33, boxstyle="round,pad=0.4", facecolor='#EBF1F5', edgecolor='#2F5597', lw=1.2)
ax2.add_patch(rect_aza)
ax2.text(28, 53, "Availability Zone A (ap-south-1a)", fontsize=8, fontweight='bold', ha='center', color='#1F4E79')
rect_i1 = patches.FancyBboxPatch((14, 30), 28, 18, boxstyle="round,pad=0.3", facecolor='white', edgecolor='#2F5597', lw=1)
ax2.add_patch(rect_i1)
ax2.text(28, 41, "EC2 Instance 1 (Healthy)\nt3.micro · Private IP", fontsize=7.5, ha='center', color='#262626')
ax2.text(28, 34, "CPU: 45%", fontsize=7.5, fontweight='bold', ha='center', color='#385723')

# Instances in AZ-b
rect_azb = patches.FancyBboxPatch((54, 24), 36, 33, boxstyle="round,pad=0.4", facecolor='#EBF1F5', edgecolor='#2F5597', lw=1.2)
ax2.add_patch(rect_azb)
ax2.text(72, 53, "Availability Zone B (ap-south-1b)", fontsize=8, fontweight='bold', ha='center', color='#1F4E79')
rect_i2 = patches.FancyBboxPatch((58, 30), 28, 18, boxstyle="round,pad=0.3", facecolor='white', edgecolor='#2F5597', lw=1)
ax2.add_patch(rect_i2)
ax2.text(72, 41, "EC2 Instance 2 (Healthy)\nt3.micro · Private IP", fontsize=7.5, ha='center', color='#262626')
ax2.text(72, 34, "CPU: 48%", fontsize=7.5, fontweight='bold', ha='center', color='#385723')

# ALB arrows to instances
ax2.annotate('', xy=(28, 49), xytext=(40, 77), arrowprops=dict(arrowstyle="->", color='#2F5597', lw=1.5))
ax2.annotate('', xy=(72, 49), xytext=(60, 77), arrowprops=dict(arrowstyle="->", color='#2F5597', lw=1.5))

# CloudWatch Alarm & Scaling Policy
rect_cw = patches.FancyBboxPatch((15, 6), 70, 9, boxstyle="round,pad=0.4", facecolor='#FFF2CC', edgecolor='#D6B656', lw=1.2)
ax2.add_patch(rect_cw)
ax2.text(50, 11.5, "CloudWatch Target Tracking Policy: Maintain Average CPU Utilization = 50%", fontsize=8, fontweight='bold', ha='center', color='#7F6000')
ax2.text(50, 8, "If CPU > 50% -> Automatically scales out (+1, +2 instances). If CPU < 30% -> Drains & scales in.", fontsize=7, ha='center', color='#595959')

plt.tight_layout()
plt.savefig(f"{diag_dir}/17_horizontal_scaling_asg_target_tracking.png", dpi=200, bbox_inches='tight')
plt.close()
print("Generated 17_horizontal_scaling_asg_target_tracking.png")
