# Quick Start Guide - ERP Ticket Triaging System

## ⚡ 30-Second Setup

### 1. Install Dependencies
```bash
cd /Users/hasan/bee_aura
pip install streamlit requests
```

### 2. Get Your API Key
- Visit: https://platform.openai.com/api-keys
- Create a new API key
- Copy the key (starts with `sk-`)

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Use the App
- App opens at `http://localhost:8501`
- Paste your API key in the sidebar
- Click "Use Example Ticket" checkbox
- Click "🚀 Triage Ticket"
- View results!

---

## 📋 Example Tickets to Try

### Example 1: High Priority (System Down)
```
Our SAP inventory module crashed this morning at 9 AM and we can't process any 
incoming purchase orders. We have $50K in orders waiting to be entered. Our finance 
team is on hold with vendors. This is affecting our daily operations.
```
**Expected**: Inventory, SAP, Incident, High Priority

---

### Example 2: Medium Priority (Slow Performance)
```
The purchase order generation in SAP is running extremely slow. 
It takes 5-10 minutes to create a single PO now. We used to process them in seconds.
It's slowing down our procurement team but we have a workaround.
```
**Expected**: Procurement, SAP, Service Request, Medium Priority

---

### Example 3: Low Priority (Information Request)
```
I'm a new employee and need to reset my password for Microsoft Dynamics.
I've never used this system before. Can someone guide me through the process?
```
**Expected**: IT, Microsoft Dynamics, Information Request, Low Priority

---

## 🔑 API Key Setup Options

### Option A: Session-Based (Easiest for Testing)
1. Run `streamlit run app.py`
2. Paste API key in the sidebar input
3. Key only works for current session

### Option B: Environment Variable
```bash
export OPENAI_API_KEY="sk-your-key-here"
streamlit run app.py
```

### Option C: Streamlit Secrets (Best for Deployment)
1. Create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   ```
2. Run `streamlit run app.py`

---

## ✅ Verify Everything Works

1. **Test with Example Ticket**
   - Check "Use Example Ticket" box
   - Click "🚀 Triage Ticket"
   - Should see results in ~5 seconds

2. **Test with Custom Ticket**
   - Write your own ticket
   - Click "🚀 Triage Ticket"
   - Verify classification makes sense

3. **View Raw JSON**
   - Expand "View Raw JSON" section
   - See structured output

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not configured" | Paste API key in sidebar or set environment variable |
| "API Error (401)" | Check API key is valid and hasn't expired |
| "API call timed out" | Check internet connection, try again |
| Nothing happens | Check browser console for errors (F12) |
| Very slow response | Normal - API calls take 3-5 seconds |

---

## 📚 Full Documentation

See `README.md` for:
- Complete system architecture
- All classification options
- Cost analysis
- Deployment considerations
- Known limitations
- Development tips

---

## 🎯 What to Expect

**Input**: Free-text support ticket (any length)

**Processing**: 
- LLM analyzes ticket with structured prompt
- Enforces JSON output format
- Validates all fields
- ~3-5 seconds per ticket

**Output**:
- Business Category (7 options)
- ERP System (4 options)
- Issue Type (4 options)
- Priority Level (High/Medium/Low)
- Professional first-level response
- Timestamp

---

## 💡 Tips

- **Clearer tickets = Better results**: Well-written tickets classify more accurately
- **Specific details help**: Mention system names, impact, users affected
- **Test patterns**: Try high/medium/low priority examples to see differences
- **Check raw JSON**: Expand the JSON output to see the structured data
- **Monitor costs**: Each classification costs ~$0.0005 (very cheap)

---

## 🚀 Next Steps

1. **Test the system** with provided examples
2. **Try custom tickets** from your environment
3. **Check accuracy** of classifications
4. **Review limitations** in README
5. **Plan integration** with your ticketing system
6. **Customize prompt** for your specific ERP environment

---

Happy triaging! 🎯
