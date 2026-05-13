import pandas as pd


def preprocess_kpi_data(df):

    processed_records = []

    for _, row in df.iterrows():

        affected_kpis = []

        severity_score = 0

        # ----------------------------
        # LATENCY
        # ----------------------------

        if row["avg_latency_ms"] > 120:
            affected_kpis.append("HIGH_LATENCY")
            severity_score += 2

        # ----------------------------
        # PACKET LOSS
        # ----------------------------

        if row["packet_loss_pct"] > 2:
            affected_kpis.append("HIGH_PACKET_LOSS")
            severity_score += 2

        # ----------------------------
        # DROP RATE
        # ----------------------------

        if row["drop_rate_pct"] > 3:
            affected_kpis.append("HIGH_DROP_RATE")
            severity_score += 2

        # ----------------------------
        # AVAILABILITY
        # ----------------------------

        if row["availability_pct"] < 99:
            affected_kpis.append("LOW_AVAILABILITY")
            severity_score += 3

        # ----------------------------
        # CSSR
        # ----------------------------

        if row["cssr_pct"] < 95:
            affected_kpis.append("LOW_CSSR")
            severity_score += 2

        # ----------------------------
        # SEVERITY CLASSIFICATION
        # ----------------------------

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

        # ----------------------------
        # ROOT CAUSE DETECTION
        # ----------------------------

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

        # ----------------------------
        # FINAL JSON
        # ----------------------------

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

def build_ai_summary(processed_records):

    summary = {

        "total_records": len(processed_records),

        "critical_count": 0,
        "high_count": 0,
        "medium_count": 0,

        "top_impacted_geo_ids": [],

        "major_root_causes": [],

        "high_latency_count": 0,
        "high_packet_loss_count": 0,
        "drop_rate_issues": 0,

        "regions_impacted": []
    }

    geo_ids = []
    root_causes = set()
    regions = set()

    for record in processed_records:

        severity = record["severity"]

        if severity == "CRITICAL":
            summary["critical_count"] += 1

        elif severity == "HIGH":
            summary["high_count"] += 1

        elif severity == "MEDIUM":
            summary["medium_count"] += 1

        geo_ids.append(record["geo_id"])

        root_causes.add(record["root_cause"])

        regions.add(record["region"])

        if "HIGH_LATENCY" in record["affected_kpis"]:
            summary["high_latency_count"] += 1

        if "HIGH_PACKET_LOSS" in record["affected_kpis"]:
            summary["high_packet_loss_count"] += 1

        if "HIGH_DROP_RATE" in record["affected_kpis"]:
            summary["drop_rate_issues"] += 1

    summary["top_impacted_geo_ids"] = list(set(geo_ids))[:5]

    summary["major_root_causes"] = list(root_causes)

    summary["regions_impacted"] = list(regions)

    return summary