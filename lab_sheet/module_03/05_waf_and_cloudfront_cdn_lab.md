# Lab Sheet 3.5: Web Security & Content Acceleration — AWS WAF & CloudFront
> **Module 3:** AWS Associate Core Knowledge  
> **Topic 3.c:** Web Application Firewall (WAF) & CloudFront CDN  
> **Target:** Cloud Software Developer Trainees  

---

## 🎯 Lab Objectives
1. Configure an **Amazon CloudFront Distribution** to globally cache and accelerate static website assets.
2. Understand origins, cache behaviors, Time-To-Live (TTL), and cache invalidations.
3. Create an **AWS WAF (Web Application Firewall) Web ACL** to protect against SQL Injection and XSS attacks.
4. Associate AWS WAF with CloudFront or an Application Load Balancer.

---

## 🛠️ Part 1: Amazon CloudFront CDN Acceleration

### Step 1: Create a CloudFront Distribution
1. Open the [AWS Management Console](https://console.aws.amazon.com/) and navigate to **CloudFront**.
2. Click the orange **Create distribution** button.
3. **Origin domain:** Select your S3 static website bucket (or EC2 Public DNS).
4. **Origin access:**
   * Select **Origin access control settings (recommended)** (OAC) to secure the S3 bucket so users cannot bypass CloudFront!
   * Click **Create control setting** -> Click **Create**.
5. **Default cache behavior:**
   * Viewer protocol policy: **Redirect HTTP to HTTPS**.
   * Allowed HTTP methods: `GET, HEAD`.
   * Cache key and origin requests: Select **CacheOptimized**.
6. **Web Application Firewall (WAF):** Choose *Do not enable security protections* for now (we will attach our custom WAF in Part 2).
7. Click **Create distribution**.
8. CloudFormation/CloudFront will deploy your distribution to 450+ global edge locations.
9. Copy your **Distribution domain name** (e.g., `d12345abcdef.cloudfront.net`) and test it in your browser!

### Step 2: Test Cache Invalidation
1. If you update an image or HTML file in S3, CloudFront edge servers still serve the cached version until TTL expires.
2. Click the **Invalidations** tab -> Click **Create invalidation**.
3. Object paths: `/*` (or `/index.html`) -> Click **Create invalidation**.
4. In under 60 seconds, CloudFront flushes the edge cache worldwide!

---

## 🛠️ Part 2: AWS WAF (Web Application Firewall) Protection

### Step 1: Create a Web ACL (Access Control List)
1. In the console search bar, type **WAF** and click on **AWS WAF & Shield**.
2. In the left navigation, click **Web ACLs** -> Click **Create web ACL**.
3. **Name:** `task-web-firewall-acl`.
4. **Resource type:** Select **Amazon CloudFront distributions** (Global) or **Regional resources** (ALB).
5. Click **Add AWS resources** -> Select your CloudFront distribution -> Click **Add**.
6. Click **Next**.

### Step 2: Add AWS Managed Rule Groups
1. Under *Rules*, click the **Add rules** dropdown -> Select **Add managed rule groups**.
2. Expand **AWS managed rule groups**:
   * Locate **Core rule set (CRS)** -> Toggle **Add to web ACL**. (Protects against OWASP Top 10 exploits).
   * Locate **SQL database** -> Toggle **Add to web ACL**. (Protects against SQL Injection `SQLi`).
   * Locate **Known bad inputs** -> Toggle **Add to web ACL**. (Protects against invalid request bodies).
3. Click **Add rules** -> Click **Next**.
4. Set rule priority (leave defaults) -> Click **Next**.
5. Leave CloudWatch metrics enabled -> Click **Next** -> Click **Create web ACL**.

---

### ✅ Verification Checklist
- [ ] CloudFront distribution status: `Enabled`.
- [ ] Website loads via HTTPS domain `dxxxxxxxx.cloudfront.net`.
- [ ] AWS WAF Web ACL successfully associated and monitoring requests.
