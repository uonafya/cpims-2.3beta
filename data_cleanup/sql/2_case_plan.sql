
DROP MATERIALIZED VIEW IF EXISTS data_quality_case_plan;

CREATE MATERIALIZED VIEW data_quality_case_plan AS SELECT
    ovc_care_case_plan.case_plan_id as id,
    ovc_care_case_plan.domain,
    ovc_care_case_plan.goal,
    ovc_care_case_plan.need,
    ovc_care_case_plan.priority,
    ovc_care_case_plan.cp_service,
    ovc_care_case_plan.responsible,
    ovc_care_case_plan.completion_date,
    ovc_care_case_plan.results,
    ovc_care_case_plan.reasons,
    ovc_care_case_plan.date_of_event,
    ovc_care_case_plan.date_of_previous_event,
    ovc_care_case_plan.case_plan_status,
    ovc_care_case_plan.initial_caseplan,
    ovc_care_case_plan.is_void,
    ovc_care_case_plan.timestamp_created,
    ovc_care_case_plan.timestamp_updated,
    ovc_care_case_plan.event_id,
    ovc_care_case_plan.form_id,
    ovc_care_case_plan.household_id,
    ovc_care_case_plan.person_id as case_plan_person_id,
    ovc_care_case_plan.caregiver_id,
    ovc_care_case_plan.actual_completion_date,
    data_quality_view.reg_person_id,
    data_quality_view.has_bcert,
    data_quality_view.is_disabled,
    data_quality_view.hiv_status,
    data_quality_view.school_level,
    data_quality_view.child_cbo_id,
    data_quality_view.person_id,
    data_quality_view.art_status,
    data_quality_view.designation,
    data_quality_view.first_name,
    data_quality_view.other_names,
    data_quality_view.surname,
    data_quality_view.age,
    data_quality_view.sex_id,
    data_quality_view.exit_date,
    data_quality_view.org_unit_name

FROM ovc_care_case_plan
INNER JOIN data_quality_view ON ovc_care_case_plan.person_id=data_quality_view.person_id;

CREATE INDEX IF NOT EXISTS cp_service_index on data_quality_case_plan USING btree (cp_service);
