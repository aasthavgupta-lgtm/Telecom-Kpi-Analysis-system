from llm_filter import generate_filter
from bq_fetch import fetch_filtered_data

from preprocessing import (
    preprocess_kpi_data,
    build_ai_summary
)

from crew import telecom_kpi_crew

import json


def main():

    # ---------------------------------
    # USER INPUT
    # ---------------------------------

    user_input = input("Enter filter request: ")

    # ---------------------------------
    # GENERATE SQL WHERE CLAUSE
    # ---------------------------------

    where_clause = generate_filter(user_input)

    print("\nGenerated WHERE clause:")
    print(where_clause)

    # ---------------------------------
    # FETCH FILTERED DATA
    # ---------------------------------

    df = fetch_filtered_data(where_clause)

    # ---------------------------------
    # EMPTY CHECK
    # ---------------------------------

    if df.empty:
        print("\nNo records found.")
        return

    print(f"\nTotal Records Found: {len(df)}")

    print("\nFiltered Data Preview:\n")
    print(df.head())

    # ---------------------------------
    # PREPROCESS TELECOM DATA
    # ---------------------------------

    processed_records = preprocess_kpi_data(df)

    # ---------------------------------
    # BUILD AI SUMMARY
    # ---------------------------------

    ai_summary = build_ai_summary(processed_records)

    print("\nAI Telecom Summary:\n")

    print(json.dumps(ai_summary, indent=4))

    # ---------------------------------
    # INJECT AI SUMMARY INTO TASKS
    # ---------------------------------

    for task in telecom_kpi_crew.tasks:

        task.description += f"""

        TELECOM KPI INTELLIGENCE SUMMARY:

        {json.dumps(ai_summary, indent=4)}

        """

    # ---------------------------------
    # RUN CREW AI ANALYSIS
    # ---------------------------------

    print("\nRunning CrewAI Telecom Analysis...\n")

    agent_outputs = []

    for task in telecom_kpi_crew.tasks:

        print(f"\nRunning Task: {task.agent.role}\n")

        output = task.execute_sync()

        raw_output = output.raw.strip()

        # ---------------------------------
        # CLEAN MARKDOWN JSON
        # ---------------------------------

        raw_output = raw_output.replace(
            "```json",
            ""
        )

        raw_output = raw_output.replace(
            "```",
            ""
        )

        raw_output = raw_output.strip()

        # ---------------------------------
        # PARSE JSON
        # ---------------------------------

        try:

            parsed_json = json.loads(raw_output)

            agent_outputs.append(parsed_json)

        except Exception as e:

            print("\nJSON Parsing Error:", e)

            print("\nRaw Output:\n")

            print(raw_output)

    # ---------------------------------
    # MERGE ALL AGENT OUTPUTS
    # ---------------------------------

    final_output = {}

    for item in agent_outputs:

        final_output.update(item)

    # ---------------------------------
    # FINAL AI OUTPUT
    # ---------------------------------

    print("\n===================================")
    print("FINAL AI TELECOM ANALYSIS")
    print("===================================\n")

    print(json.dumps(final_output, indent=4))

    # ---------------------------------
    # SAVE FINAL OUTPUT
    # ---------------------------------

    with open("final_output.json", "w") as f:

        json.dump(final_output, f, indent=4)

    print("\nfinal_output.json saved successfully.\n")


if __name__ == "__main__":
    main()