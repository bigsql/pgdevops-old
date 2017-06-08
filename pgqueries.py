####################################################################
#########         Copyright 2016-2017 BigSQL             ###########
####################################################################

connection_query = """WITH act_base as (
                    SELECT unnest(ARRAY['idle','active','idle_in_transaction']) as "state" )
                    SELECT ab.state, count(sa.state)
                    FROM act_base ab LEFT OUTER JOIN pg_stat_activity sa ON ab.state = sa.state
                    GROUP BY ab.state
                    UNION ALL
                    SELECT 'total', count(1) FROM pg_stat_activity
                    UNION ALL
                    SELECT 'max', setting::bigint FROM pg_settings WHERE name='max_connections'"""

metrics_query = """SELECT sum(numbackends::float8) as "num_backends",
                          sum(xact_commit::float8) as "xact_commit",
                          sum(xact_rollback::float8) as "xact_rollback",
                          sum(blks_read::float8) as "blks_read",
                          sum(blks_hit::float8) as "blks_hit",
                          sum(tup_fetched::float8) as "tup_fetched",
                          sum(tup_inserted::float8) as "tup_inserted",
                          sum(tup_updated::float8) as "tup_updated",
                          sum(tup_deleted::float8) as "tup_deleted"
                     FROM pg_stat_database"""

pg_settings_query = "select category, name, setting, short_desc from pg_settings order by category"


activity_query = """SELECT datname, state, pid, usename, client_addr::varchar,
            to_char(backend_start::timestamp(0),'MM-DD-YYYY HH24:MI:SS') as backend_start,
            to_char(xact_start::timestamp(0),'MM-DD-YYYY HH24:MI:SS') as xact_start,
            justify_interval((clock_timestamp() - query_start)::interval(0))::varchar as query_time,
            query
            FROM pg_stat_activity
            ORDER BY 8 DESC"""