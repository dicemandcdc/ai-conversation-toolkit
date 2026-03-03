# FinOps Governance Demo — Azure Configuration

## Resource Group
- **Name:** rg-platform-governance-demo
- **Region:** East US 2
- **Purpose:** Demonstrate cost governance automation chain

## Budget Alerts

| Budget Name | Amount | Threshold Type | Alert Type | Action |
|---|---|---|---|---|
| budget-cost-threshold | $25 | Actual cost | Info | Email notification |
| budget-persistence-decision | $50 | Actual cost | Warning | Email notification |
| budget-value-realization | $80 | Actual cost | Critical | Email + tag resource |
| budget-cost-reset | $100 | Actual cost | Hard Stop | Webhook → Runbook → VM Deallocate |

## Automation Chain
**Trigger:** Budget threshold ($100) exceeded  
**Action Group:** ag-finops-alerts  
**Webhook:** webhook-budget-hardstop  
**Automation Account:** aa-finops-governance  
**Runbook:** Stop-VMFinopsDemo (PowerShell 7.2)  
**Target:** vm-finops-demo (deallocate)  

## Virtual Machine
- **Name:** vm-finops-demo
- **Size:** Standard D2s v3
- **OS:** Ubuntu 24.04 LTS
- **Status:** Deallocated (cost-optimized)
- **Region:** East US 2

## Managed Identity
- **Type:** System-assigned
- **Role:** Virtual Machine Contributor
- **Scope:** rg-platform-governance-demo

## Resource Tags
| Tag | Value |
|---|---|
| environment | demo |
| project | finops-governance |
| owner | diceman |
| cost-center | platform-economics |

## Governance Principle
**"Governance outweighs optimization."**

This demo proves that cost control is not about cutting resources—it's about making cost decisions **observable, testable, and automated**. The $100 hard-stop threshold prevents infrastructure drift and uncontrolled escalation.

## Evidence
- **Screenshots:** `evidence/screenshots/finops-demo/`
- **Runbook:** Confluence (FinOps Governance Knowledge Base)
- **LinkedIn Narrative:** Three-act story (Ubuntu VM → Azure FinOps → future capability)
