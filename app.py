import streamlit as st

from data_security.pipeline import run_security_analysis
from data_security.api.public_interface import ingest_event
from data_security.detectors.basic_threat_detector import detect_threats
from data_security.repository.threat_repository import ThreatRepository


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sentinel-AI",
    page_icon="🛡️",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ Sentinel-AI")
st.subheader("Windows Security Monitoring Dashboard")

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Analysis Settings")

log_name = st.sidebar.selectbox(
    "Windows Event Log",
    ["System", "Application"],
)

limit = st.sidebar.slider(
    "Number of events",
    min_value=5,
    max_value=50,
    value=20,
)

scope = st.sidebar.text_input(
    "Assessment Scope",
    "TARUN",
)


# ============================================================
# SECURITY OVERVIEW
# ============================================================

st.header("📊 Security Overview")

try:

    repository = ThreatRepository()

    overview_threats = repository.query_threats(
        limit=100,
    )

    total_threats = len(overview_threats)

    critical_threats = sum(
        1
        for threat in overview_threats
        if threat.severity.value == "critical"
    )

    high_threats = sum(
        1
        for threat in overview_threats
        if threat.severity.value == "high"
    )

    medium_threats = sum(
        1
        for threat in overview_threats
        if threat.severity.value == "medium"
    )

    low_threats = sum(
        1
        for threat in overview_threats
        if threat.severity.value == "low"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Threats",
        total_threats,
    )

    col2.metric(
        "Critical / High",
        critical_threats + high_threats,
    )

    col3.metric(
        "Medium",
        medium_threats,
    )

    col4.metric(
        "Low",
        low_threats,
    )

except Exception as exc:

    st.error(
        "Unable to load security overview."
    )

    st.exception(exc)


st.divider()


# ============================================================
# SECURITY ANALYSIS
# ============================================================

st.header("🔍 Security Analysis")

if st.button(
    "▶ Run Security Analysis",
    type="primary",
):

    with st.spinner("Analyzing Windows events..."):

        try:

            result = run_security_analysis(
                log_name=log_name,
                limit=limit,
                scope=scope,
            )

            st.session_state["analysis_result"] = result

            st.success(
                "Security analysis completed successfully."
            )

        except PermissionError as exc:

            st.error(
                "Windows Event Log access was denied."
            )

            st.warning(
                "Use the System or Application log. "
                "The Security log requires Administrator permissions."
            )

            st.code(str(exc))

        except Exception as exc:

            st.error(
                "Analysis failed."
            )

            st.exception(exc)


# ============================================================
# ANALYSIS RESULTS
# ============================================================

if "analysis_result" in st.session_state:

    result = st.session_state["analysis_result"]

    st.subheader("📈 Latest Analysis")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Events Collected",
        result["events_collected"],
    )

    col2.metric(
        "Threats Detected",
        result["threats_detected"],
    )

    col3.metric(
        "Risk Score",
        result["risk_score"],
    )

    col4.metric(
        "Risk Level",
        result["risk_level"].upper(),
    )

    st.divider()

    st.subheader("🧾 Risk Assessment")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Assessment ID:** "
            f"`{result['assessment_id']}`"
        )

    with col2:

        st.write(
            f"**Scope:** `{scope}`"
        )

    st.info(
        f"Sentinel-AI analyzed "
        f"{result['events_collected']} Windows events "
        f"and detected "
        f"{result['threats_detected']} threats."
    )


# ============================================================
# RECENT THREATS
# ============================================================

st.divider()

st.header("🚨 Recent Threats")

try:

    repository = ThreatRepository()

    recent_threats = repository.query_threats(
        limit=20,
    )

    if recent_threats:

        st.write(
            f"Showing the "
            f"{len(recent_threats)} "
            f"most recent threats."
        )

        for threat in recent_threats:

            if threat.severity.value == "critical":

                severity_icon = "🔴"

            elif threat.severity.value == "high":

                severity_icon = "🟠"

            elif threat.severity.value == "medium":

                severity_icon = "🟡"

            else:

                severity_icon = "🟢"

            with st.container(border=True):

                st.subheader(
                    f"{severity_icon} "
                    f"{threat.threat_type}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"**Severity:** "
                        f"{threat.severity.value}"
                    )

                with col2:

                    st.write(
                        f"**Confidence:** "
                        f"{threat.confidence_score}"
                    )

                with col3:

                    st.write(
                        f"**Status:** "
                        f"{threat.status.value}"
                    )

                st.write(
                    f"**Threat ID:** "
                    f"`{threat.threat_id}`"
                )

                st.write(
                    f"**Description:** "
                    f"{threat.description}"
                )

                st.write(
                    f"**Detected:** "
                    f"{threat.detected_at}"
                )

    else:

        st.success(
            "No stored threats found."
        )

except Exception as exc:

    st.error(
        "Unable to load recent threats."
    )

    st.exception(exc)


# ============================================================
# THREAT DETECTION TEST
# ============================================================

st.divider()

st.header("🧪 Threat Detection Test")

st.write(
    "Create a simulated failed-login event "
    "to verify that Sentinel-AI detects threats."
)


if st.button(
    "Run Threat Detection Test"
):

    test_event = {
        "source": "dashboard_test",
        "event_type": "failed_login",
        "severity": "high",
        "host": scope,
        "description": "Simulated failed login detected.",
    }

    try:

        event_id = ingest_event(
            test_event
        )

        test_event["event_id"] = event_id

        threats = detect_threats(
            [test_event]
        )

        if threats:

            st.error(
                f"🚨 {len(threats)} threat(s) detected."
            )

            for threat in threats:

                st.warning(
                    f"**{threat['threat_type']}**"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"Severity: "
                        f"**{threat['severity']}**"
                    )

                with col2:

                    st.write(
                        f"Confidence: "
                        f"**{threat['confidence_score']}**"
                    )

                st.write(
                    threat["description"]
                )

        else:

            st.success(
                "No threats detected."
            )

    except Exception as exc:

        st.error(
            "Threat detection test failed."
        )

        st.exception(exc)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Sentinel-AI • Windows Security Monitoring & Threat Detection"
)