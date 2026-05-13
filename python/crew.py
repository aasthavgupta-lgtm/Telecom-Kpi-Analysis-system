from crewai import Crew

from agents import (
    kpi_aggregation_agent,
    baseline_agent,
    sla_agent,
    severity_agent,
    root_cause_agent
)

from tasks import (
    kpi_aggregation_task,
    baseline_task,
    sla_validation_task,
    severity_task,
    root_cause_task
)

# -----------------------------------------
# Telecom KPI Intelligence Crew
# -----------------------------------------

telecom_kpi_crew = Crew(

    agents=[

        kpi_aggregation_agent,
        baseline_agent,
        sla_agent,
        severity_agent,
        root_cause_agent
    ],

    tasks=[

        kpi_aggregation_task,
        baseline_task,
        sla_validation_task,
        severity_task,
        root_cause_task
    ],

    verbose=True
)