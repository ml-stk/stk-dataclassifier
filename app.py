import streamlit as st
import asyncio
from scanning-engine.regex_worker import RegexClassifier

# Initialize classifier
classifier = RegexClassifier()

st.set_page_config(
    page_title="STK DataClassifier - POC",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ STK DataClassifier (POC)")
st.markdown("Run enterprise-grade pattern matching locally without requiring Docker or a VM.")

# Input fields
file_id_input = st.text_input("File ID / Reference", value="file_test_001")
text_input = st.text_area("Paste document text or content to classify:", height=150, placeholder="Enter text containing sensitive patterns (e.g., SSN, credit cards, or 'strictly confidential')...")

manual_override = st.selectbox(
    "Manual Override Tier (Optional)",
    options=["None", "Public", "Internal", "Confidential", "Restricted"],
    index=0
)

if st.button("Classify Content", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text content to scan.")
    else:
        override_val = None if manual_override == "None" else manual_override
        
        # Run classification
        with st.spinner("Analyzing content..."):
            result = asyncio.run(
                classifier.classify(
                    file_id=file_id_input,
                    text_content=text_input,
                    manual_override=override_val
                )
            )
        
        st.success("Classification Complete!")
        
        # Display Results in Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Assigned Tier", result.assigned_tier)
        col2.metric("Confidence Score", f"{result.confidence_score * 100:.0f}%")
        col3.metric("Engine Used", result.engine_used)
        
        st.subheader("Matched Rules / Triggers")
        if result.matched_rules:
            for rule in result.matched_rules:
                st.code(rule, language="text")
        else:
            st.info("No sensitive pattern rules matched. Default tier applied.")
