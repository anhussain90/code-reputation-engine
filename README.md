# Code Reputation Engine

Automated collection of static code analysis feedback from GitHub Actions into structured CSV reports.  
This repository powers a reputation and quality scoring system by aggregating findings from CodeQL, linters, and other static analysis tools.

---

## 🎯 Purpose

Modern development teams run multiple static analysis tools in GitHub Actions.  
This project provides a **standardized, automated way** to collect those results and store them as machine-readable reports for:

- Code quality dashboards  
- Developer reputation scoring  
- Security posture tracking  
- Trend analysis over time  

---

## ⚙️ How It Works

1. A Static Analysis workflow runs (CodeQL, ESLint, etc.)
2. An external system triggers the collector workflow using `workflow_dispatch`
3. The collector:
   - Locates the latest analysis workflow run
   - Fetches all check-run annotations via GitHub API
   - Writes results into a CSV report
   - Commits the report back into this repository

---

## 📦 Output Format

Reports are stored in:

