import streamlit as st
import requests

st.title("CAI MCP POC")

tools_list_url = "http://127.0.0.1:8000/tool/list"
base_tool_url = "http://127.0.0.1:8000/tool"
llm_agent_url = "http://127.0.0.1:8000/llm_agent"


if "tool_data" not in st.session_state:
    st.session_state.tool_data = None
if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = False
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = None
if "tool_inputs" not in st.session_state:
    st.session_state.tool_inputs = {}
if "response" not in st.session_state:
    st.session_state.response = None
if "llm_active" not in st.session_state:
    st.session_state.llm_active = False
if "llm_prompt" not in st.session_state:
    st.session_state.llm_prompt = ""
if "llm_response" not in st.session_state:
    st.session_state.llm_response = None


def fetch_tools():
    try:
        response = requests.get(tools_list_url, timeout=5)
        response.raise_for_status()
        st.session_state.tool_data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch tools list: {e}")
        st.session_state.tool_data = None


def show_input_dialog(tool):
    st.session_state.show_dialog = True
    st.session_state.selected_tool = tool
    st.session_state.tool_inputs = {key: "" for key in tool["schema"].get("properties", {}).keys()}
    st.session_state.response = None


def submit_tool():
    tool = st.session_state.selected_tool
    url = f"{base_tool_url}/{tool['name']}"
    payload = st.session_state.tool_inputs
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        st.session_state.response = response.json()
    except requests.exceptions.RequestException as e:
        st.session_state.response = {"error": str(e)}


def submit_llm_prompt():
    payload = {"prompt": st.session_state.llm_prompt}
    try:
        response = requests.post(llm_agent_url, json=payload, timeout=10)
        response.raise_for_status()
        st.session_state.llm_response = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"LLM Agent call failed: {e}")
        st.session_state.llm_response = None


# Top row with two buttons horizontally
col1, col2 = st.columns(2)

with col1:
    if st.button("Lists"):
        fetch_tools()
        st.session_state.llm_active = False  # Hide LLM UI
        st.session_state.show_dialog = False  # Hide any open tool input dialogs

with col2:
    if st.button("Ask LLM"):
        st.session_state.llm_active = True
        st.session_state.tool_data = None  # Hide tools list
        st.session_state.show_dialog = False  # Hide any open tool input dialogs
        st.session_state.llm_prompt = ""
        st.session_state.llm_response = None


# Main content with tools on left, form and response on right OR LLM UI
col_left, col_right = st.columns([1, 3])

with col_left:
    if st.session_state.tool_data:
        tools = st.session_state.tool_data.get("Available tools on this MCP server", [])
        st.markdown("### Available Tools")
        for tool in tools:
            if st.button(tool["name"], key=f"tool_button_{tool['name']}"):
                show_input_dialog(tool)
                st.session_state.llm_active = False  # Hide LLM UI when choosing tools

with col_right:
    if st.session_state.llm_active:
        st.markdown("### LLM Agent Interaction")
        st.caption("Enter your prompt below and submit to get LLM agent response.")

        st.session_state.llm_prompt = st.text_area(
            "Your Prompt", st.session_state.llm_prompt, height=120
        )

        col_submit, col_blank = st.columns([1, 4])
        with col_submit:
            if st.button("Submit Prompt"):
                if st.session_state.llm_prompt.strip():
                    submit_llm_prompt()
                else:
                    st.warning("Please enter a prompt before submitting.")

        st.markdown("---")
        st.markdown("### Response")
        if st.session_state.llm_response:
            st.json(st.session_state.llm_response)
        else:
            st.info("Response will be shown here after submission.")

    elif st.session_state.show_dialog and st.session_state.selected_tool:
        tool = st.session_state.selected_tool
        st.markdown(f"### Input for Tool: {tool['name']}")
        props = tool["schema"].get("properties", {})

        st.markdown(f"**Description:** {tool['description'] or 'No description available.'}")

        for key, detail in props.items():
            typ = detail.get("type", "string")
            label = detail.get("title", key)
            if typ == "number":
                val = st.text_input(f"{label} ({typ})", st.session_state.tool_inputs.get(key, ""))
                try:
                    val = float(val) if val != "" else None
                except Exception:
                    val = st.session_state.tool_inputs.get(key, "")
                st.session_state.tool_inputs[key] = val
            else:
                st.session_state.tool_inputs[key] = st.text_input(f"{label} ({typ})", st.session_state.tool_inputs.get(key, ""))

        if st.button("Submit"):
            submit_tool()

        if st.session_state.response:
            st.markdown("### Response")
            st.json(st.session_state.response)
