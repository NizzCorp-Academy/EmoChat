import streamlit as st
from evaluation.evaluation_engine import EvaluationEngine
from db.connector import get_db

st.set_page_config(
    page_title="Evaluation Dashboard",
    page_icon="📊",
)

def main():
    st.title("📊 Evaluation Dashboard")

    # Check for user authentication
    if 'user' not in st.session_state or not st.session_state.user:
        st.warning("Please log in to view the evaluation dashboard.")
        st.stop()

    # Initialize Evaluation Engine
    db_session = next(get_db())
    eval_engine = EvaluationEngine(db_session)
    report = eval_engine.run_evaluation()

    st.header("Key Performance Indicators")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Avg. Feedback Rating",
            value=report['average_feedback_rating'],
            help="Average user feedback rating on a scale of 1 to 5."
        )

    with col2:
        st.metric(
            label="Total Interactions",
            value=report['total_interactions'],
            help="Total number of conversations logged."
        )

    with col3:
        st.metric(
            label="Guardrails Trigger Rate",
            value=f"{report['guardrail_trigger_rate']}",
            help="Percentage of interactions that triggered a safety guardrail.",
            delta=f"{report['guardrail_triggered_count']} flagged",
            delta_color="inverse"
        )

    st.markdown("--- ")
    st.header("Further Analysis")
    st.info("This is a foundational dashboard. Future enhancements could include:\n- Feedback analysis over time.\n- Topic modeling on user prompts.\n- Analysis of conversations that trigger guardrails.")

if __name__ == "__main__":
    main()
