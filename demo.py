#!/usr/bin/env python3
"""
Demo & Test Script for ERP Ticket Triaging System

This script allows you to test the triaging system without the Streamlit UI.
Useful for:
- Testing LLM responses
- Validating JSON parsing
- Checking classification accuracy
- Understanding the system flow

Usage:
    python3 demo.py
"""

import os
import sys
import json
from typing import Optional
from example_tickets import EXAMPLE_TICKETS

# Add current directory to path so we can import app functions
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def get_test_api_key() -> Optional[str]:
    """Get API key from environment or user input."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print("✓ Found API key in environment")
        return api_key
    
    print("⚠️  OPENAI_API_KEY environment variable not found")
    print("   Get your key from: https://platform.openai.com/api-keys")
    api_key = input("\nEnter your OpenAI API key (or press Enter to skip): ").strip()
    return api_key if api_key else None


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_ticket_info(ticket_data: dict):
    """Print formatted ticket information."""
    print(f"Title: {ticket_data['title']}")
    print(f"\nTicket Content:\n{ticket_data['ticket']}")
    if 'expected' in ticket_data:
        print(f"\nExpected Classification:")
        for key, value in ticket_data['expected'].items():
            print(f"  - {key}: {value}")


def demo_json_parsing():
    """Demo: Show JSON parsing with different formats."""
    print_section("DEMO 1: JSON Parsing")
    
    print("The system can parse JSON in multiple formats:\n")
    
    # Test cases
    test_cases = [
        {
            "name": "Pure JSON",
            "input": '{"priority": "High", "category": "Finance"}'
        },
        {
            "name": "JSON in Markdown",
            "input": '```json\n{"priority": "High", "category": "Finance"}\n```'
        },
        {
            "name": "JSON with markdown fence (no lang)",
            "input": '```\n{"priority": "High", "category": "Finance"}\n```'
        }
    ]
    
    # We'll manually show this without actually importing the function
    for test in test_cases:
        print(f"Input format: {test['name']}")
        print(f"  Raw: {test['input'][:50]}...")
        try:
            import re
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', test['input'], re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(1))
            else:
                parsed = json.loads(test['input'])
            print(f"  ✓ Parsed successfully: {parsed}")
        except Exception as e:
            print(f"  ✗ Parse failed: {e}")
        print()


def demo_validation():
    """Demo: Show validation of classification results."""
    print_section("DEMO 2: Result Validation")
    
    VALID_CATEGORIES = ["Finance", "Inventory", "Procurement", "HR", "Sales", "Manufacturing", "IT"]
    VALID_SYSTEMS = ["SAP", "Oracle Fusion", "Microsoft Dynamics", "Unknown"]
    VALID_TYPES = ["Incident", "Service Request", "Change Request", "Information Request"]
    VALID_PRIORITIES = ["High", "Medium", "Low"]
    
    print("The system validates results against allowed values:\n")
    
    test_results = [
        {
            "name": "Valid Result",
            "result": {
                "business_category": "Finance",
                "erp_system": "SAP",
                "issue_type": "Incident",
                "priority": "High",
                "first_level_response": "Thank you for reporting. We understand..."
            }
        },
        {
            "name": "Invalid Category (typo)",
            "result": {
                "business_category": "Finanace",  # Typo
                "erp_system": "SAP",
                "issue_type": "Incident",
                "priority": "High",
                "first_level_response": "Thank you for reporting..."
            }
        },
        {
            "name": "Missing Field",
            "result": {
                "business_category": "Finance",
                "erp_system": "SAP",
                # Missing issue_type and priority
                "first_level_response": "Thank you for reporting..."
            }
        },
        {
            "name": "Empty Response",
            "result": {
                "business_category": "Finance",
                "erp_system": "SAP",
                "issue_type": "Incident",
                "priority": "High",
                "first_level_response": ""  # Empty
            }
        }
    ]
    
    for test in test_results:
        print(f"Validating: {test['name']}")
        result = test['result']
        
        # Check all required fields
        required_fields = ["business_category", "erp_system", "issue_type", "priority", "first_level_response"]
        all_present = all(field in result for field in required_fields)
        print(f"  Fields present: {'✓' if all_present else '✗'}")
        
        if all_present:
            # Validate values
            is_valid_category = result["business_category"] in VALID_CATEGORIES
            is_valid_system = result["erp_system"] in VALID_SYSTEMS
            is_valid_type = result["issue_type"] in VALID_TYPES
            is_valid_priority = result["priority"] in VALID_PRIORITIES
            has_response = result["first_level_response"].strip() != ""
            
            print(f"  Category valid: {'✓' if is_valid_category else '✗'}")
            print(f"  System valid: {'✓' if is_valid_system else '✗'}")
            print(f"  Type valid: {'✓' if is_valid_type else '✗'}")
            print(f"  Priority valid: {'✓' if is_valid_priority else '✗'}")
            print(f"  Response non-empty: {'✓' if has_response else '✗'}")
            
            overall = all_present and is_valid_category and is_valid_system and is_valid_type and is_valid_priority and has_response
            print(f"  Overall: {'✓ PASS' if overall else '✗ FAIL'}")
        
        print()


def demo_classification_scenarios():
    """Demo: Show example tickets from different scenarios."""
    print_section("DEMO 3: Classification Scenarios")
    
    print("Here are example tickets from different priority levels:\n")
    
    scenarios = [
        ("🔴 High Priority (System Down)", EXAMPLE_TICKETS["high_priority"]),
        ("🟡 Medium Priority (Functional Issue)", EXAMPLE_TICKETS["medium_priority"]),
        ("🟢 Low Priority (Information)", EXAMPLE_TICKETS["low_priority"])
    ]
    
    for scenario_name, tickets in scenarios:
        print(f"\n{scenario_name}")
        print("-" * 80)
        for i, ticket in enumerate(tickets[:1], 1):  # Show first ticket of each category
            print(f"\nExample {i}: {ticket['title']}")
            print(f"Ticket: {ticket['ticket'][:150]}...")
            if 'expected' in ticket:
                print(f"Expected:")
                print(f"  • Category: {ticket['expected']['business_category']}")
                print(f"  • System: {ticket['expected']['erp_system']}")
                print(f"  • Type: {ticket['expected']['issue_type']}")
                print(f"  • Priority: {ticket['expected']['priority']}")


def demo_with_api(api_key: Optional[str]):
    """Demo: Test actual API call if API key provided."""
    if not api_key:
        print_section("API Testing (SKIPPED)")
        print("API key not provided. To test actual API calls, run:")
        print("  OPENAI_API_KEY='sk-...' python3 demo.py")
        return
    
    print_section("DEMO 4: Live API Test")
    
    # Import here to avoid import errors if OpenAI not installed
    try:
        import requests
        from example_tickets import EXAMPLE_TICKETS
    except ImportError:
        print("✗ Required packages not installed")
        print("  Run: pip install requests")
        return
    
    # Test with a simple high-priority ticket
    test_ticket = EXAMPLE_TICKETS["high_priority"][0]["ticket"]
    
    print(f"Testing with: {EXAMPLE_TICKETS['high_priority'][0]['title']}")
    print(f"Ticket: {test_ticket[:100]}...\n")
    
    print("🔄 Calling OpenAI API...")
    
    # Construct prompt
    system_prompt = """You are an expert ERP support specialist.
