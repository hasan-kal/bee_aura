"""
Example Support Tickets for Testing the ERP Triaging System

These are realistic enterprise support tickets organized by priority and category.
Use these to test the triaging system's classification accuracy.
"""

EXAMPLE_TICKETS = {
    "high_priority": [
        {
            "title": "SAP Inventory Module Down - Revenue Impact",
            "ticket": """Our SAP inventory module crashed this morning at 9 AM and we can't process any incoming purchase orders. 
We have $50K in orders waiting to be entered. Our finance team is on hold with vendors. 
This is affecting our daily operations and we're losing revenue. When can we get this fixed?""",
            "expected": {
                "business_category": "Inventory",
                "erp_system": "SAP",
                "issue_type": "Incident",
                "priority": "High"
            }
        },
        {
            "title": "Oracle Payroll Processing Blocked",
            "ticket": """The payroll processing module in Oracle Fusion is not responding. 
We have 500+ employees waiting for salary processing scheduled for today. 
This is critical. HR can't access the system at all. Need immediate assistance.""",
            "expected": {
                "business_category": "HR",
                "erp_system": "Oracle Fusion",
                "issue_type": "Incident",
                "priority": "High"
            }
        },
        {
            "title": "Microsoft Dynamics Financial Close Stuck",
            "ticket": """Microsoft Dynamics financial close process is hung. We're trying to close Q1 books today.
All finance users are blocked. No transactions can be posted. System is completely down for finance team.
This has major implications for our audit schedule.""",
            "expected": {
                "business_category": "Finance",
                "erp_system": "Microsoft Dynamics",
                "issue_type": "Incident",
                "priority": "High"
            }
        }
    ],
    "medium_priority": [
        {
            "title": "Procurement - Slow PO Generation",
            "ticket": """The purchase order generation in SAP is running extremely slow. 
It takes 5-10 minutes to create a single PO now. We used to process them in seconds.
It's slowing down our procurement team but we have a workaround (manual entry). 
Can you investigate the performance issue?""",
            "expected": {
                "business_category": "Procurement",
                "erp_system": "SAP",
                "issue_type": "Service Request",
                "priority": "Medium"
            }
        },
        {
            "title": "Manufacturing - Report Export Issue",
            "ticket": """I can't export production reports from the manufacturing module in Oracle Fusion.
The export button is grayed out for my user role. I'm using CSV workaround but need proper reporting access.
Other team members can export fine.""",
            "expected": {
                "business_category": "Manufacturing",
                "erp_system": "Oracle Fusion",
                "issue_type": "Service Request",
                "priority": "Medium"
            }
        },
        {
            "title": "Sales - Forecast Data Missing",
            "ticket": """Some of the sales forecast data from last month isn't showing in the sales pipeline.
We can see it in the backup reports but not in the main dashboard.
This is affecting our planning but we can work around it for now.""",
            "expected": {
                "business_category": "Sales",
                "erp_system": "Unknown",
                "issue_type": "Incident",
                "priority": "Medium"
            }
        }
    ],
    "low_priority": [
        {
            "title": "Password Reset Request",
            "ticket": """I'm a new employee and need to reset my password for Microsoft Dynamics.
I've never used this system before. Can someone guide me through the process?
I read the documentation but need some clarification.""",
            "expected": {
                "business_category": "IT",
                "erp_system": "Microsoft Dynamics",
                "issue_type": "Information Request",
                "priority": "Low"
            }
        },
        {
            "title": "Feature Suggestion - Better Reporting",
            "ticket": """We would like to request a new feature in our SAP inventory system.
Currently, we need a way to export monthly reconciliation reports in a different format.
Can we schedule a meeting with the development team to discuss this enhancement?""",
            "expected": {
                "business_category": "Inventory",
                "erp_system": "SAP",
                "issue_type": "Change Request",
                "priority": "Low"
            }
        },
        {
            "title": "Training Request - Finance Module",
            "ticket": """Hi, could you point me to documentation or training for the financial reconciliation process 
in Oracle Fusion? I'm trying to understand how to use the monthly reconciliation feature.""",
            "expected": {
                "business_category": "Finance",
                "erp_system": "Oracle Fusion",
                "issue_type": "Information Request",
                "priority": "Low"
            }
        },
        {
            "title": "General ERP Question",
            "ticket": """Where can I find information about the new ERP rollout schedule? 
Is there a training session available for the finance team?""",
            "expected": {
                "business_category": "Finance",
                "erp_system": "Unknown",
                "issue_type": "Information Request",
                "priority": "Low"
            }
        }
    ],
    "edge_cases": [
        {
            "title": "Multiple Systems Mentioned",
            "ticket": """We're integrating SAP with Oracle Fusion for inventory sync.
The data doesn't match between the two systems. 
Finance reconciliation is failing because of the mismatch.
Which system should be classified?""",
            "expected": {
                "business_category": "Inventory",
                "erp_system": "SAP",  # Primary issue system
                "issue_type": "Incident",
                "priority": "High"
            }
        },
        {
            "title": "Vague Technical Issue",
            "ticket": """System not working. Help needed ASAP.""",
            "expected": {
                "business_category": "IT",
                "erp_system": "Unknown",
                "issue_type": "Incident",
                "priority": "Medium"  # Treated as medium due to vagueness
            }
        },
        {
            "title": "Complex Business Process",
            "ticket": """When processing a three-way match in accounts payable with Oracle Fusion, 
the system is rejecting valid invoices that don't have a corresponding purchase order, 
even though we have manual approval. The tolerance rules seem misconfigured. 
Can someone help troubleshoot the three-way match settings?""",
            "expected": {
                "business_category": "Finance",
                "erp_system": "Oracle Fusion",
                "issue_type": "Service Request",
                "priority": "Medium"
            }
        }
    ]
}


# Test scenarios for manual validation
TEST_SCENARIOS = [
    {
        "name": "Crisis Management",
        "tickets": EXAMPLE_TICKETS["high_priority"],
        "expected_accuracy": 0.95
    },
    {
        "name": "Normal Operations",
        "tickets": EXAMPLE_TICKETS["medium_priority"],
        "expected_accuracy": 0.90
    },
    {
        "name": "Support & Information",
        "tickets": EXAMPLE_TICKETS["low_priority"],
        "expected_accuracy": 0.85
    },
    {
        "name": "Edge Cases",
        "tickets": EXAMPLE_TICKETS["edge_cases"],
        "expected_accuracy": 0.80
    }
]


def get_random_high_priority_ticket():
    """Get a high priority ticket for quick testing."""
    return EXAMPLE_TICKETS["high_priority"][0]["ticket"]


def get_random_low_priority_ticket():
    """Get a low priority ticket for quick testing."""
    return EXAMPLE_TICKETS["low_priority"][0]["ticket"]


if __name__ == "__main__":
    # Print all tickets for reference
    import json
    
    print("=" * 80)
    print("ERP TICKET TRIAGING SYSTEM - TEST TICKETS")
    print("=" * 80)
    
    for category, tickets in EXAMPLE_TICKETS.items():
        print(f"\n{category.upper().replace('_', ' ')}")
        print("-" * 80)
        for i, item in enumerate(tickets, 1):
            print(f"\n{i}. {item['title']}")
            print(f"   Ticket: {item['ticket'][:100]}...")
            if 'expected' in item:
                print(f"   Expected: {json.dumps(item['expected'], indent=12)}")
