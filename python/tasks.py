from crewai import Task

from agents import (
    kpi_aggregation_agent,
    baseline_agent,
    sla_agent,
    severity_agent,
    root_cause_agent
)

# -----------------------------------------
# KPI Aggregation Task
# -----------------------------------------

kpi_aggregation_task = Task(

    description="""
    Analyze the following telecom KPI intelligence data:

    {telecom_data}

    Identify:
    - degraded KPIs
    - operational KPI health
    - abnormal telecom behavior

    Return ONLY valid JSON.

    Example:

    {
      "kpi_analysis": {
        "availability_status": "degraded",
        "cssr_status": "warning",
        "drop_rate_status": "critical",
        "overall_network_health": "poor"
      }
    }
    """,

    expected_output="""
    Strict JSON output containing KPI health analysis only.
    """,

    agent=kpi_aggregation_agent
)

# -----------------------------------------
# Baseline Comparison Task
# -----------------------------------------

baseline_task = Task(

    description="""
    Analyze the following telecom KPI intelligence data:

    {telecom_data}

    Compare KPI values against telecom baselines.

    Baselines:
    - Availability = 98%
    - CSSR = 99%
    - Drop Rate = 1%

    Return ONLY valid JSON.

    Example:

    {
      "baseline_analysis": {
        "availability_deviation_pct": -10,
        "cssr_deviation_pct": -4,
        "drop_rate_deviation_pct": 3
      }
    }
    """,

    expected_output="""
    Strict JSON output containing KPI baseline deviations.
    """,

    agent=baseline_agent
)

# -----------------------------------------
# SLA Validation Task
# -----------------------------------------

sla_validation_task = Task(

    description="""
    Analyze the following telecom KPI intelligence data:

    {telecom_data}

    Validate KPIs against SLA thresholds.

    SLA Rules:
    - Availability > 95%
    - CSSR > 98%
    - Drop Rate < 2%

    Return ONLY valid JSON.

    Example:

    {
      "sla_validation": {
        "availability_sla_breach": true,
        "cssr_sla_breach": true,
        "drop_rate_sla_breach": false
      }
    }
    """,

    expected_output="""
    Strict JSON output containing SLA validation results.
    """,

    agent=sla_agent
)

# -----------------------------------------
# Severity Classification Task
# -----------------------------------------

severity_task = Task(

    description="""
    Analyze the following telecom KPI intelligence data:

    {telecom_data}

    Classify telecom operational severity.

    Allowed values:
    - HEALTHY
    - WARNING
    - CRITICAL

    Return ONLY valid JSON.

    Example:

    {
      "severity_classification": {
        "severity": "CRITICAL"
      }
    }
    """,

    expected_output="""
    Strict JSON output containing severity classification.
    """,

    agent=severity_agent
)

# -----------------------------------------
# Root Cause Analysis Task
# -----------------------------------------

root_cause_task = Task(

    description="""
    Analyze the following telecom KPI intelligence data:

    {telecom_data}

    Infer possible operational root causes.

    Consider:
    - latency
    - packet loss
    - drop rate
    - SLA violations
    - availability degradation

    Return ONLY valid JSON.

    Example:

    {
      "possible_root_causes": [
        "network congestion",
        "packet loss",
        "radio instability"
      ]
    }
    """,

    expected_output="""
    Strict JSON output containing root cause analysis.
    """,

    agent=root_cause_agent
)