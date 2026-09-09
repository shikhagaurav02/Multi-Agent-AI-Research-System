import streamlit as st
from pipeline import run_research_pipeline

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide"
)

# Header
st.title("🔎 Multi-Agent Research System")
st.write(
    "Enter a research topic and let the multi-agent system search, "
    "read, write, and critique a research report."
)

# Topic input
topic = st.text_input(
    "Research Topic",
    placeholder="Example: Impact of AI on the job market"
)

# Run button
if st.button("🚀 Run Research", type="primary"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Multi-agent system is researching your topic..."):
            result = run_research_pipeline(topic.strip())

        if result:
            st.success("Research completed successfully!")

            # Report
            st.subheader("📄 Research Report")
            st.markdown(result.get("report", "No report was generated."))

            # Critic feedback
            st.subheader("🧐 Critic Feedback")
            st.markdown(result.get("feedback", "No critic feedback was generated."))

            # Optional expandable research details
            with st.expander("🔍 View Search Results"):
                st.text(result.get("search_results", "No search results available."))

            with st.expander("📚 View Scraped Content"):
                st.text(result.get("scraped_content", "No scraped content available."))
        else:
            st.error(
                "The pipeline completed, but no result was returned. "
                "Make sure run_research_pipeline() returns the state dictionary."
            )
