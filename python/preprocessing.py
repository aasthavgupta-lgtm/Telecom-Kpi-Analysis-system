import pandas as pd

# -----------------------------------------
# KPI BASELINES
# -----------------------------------------

BASELINES = {

    "availability_pct": 99,
    "cssr_pct": 98,
    "drop_rate_pct": 1
}


# -----------------------------------------
# MAIN PREPROCESSING FUNCTION
# -----------------------------------------

def preprocess_kpi_data(df):

    processed_records = []

    for _, row in df.iterrows():

        affected_kpis = []

        severity_score = 0

        # ---------------------------------
        # LATENCY ANALYSIS
        # ---------------------------------

        if row["avg_latency_ms"] > 150:

            affected_kpis.append("HIGH_LATENCY")

            severity_score += 2

        # ---------------------------------
        # PACKET LOSS ANALYSIS
        # ---------------------------------

        if row["packet_loss_pct"] > 5:

            affected_kpis.append("HIGH_PACKET_LOSS")

            severity_score += 2

        # ---------------------------------
        # DROP RATE ANALYSIS
        # ---------------------------------

        if row["drop_rate_pct"] > 2:

            affected_kpis.append("HIGH_DROP_RATE")

            severity_score += 2

        # ---------------------------------
        # AVAILABILITY ANALYSIS
        # ---------------------------------

        if row["availability_pct"] < 95:

            affected_kpis.append("LOW_AVAILABILITY")

            severity_score += 3

        # ---------------------------------
        # CSSR ANALYSIS
        # ---------------------------------

        if row["cssr_pct"] < 98:

            affected_kpis.append("LOW_CSSR")

            severity_score += 2

        # ---------------------------------
        # SEVERITY CLASSIFICATION
        # ---------------------------------

        if severity_score >= 7:

            severity = "CRITICAL"

        elif severity_score >= 5:

            severity = "HIGH"

        elif severity_score >= 3:

            severity = "MEDIUM"

        elif severity_score >= 1:

            severity = "LOW"

        else:

            severity = "NORMAL"

        # ---------------------------------
        # ROOT CAUSE DETECTION
        # ---------------------------------

        if (
            "HIGH_LATENCY" in affected_kpis and
            "HIGH_PACKET_LOSS" in affected_kpis
        ):

            root_cause = "NETWORK_CONGESTION"

        elif (
            "HIGH_DROP_RATE" in affected_kpis and
            "LOW_CSSR" in affected_kpis
        ):

            root_cause = "RADIO_SIGNAL_ISSUE"

        elif "LOW_AVAILABILITY" in affected_kpis:

            root_cause = "SITE_DOWNTIME"

        else:

            root_cause = "NORMAL_OPERATION"

        # ---------------------------------
        # FINAL RECORD
        # ---------------------------------

        processed_records.append({

            "event_hour": str(row["event_hour"]),
            "geo_level": row["geo_level"],
            "geo_id": row["geo_id"],
            "region": row["region"],
            "technology": row["technology"],

            "severity": severity,
            "affected_kpis": affected_kpis,
            "root_cause": root_cause,

            "availability_pct": row["availability_pct"],
            "cssr_pct": row["cssr_pct"],
            "drop_rate_pct": row["drop_rate_pct"],
            "avg_latency_ms": row["avg_latency_ms"],
            "packet_loss_pct": row["packet_loss_pct"]

        })

    return processed_records


# -----------------------------------------
# BUILD AI SUMMARY
# -----------------------------------------

