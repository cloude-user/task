# Lab Sheet 2.2: AWS IAM Users, Groups & Least-Privilege Policies
> **Module 2:** AWS Certified Cloud Practitioner  
> **Topic 2.b:** Security, Identity & Compliance (IAM)  
> **Target:** Cloud Software Developer Trainees  

---

## 🎯 Lab Objectives
1. Create a dedicated administrative IAM user and cease using the root user for daily tasks.
2. Create an **IAM User Group** with tailored permissions.
3. Understand and attach AWS Managed Policies.
4. Set up an account password policy to enforce enterprise security standards.

---

## 🛠️ Step-by-Step Instructions

### Step 1: Create an IAM User Group
1. Open the [AWS Management Console](https://console.aws.amazon.com/) and navigate to **IAM**.
2. In the left navigation pane, click **User groups** -> Click **Create group**.
3. **User group name:** `CloudDevelopers`.
4. Under *Attach permissions policies*, search for and check:
   * `AmazonEC2FullAccess`
   * `AmazonS3FullAccess`
   * `AmazonVPCFullAccess`
5. Click **Create user group**.

---

### Step 2: Create a Dedicated Daily IAM User
1. In the left navigation pane, click **Users** -> Click **Create user**.
2. **User name:** `developer-user`.
3. Check the box: **Provide user access to the AWS Management Console**.
4. Select: **I want to create an IAM-user**.
5. Select: **Custom password** -> Enter a strong password.
6. Uncheck *Users must create a new password at next sign-in* for personal lab convenience.
7. Click **Next**.
8. Under *Set permissions*, select **Add user to group** -> Check `CloudDevelopers`.
9. Click **Next** -> Click **Create user**.
10. Copy and bookmark your unique **Console sign-in URL** (e.g., `https://<account-id>.signin.aws.amazon.com/console`).

---

### Step 3: Test Sign-In as the IAM User
1. Open a new Incognito / Private browsing window.
2. Navigate to your custom Console sign-in URL.
3. Enter your 12-digit Account ID, Username (`developer-user`), and Password.
4. Verify you can access EC2, S3, and VPC consoles.
5. Try opening **Billing and Cost Management** or **IAM**: Notice that access is denied because your user group only has permissions for EC2, S3, and VPC!

---

### ✅ Verification Checklist
- [ ] Root account is logged out.
- [ ] IAM User `developer-user` created and assigned to `CloudDevelopers` group.
- [ ] Successfully logged in via IAM Console sign-in URL.