Analyze tickets and classify them. Respond ONLY with valid JSON.
{
    "business_category": "Finance|Inventory|Procurement|HR|Sales|Manufacturing|IT",
    "erp_system": "SAP|Oracle Fusion|Microsoft Dynamics|Unknown",
    "issue_type": "Incident|Service Request|Change Request|Information Request",
    "priority": "High|Medium|Low",
    "first_level_response": "2-3 sentence professional acknowledgement"
}"""
    
    user_prompt = f"Triage this ticket:\n\n{test_ticket}"
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            llm_response = response.json()["choices"][0]["message"]["content"]
            print("\n✓ API Response Received:")
            print(llm_response)
            
            # Try to parse
            import re
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', llm_response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(1))
            else:
                parsed = json.loads(llm_response)
            
            print("\n✓ JSON Parsed Successfully:")
            print(json.dumps(parsed, indent=2))
        else:
            print(f"\n✗ API Error: {response.status_code}")
            print(response.json())
    
    except requests.exceptions.Timeout:
        print("\n✗ API call timed out")
    except Exception as e:
        print(f"\n✗ Error: {e}")


def main():
    """Run all demos."""
    print("\n" + "=" * 80)
    print(" ERP TICKET TRIAGING SYSTEM - DEMO & TEST")
    print("=" * 80)
    
    # Run demos
    demo_json_parsing()
    demo_validation()
    demo_classification_scenarios()
    
    # Optional: Run API test if key is provided
    api_key = get_test_api_key()
    demo_with_api(api_key)
    
    # Summary
    print_section("Demo Complete")
    print("Next steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Run the Streamlit app: streamlit run app.py")
    print("  3. Paste your API key in the sidebar")
    print("  4. Click 'Use Example Ticket' and test")
    print("\nFor more information, see:")
    print("  - README.md: Full documentation")
    print("  - QUICKSTART.md: 30-second setup guide")
    print("  - ARCHITECTURE.md: Design details\n")


if __name__ == "__main__":
    main()
