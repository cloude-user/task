# Lab 4.1b: AWS Well-Architected Tool & Enterprise Cost Guardrails
> **Course Track:** Cloud Software Developer (Module 4: AWS Solutions Architect)  
> **Lab Focus:** Well-Architected Framework Assessment, AWS Budgets, Cost Anomaly Detection & Zero-Spend Shield  
> **Prerequisites:** Active AWS Account with Billing & Cost Management access.  

---

## 🎯 Lab Objectives
By the end of this lab, you will have demonstrated:
1. Conducting a formal cloud workload evaluation using the **AWS Well-Architected Tool**.
2. Documenting architectural risks across the 6 Pillars of the Well-Architected Framework.
3. Creating an **AWS Zero-Spend Budget** with automated email notifications.
4. Setting up a monthly cost threshold budget with **80% Forecasted Alerts**.
5. Configuring **AWS Cost Anomaly Detection** to identify unexpected spending spikes.

---

## 🛠️ Step-by-Step Practical Instructions

### Task 1: Conduct a Well-Architected Workload Review
1. Open the **AWS Management Console** → Search for **Well-Architected Tool**.
2. Click **Define workload**.
3. Fill in the workload details:
   - **Workload name:** `TASK-Student-Ecommerce-Workload`
   - **Description:** `Production 3-tier web application evaluation`
   - **Review owner:** Your name / email.
   - **Environment:** `Production`
   - **Regions:** Select `Asia Pacific (Mumbai) ap-south-1`.
4. Click **Next** → Select the **AWS Well-Architected Framework Lens** → Click **Define workload**.
5. Click **Start review**.
6. Evaluate key pillar questions:
   - **Security:** Check *"How do you securely manage identities and permissions?"* → Select *"Rely on centralized identity provider"* and *"Apply least privilege permissions"*.
   - **Reliability:** Check *"How do you design your workload service architecture?"* → Select *"Use highly available services (Multi-AZ)"* and *"Implement loose coupling with queues"*.
   - **Cost Optimization:** Check *"How do you monitor usage and cost?"* → Select *"Configure billing alerts and cost allocation tags"*.
7. Review the generated **Milestone Report** and examine the identified High Risk Issues (HRIs) and Medium Risk Issues (MRIs).

---

### Task 2: Configure an AWS Zero-Spend Budget (Student Safety Shield)
1. Open the search bar → Navigate to **AWS Budgets** (inside Billing & Cost Management).
2. Click **Create budget**.
3. Under **Budget setup**, choose **Use a template (simplified)**.
4. Select **Zero spend budget**:
   - Budget name: `TASK-Zero-Spend-Guardrail`
   - Email recipients: Enter your personal email address.
   - *Behavior:* AWS will immediately send an alert if your account incurs any charges exceeding **$0.01**.
5. Click **Create budget**.

---

### Task 3: Create a Monthly Cost Threshold Budget with Forecast Alert
1. In the AWS Budgets console, click **Create budget** again.
2. Select **Customize (advanced)** → Choose **Cost budget** → Click **Next**.
3. Configure details:
   - **Budget name:** `TASK-Monthly-Safety-Cap`
   - **Period:** `Monthly`
   - **Budget renewal type:** `Recurring`
   - **Budgeting method:** `Fixed`
   - **Enter your budgeted amount ($):** `5.00` (Five USD) → Click **Next**.
4. Set Alert Threshold 1:
   - **Threshold:** `80%`
   - **Trigger:** `Forecasted` (Alerts you *before* you actually spend the money if current trends indicate you will exceed 80% by month end).
   - **Notification email:** Your email address.
5. Set Alert Threshold 2:
   - Click **Add alert threshold**.
   - **Threshold:** `100%`
   - **Trigger:** `Actual` (Alerts immediately if actual spend exceeds $5.00).
6. Click **Next** → Review configuration → Click **Create budget**.

---

### Task 4: Enable AWS Cost Anomaly Detection
1. In the left navigation pane of Billing & Cost Management, click **Cost Anomaly Detection**.
2. Click **Get started** (or **Create monitor**).
3. Select **Monitor type:** `AWS services (recommended)` (Monitors spending independently across all individual AWS services).
4. Monitor name: `All-AWS-Services-Anomaly-Detector`.
5. Alert frequency: Select **Daily summary** or **Immediate alerts**.
6. Threshold: Set to alerts for anomalies greater than **$2.00**.
7. Enter your email address and click **Create monitor**.

---

## 🧹 Clean-Up Instructions
* Budgets and Cost Anomaly Monitors do not incur any hourly costs in AWS. You may keep them active as permanent guardrails to protect your account during future training sessions.
