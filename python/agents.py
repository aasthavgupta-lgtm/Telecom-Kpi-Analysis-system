from crewai import Agent, LLM
from dotenv import load_dotenv
import os

# -----------------------------------------
# Load environment variables
# -----------------------------------------

load_dotenv()

# -----------------------------------------
# Initialize Groq LLM
# -----------------------------------------

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------------------
# KPI Aggregation Agent
# -----------------------------------------

kpi_aggregation_agent = Agent(

    role="Telecom KPI Aggregation Specialist",

    goal="""
    Analyze telecom KPI datasets and summarize
    the overall operational health of the network.
    """,

    backstory="""
    You are an experienced telecom KPI analyst
    responsible for monitoring network performance
    metrics such as:
    - availability
    - CSSR
    - latency
    - packet loss
    - drop rate

    You identify degraded KPI behavior,
    abnormal operational patterns,
    and telecom network instability.
    """,

    llm=llm,

    verbose=True,
    max_iter=1
)

# -----------------------------------------
# Baseline Comparison Agent
# -----------------------------------------

baseline_agent = Agent(

    role="Telecom Baseline Comparison Analyst",

    goal="""
    Compare current telecom KPI values against
    expected historical baselines and detect abnormal deviations.
    """,

    backstory="""
    You specialize in telecom operational baseline analysis.

    You determine whether network KPIs are behaving
    abnormally compared to expected telecom performance.
    """,

    llm=llm,

    verbose=True,
    max_iter=1
)

# -----------------------------------------
# SLA Validation Agent
# -----------------------------------------

sla_agent = Agent(

    role="Telecom SLA Validation Specialist",

    goal="""
    Validate telecom KPIs against SLA thresholds
    and identify operational SLA violations.
    """,

    backstory="""
    You monitor telecom SLA compliance.

    You identify service degradation,
    KPI threshold violations,
    and SLA breaches.
    """,

    llm=llm,

    verbose=True,
    max_iter=1
)

# -----------------------------------------
# Severity Classification Agent
# -----------------------------------------

severity_agent = Agent(

    role="Telecom Severity Classification Expert",

    goal="""
    Classify telecom network operational severity.
    """,

    backstory="""
    You are a telecom operational risk specialist.

    You classify telecom operational states into:
    - HEALTHY
    - WARNING
    - CRITICAL
    """,

    llm=llm,

    verbose=True,
    max_iter=1
)

# -----------------------------------------
# Root Cause Analysis Agent
# -----------------------------------------

root_cause_agent = Agent(

    role="Telecom Root Cause Analysis Engineer",

    goal="""
    Infer possible operational causes responsible
    for telecom KPI degradation.
    """,

    backstory="""
    You are an experienced telecom operations engineer.

    You specialize in identifying:
    - network congestion
    - packet loss
    - service instability
    - high latency
    - radio issues
    - downtime
    - infrastructure problems

    based on telecom KPI behavior.
    """,

    llm=llm,

    verbose=True,
    max_iter=1
)