def build_ai_summary(processed_records):

    df = pd.DataFrame(processed_records)

    # -----------------------------------------
    # KPI AVERAGES
    # -----------------------------------------

    avg_availability = round(
        df["availability_pct"].mean(),
        2
    )

    avg_cssr = round(
        df["cssr_pct"].mean(),
        2
    )

    avg_drop_rate = round(
        df["drop_rate_pct"].mean(),
        2
    )

    avg_latency = round(
        df["avg_latency_ms"].mean(),
        2
    )

    avg_packet_loss = round(
        df["packet_loss_pct"].mean(),
        2
    )

    # -----------------------------------------
    # KPI STATUS
    # -----------------------------------------

    availability_status = (
        "healthy"
        if avg_availability >= 99
        else "degraded"
    )

    cssr_status = (
        "healthy"
        if avg_cssr >= 98
        else "warning"
    )

    latency_status = (
        "critical"
        if avg_latency > 150
        else "healthy"
    )

    packet_loss_status = (
        "critical"
        if avg_packet_loss > 5
        else "healthy"
    )

    drop_rate_status = (
        "critical"
        if avg_drop_rate > 2
        else "healthy"
    )

    # -----------------------------------------
    # OVERALL NETWORK HEALTH
    # -----------------------------------------

    if (
        latency_status == "critical"
        or packet_loss_status == "critical"
        or drop_rate_status == "critical"
    ):

        overall_network_health = "poor"

    else:

        overall_network_health = "healthy"

    # -----------------------------------------
    # BASELINE DEVIATION ANALYSIS
    # -----------------------------------------

    availability_deviation = round(
        (
            (
                avg_availability -
                BASELINES["availability_pct"]
            )
            /
            BASELINES["availability_pct"]
        ) * 100,
        2
    )

    cssr_deviation = round(
        (
            (
                avg_cssr -
                BASELINES["cssr_pct"]
            )
            /
            BASELINES["cssr_pct"]
        ) * 100,
        2
    )

    drop_rate_deviation = round(
        (
            (
                avg_drop_rate -
                BASELINES["drop_rate_pct"]
            )
            /
            BASELINES["drop_rate_pct"]
        ) * 100,
        2
    )

    # -----------------------------------------
    # SEGMENT IMPACT ANALYSIS
    # -----------------------------------------

    segment_impact = (
        df.groupby(
            ["geo_level", "geo_id"]
        )["drop_rate_pct"]
        .mean()
        .sort_values(ascending=False)
        .head(3)
    )

    top_impacted_segments = []

    for idx, value in segment_impact.items():

        geo_level, geo_id = idx

        top_impacted_segments.append({

            "geo_level": geo_level,
            "geo_id": geo_id,
            "impact": f"{round(value,2)} average drop rate"

        })

    # -----------------------------------------
    # KPI RELATIONSHIP ANALYSIS
    # -----------------------------------------

    kpi_relationships = []

    if avg_latency > 150 and avg_packet_loss > 5:

        kpi_relationships.append(
            "High latency and packet loss leading to increased call failures"
        )

    if avg_drop_rate > 2 and avg_cssr < 98:

        kpi_relationships.append(
            "Call failures resulting in increased drop rate and reduced CSSR"
        )

    # -----------------------------------------
    # ROOT CAUSE ANALYSIS
    # -----------------------------------------

    possible_root_causes = []

    if avg_packet_loss > 5:

        possible_root_causes.append(
            f"High packet loss ({avg_packet_loss}%) causing session instability"
        )

    if avg_latency > 150:

        possible_root_causes.append(
            f"High latency ({avg_latency} ms) impacting call setup success"
        )

    if avg_drop_rate > 2:

        possible_root_causes.append(
            f"Increased drop rate ({avg_drop_rate}%) indicating network congestion"
        )

    if avg_availability < 95:

        possible_root_causes.append(
            f"Availability degradation ({avg_availability}%) indicating possible site downtime"
        )

    # -----------------------------------------
    # SEVERITY CLASSIFICATION
    # -----------------------------------------

    critical_kpis = 0

    if latency_status == "critical":
        critical_kpis += 1

    if packet_loss_status == "critical":
        critical_kpis += 1

    if drop_rate_status == "critical":
        critical_kpis += 1

    if critical_kpis >= 2:

        severity = "CRITICAL"

    elif critical_kpis == 1:

        severity = "WARNING"

    else:

        severity = "HEALTHY"

    # -----------------------------------------
    # SEVERITY REASON
    # -----------------------------------------

    severity_reason = ""

    if severity == "CRITICAL":

        severity_reason = (
            "Multiple KPIs breached with high deviation "
            "impacting telecom service quality"
        )

    elif severity == "WARNING":

        severity_reason = (
            "One or more KPIs exceeded expected thresholds"
        )

    else:

        severity_reason = (
            "All KPIs operating within acceptable thresholds"
        )

    # -----------------------------------------
    # FINAL AI SUMMARY
    # -----------------------------------------

    ai_summary = {

        "kpi_analysis": {

            "availability_status": availability_status,
            "cssr_status": cssr_status,
            "latency_status": latency_status,
            "packet_loss_status": packet_loss_status,
            "drop_rate_status": drop_rate_status,
            "overall_network_health": overall_network_health
        },

        "baseline_analysis": {

            "availability_deviation_pct":
                availability_deviation,

            "cssr_deviation_pct":
                cssr_deviation,

            "drop_rate_deviation_pct":
                drop_rate_deviation
        },

        "severity_classification": {

            "severity": severity,
            "reason": severity_reason
        },

        "top_impacted_segments":
            top_impacted_segments,

        "kpi_relationships":
            kpi_relationships,

        "possible_root_causes":
            possible_root_causes
    }

    return ai_summary