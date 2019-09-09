DROP MATERIALIZED VIEW IF EXISTS data_quality_form1b;

CREATE MATERIALIZED VIEW data_quality_form1b AS SELECT
ovc_care_f1b.form_id as id,
ovc_care_f1b.domain,
ovc_care_f1b.entity,
ovc_care_f1b.value,
ovc_care_f1b.event_id,
ovc_care_events.event,
ovc_care_events.person_id as ovc_care_events_person_id,
data_quality_view.ovc_registration_id,
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
data_quality_view.exit_date

FROM ovc_care_f1b
LEFT JOIN ovc_care_events ON ovc_care_events.event=ovc_care_f1b.event_id
LEFT JOIN data_quality_view ON data_quality_view.person_id=ovc_care_events.person_id
WHERE ovc_care_events.is_void='f';
