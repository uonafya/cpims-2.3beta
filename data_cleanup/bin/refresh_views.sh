#!/usr/bin/env bash

psql -U $CPIMS_DBUSER -h $CPIMS_HOST -d $CPIMS_DB -c "REFRESH MATERIALIZED VIEW data_quality_case_plan"
psql -U $CPIMS_DBUSER -h $CPIMS_HOST -d $CPIMS_DB -c "REFRESH MATERIALIZED VIEW data_quality_view"
psql -U $CPIMS_DBUSER -h $CPIMS_HOST -d $CPIMS_DB -c "REFRESH MATERIALIZED VIEW data_quality_form1b"
psql -U $CPIMS_DBUSER -h $CPIMS_HOST -d $CPIMS_DB -c "REFRESH MATERIALIZED VIEW data_quality_ovc_care_services"
psql -U $CPIMS_DBUSER -h $CPIMS_HOST -d $CPIMS_DB -c "REFRESH MATERIALIZED VIEW data_quality_priority"
