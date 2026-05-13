{{ config(materialized='table') }}

WITH filtered_network_data AS (

    SELECT *

    FROM `acn-datafabricpoc.Interns_Test_Dataset.AG_network_kpi_data`

    -- -----------------------------------------
    -- DATE FILTERING
    -- Prevent mixing historical + current data
    -- -----------------------------------------

    -- WHERE DATE(event_hour)
    -- BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    -- AND CURRENT_DATE()

),

network_kpi_calculation AS (

    SELECT

        -- -----------------------------------------
        -- IDENTIFIERS
        -- -----------------------------------------

        kpi_row_id,

        event_hour,

        geo_level,

        geo_id,

        region,

        technology,

        -- -----------------------------------------
        -- NETWORK KPI CALCULATIONS
        -- -----------------------------------------

        ROUND(
            (
                uptime_minutes * 100.0
            )
            /
            NULLIF(
                uptime_minutes + downtime_minutes,
                0
            ),
            2
        ) AS availability_pct,

        ROUND(
            (
                call_setup_successes * 100.0
            )
            /
            NULLIF(
                call_setup_attempts,
                0
            ),
            2
        ) AS cssr_pct,

        ROUND(
            (
                call_drops * 100.0
            )
            /
            NULLIF(
                call_connected,
                0
            ),
            2
        ) AS drop_rate_pct,

        -- -----------------------------------------
        -- SUPPORTING NETWORK METRICS
        -- -----------------------------------------

        avg_latency_ms,

        packet_loss_pct,

        avg_downlink_throughput_mbps,

        avg_uplink_throughput_mbps,

        uptime_minutes,

        downtime_minutes,

        call_setup_attempts,

        call_setup_successes,

        call_connected,

        call_drops

    FROM filtered_network_data

),

-- -----------------------------------------
-- ROOT CAUSE FLAGS
-- -----------------------------------------

root_cause_analysis AS (

    SELECT

        *,

        CASE
            WHEN packet_loss_pct > 5
            THEN 'HIGH_PACKET_LOSS'

            WHEN avg_latency_ms > 150
            THEN 'HIGH_LATENCY'

            WHEN drop_rate_pct > 2
            THEN 'NETWORK_CONGESTION'

            ELSE 'NORMAL'
        END AS possible_root_cause,

        CASE
            WHEN availability_pct < 95
            OR cssr_pct < 98
            OR drop_rate_pct > 2
            THEN 'SLA_BREACH'

            ELSE 'SLA_OK'
        END AS sla_status

    FROM network_kpi_calculation

)

-- -----------------------------------------
-- FINAL OUTPUT
-- -----------------------------------------

SELECT *

FROM root_cause_analysis