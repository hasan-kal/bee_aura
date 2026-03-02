#!/usr/bin/env python3
"""
AI-Powered ERP Ticket Triaging System
A Streamlit-based prototype that uses LLMs to automatically classify and triage support tickets.

Architecture:
1. User inputs a free-text ERP support ticket
2. System sends ticket to LLM with structured prompt (enforces JSON output)
3. LLM classifies ticket across 5 dimensions
4. System parses and validates JSON response
5. Results displayed in organized layout with professional formatting
"""

import streamlit as st
import json
import re
from typing import Dict, Optional, Tuple
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="ERP Ticket Triaging System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CONFIGURATION
# ============================================================================

# API Configuration - supports OpenAI-compatible endpoints
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
MODEL_NAME = "gpt-4o-mini"  # Can use gpt-3.5-turbo for cost efficiency
TIMEOUT_SECONDS = 30

# Classification options
VALID_BUSINESS_CATEGORIES = [
    "Finance", "Inventory", "Procurement", "HR", "Sales", "Manufacturing", "IT"
]
VALID_ERP_SYSTEMS = ["SAP", "Oracle Fusion", "Microsoft Dynamics", "Unknown"]
VALID_ISSUE_TYPES = ["Incident", "Service Request", "Change Request", "Information Request"]
VALID_PRIORITIES = ["High", "Medium", "Low"]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_api_key() -> Optional[str]:
    """Retrieve API key from secrets or environment."""
    # Try Streamlit secrets first (for deployed apps)
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except:
        # Secrets file may not exist, which is fine
        pass
    
    # Fall back to session state or user input
    if "api_key" in st.session_state and st.session_state.api_key:
        return st.session_state.api_key
    
    return None


def validate_json_response(json_str: str) -> Tuple[bool, Optional[Dict]]:
    """
    Validate and parse JSON response from LLM.
    
    Returns:
        Tuple of (is_valid, parsed_dict)
    """
    try:
        # Try to extract JSON if LLM wrapped it in markdown
        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', json_str, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        
        parsed = json.loads(json_str)
        return True, parsed
    except json.JSONDecodeError as e:
        return False, None


def validate_triaging_result(result: Dict) -> Tuple[bool, str]:
    """
    Validate that triaging result contains all required fields with valid values.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = {
        "business_category": VALID_BUSINESS_CATEGORIES,
        "erp_system": VALID_ERP_SYSTEMS,
        "issue_type": VALID_ISSUE_TYPES,
        "priority": VALID_PRIORITIES,
        "first_level_response": None  # String field, any value acceptable
    }
    
    # Check all required fields exist
    for field, valid_values in required_fields.items():
        if field not in result:
            return False, f"Missing required field: {field}"
        
        # Validate against allowed values
        if valid_values is not None:
            if result[field] not in valid_values:
                return False, f"Invalid {field}: {result[field]}. Must be one of: {valid_values}"
    
    # Validate response is non-empty string
    if not isinstance(result["first_level_response"], str) or len(result["first_level_response"].strip()) == 0:
        return False, "First-level response cannot be empty"
    
    return True, ""


def call_llm_for_triaging(ticket_text: str, api_key: str) -> Tuple[bool, Optional[Dict], str]:
    """
    Call LLM API to triage the ticket.
    
    Returns:
        Tuple of (success, triaging_result, message)
    """
    # Construct the system prompt that enforces JSON output
    system_prompt = """You are an expert ERP support specialist tasked with triaging support tickets.
    
Analyze each ticket and classify it across these dimensions:

1. Business Category: Choose from [Finance, Inventory, Procurement, HR, Sales, Manufacturing, IT]
2. ERP System: Identify the system mentioned [SAP, Oracle Fusion, Microsoft Dynamics, Unknown]
3. Issue Type: Classify as [Incident, Service Request, Change Request, Information Request]
   - Incident: System is broken or not working
   - Service Request: User needs help with existing functionality
   - Change Request: User wants new feature or modification
   - Information Request: User is asking for information/documentation
4. Priority: Assess urgency [High, Medium, Low]
   - High: System down, financial impact, critical business process blocked
   - Medium: Functional issue affecting productivity but workaround exists
   - Low: General inquiry, minor inconvenience, documentation question
5. First-Level Response: Write a 2-3 sentence professional acknowledgement that:
   - Thanks the user for reporting
   - Confirms what you understood about their issue
   - Provides next steps or indicates routing to specialist

IMPORTANT: You must respond ONLY with valid JSON (no markdown, no extra text).
Use this exact structure:
{
    "business_category": "string from allowed list",
    "erp_system": "string from allowed list",
    "issue_type": "string from allowed list",
    "priority": "string from allowed list",
    "first_level_response": "string with acknowledgement message"
}"""

    user_prompt = f"Please triage this support ticket:\n\n{ticket_text}"
    
    try:
        # Prepare request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        # Make API call
        response = requests.post(
            API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=TIMEOUT_SECONDS
        )
        
        # Handle HTTP errors
        if response.status_code != 200:
            error_detail = response.json().get("error", {}).get("message", "Unknown error")
            return False, None, f"API Error ({response.status_code}): {error_detail}"
        
        # Extract LLM response
        llm_response = response.json()["choices"][0]["message"]["content"]
        
        # Parse JSON response
        is_valid, parsed_result = validate_json_response(llm_response)
        if not is_valid:
            return False, None, f"Failed to parse LLM response as JSON. Response: {llm_response[:200]}"
        
        # Validate triaging result
        is_valid, error_msg = validate_triaging_result(parsed_result)
        if not is_valid:
            return False, None, f"Invalid triaging result: {error_msg}. Response: {parsed_result}"
        
        return True, parsed_result, "Successfully triaged ticket"
        
    except requests.exceptions.Timeout:
        return False, None, f"API call timed out (>{TIMEOUT_SECONDS}s). Please try again."
    except requests.exceptions.ConnectionError:
        return False, None, "Connection error. Please check your internet connection and API endpoint."
    except requests.exceptions.RequestException as e:
        return False, None, f"Request error: {str(e)}"
    except KeyError as e:
        return False, None, f"Unexpected API response format: {str(e)}"


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_header():
    """Render page header and description."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🎯 ERP Ticket Triaging System")
        st.markdown("**Automated AI-powered classification and routing for support tickets**")
    with col2:
        st.metric("System Status", "Active", "Ready")
    
    st.divider()


