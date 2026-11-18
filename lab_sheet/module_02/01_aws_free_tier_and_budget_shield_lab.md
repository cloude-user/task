# Lab Sheet 2.1: AWS Free Tier Account Setup & The Budget Shield
> **Module 2:** AWS Certified Cloud Practitioner  
> **Topic 2.c:** Free Tier, Account Setup & Cost Control Alarms  
> **Target:** Cloud Software Developer Trainees  

---

## 🎯 Lab Objectives
1. Verify personal AWS Free Tier activation and understand monthly free allowances.
2. Secure the AWS Root account with Multi-Factor Authentication (MFA).
3. Create a **Zero-Spend Budget Alert** ($0.01 threshold) to catch unwanted charges immediately.
4. Create a **$5 Monthly Safety Shield** alarm with automated email alerts.

---

## 🛠️ Step-by-Step Instructions

### Step 1: Secure the Root Account with MFA
1. Log in to the [AWS Management Console](https://console.aws.amazon.com/) using your root account email.
2. Click your account name at the top right -> Select **Security credentials**.
3. Under **Multi-factor authentication (MFA)**, click **Assign MFA device**.
4. Device name: `student-mobile-authenticator`.
5. Select **Authenticator app** (Google Authenticator, Microsoft Authenticator, or Authy).
6. Click **Next** -> Show QR code -> Scan the QR code with your mobile app.
7. Enter two consecutive 6-digit codes from your phone app -> Click **Add MFA**.
8. Verify that your root account now displays **MFA status: Active**.

---

### Step 2: Configure the Zero-Spend Budget Shield
1. In the top search bar, type **Budgets** and click on **AWS Budgets**.
2. Click the orange **Create budget** button.
3. Under *Budget setup*, select **Use a template (simplified)**.
4. Select the template: **Zero spend budget**.
5. **Budget name:** `task-zero-spend-shield`.
6. **Email recipients:** Enter your personal email address.
7. Click **Create budget**.
8. *Result:* AWS will notify you the instant your account incurs more than $0.01 in charges!

---

### Step 3: Configure a $5 Monthly Hard Alert
1. On the AWS Budgets dashboard, click **Create budget** again.
2. Select **Customize (advanced)** -> Select **Cost budget** -> Click **Next**.
3. **Budget name:** `task-monthly-5dollar-limit`.
4. **Period:** `Monthly` | **Budget renewal type:** `Recurring budget`.
5. **Budgeting method:** `Fixed` | **Enter your budgeted amount:** `5.00`.
6. Click **Next**.
7. Under *Alert 1*:
   * **Trigger:** Actual spend > 80% (which is $4.00).
   * **Email recipients:** Your email address.
8. Click **Next** -> Click **Create budget**.

---

### ✅ Verification Checklist
- [ ] Root account displays green checkmark for MFA.
- [ ] AWS Budgets dashboard displays 2 active budgets (`task-zero-spend-shield` and `task-monthly-5dollar-limit`).
- [ ] Confirmation email received in inbox.