def render_api_key_section():
    """Render API key input section."""
    with st.sidebar:
        st.subheader("⚙️ Configuration")
        st.markdown("---")
        
        api_key = get_api_key()
        
        if not api_key:
            st.warning("⚠️ API key not configured")
            api_key_input = st.text_input(
                "Enter OpenAI API Key",
                type="password",
                help="Your API key is not stored and only used for this session"
            )
            if api_key_input:
                st.session_state.api_key = api_key_input
                api_key = api_key_input
        else:
            st.success("✓ API key configured")
            if st.button("Clear API Key"):
                st.session_state.api_key = None
                st.rerun()
        
        st.markdown("---")
        st.markdown("**Model Configuration**")
        st.markdown(f"- **Endpoint**: {API_ENDPOINT}")
        st.markdown(f"- **Model**: {MODEL_NAME}")
        
        return api_key


def render_input_section() -> str:
    """Render ticket input section. Returns ticket text."""
    st.subheader("📝 Support Ticket")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        use_example = st.checkbox("Use Example Ticket", value=False)
    
    if use_example:
        example_ticket = """Our SAP inventory module crashed this morning at 9 AM and we can't process any incoming purchase orders. 
        We have $50K in orders waiting to be entered. Our finance team is on hold with vendors. 
        This is affecting our daily operations. When can we get this fixed?"""
        ticket_text = st.text_area(
            "Ticket Content",
            value=example_ticket,
            height=150,
            key="ticket_input"
        )
    else:
        ticket_text = st.text_area(
            "Paste your support ticket here",
            height=150,
            placeholder="Describe your ERP issue...",
            key="ticket_input"
        )
    
    return ticket_text.strip()


def render_results_section(result: Dict):
    """Render triaging results in organized layout."""
    st.subheader("✅ Triaging Results")
    
    # Create a metrics row for primary classifications
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Business Category", result["business_category"])
    
    with col2:
        st.metric("ERP System", result["erp_system"])
    
    with col3:
        st.metric("Issue Type", result["issue_type"])
    
    with col4:
        # Color-code priority
        priority = result["priority"]
        color = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
        st.metric("Priority", f"{color} {priority}")
    
    st.divider()
    
    # Display first-level response
    st.markdown("**First-Level Response**")
    st.info(result["first_level_response"])
    
    # Timestamp
    st.caption(f"_Triaged at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_")


def render_sidebar_info():
    """Render information in sidebar."""
    with st.sidebar:
        st.markdown("---")
        with st.expander("📚 About This System"):
            st.markdown("""
This system demonstrates how AI/LLMs can automate support ticket triaging:

**How it works:**
1. You paste a free-text support ticket
2. The LLM analyzes it using a structured prompt
3. Results are classified across 5 dimensions
4. A professional acknowledgement is generated

**Benefits:**
- Reduces manual triaging time
- Consistent classification criteria
- Faster routing to specialists
- 24/7 first-level response
            """)
        
        with st.expander("🔧 Example Tickets"):
            st.markdown("""
**Example 1 (High Priority):**
"SAP crashed. Orders piling up. Revenue impact."

**Example 2 (Medium Priority):**
"Can't export reports in Finance module. Using workaround."

**Example 3 (Low Priority):**
"How do I reset my password in Oracle Fusion?"
            """)
        
        with st.expander("⚠️ Known Limitations"):
            st.markdown("""
- LLM may misclassify complex multi-issue tickets
- Requires clear, well-written tickets for best accuracy
- No integration with actual ticketing system (proof of concept)
- Cannot handle images or attachments
- May take 3-5 seconds per classification
            """)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application logic."""
    render_header()
    
    # Get API key
    api_key = render_api_key_section()
    
    # Main content area
    st.markdown("")
    
    # Input section
    ticket_text = render_input_section()
    
    # Process button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        process_button = st.button("🚀 Triage Ticket", type="primary", use_container_width=True)
    
    st.markdown("")
    
    # Handle triaging
    if process_button:
        # Validate inputs
        if not api_key:
            st.error("❌ API key is required. Please configure it in the sidebar.")
            return
        
        if not ticket_text or len(ticket_text) < 10:
            st.error("❌ Please enter a ticket with at least 10 characters.")
            return
        
        # Call LLM
        with st.spinner("🔄 Analyzing ticket with AI..."):
            success, result, message = call_llm_for_triaging(ticket_text, api_key)
        
        if success:
            st.success("✅ Ticket triaged successfully!")
            render_results_section(result)
            
            # Show raw JSON for transparency
            with st.expander("📊 View Raw JSON"):
                st.json(result)
        else:
            st.error(f"❌ Triaging failed: {message}")
            st.markdown("**Troubleshooting:**")
            st.markdown("""
- Verify your API key is valid
- Check your OpenAI account has available credits
- Ensure your internet connection is stable
- Try again in a few seconds
            """)
    
    # Sidebar info
    render_sidebar_info()


if __name__ == "__main__":
    main()
