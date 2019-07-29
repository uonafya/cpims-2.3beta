DROP MATERIALIZED VIEW IF EXISTS data_quality_form1b;

CREATE MATERIALIZED VIEW data_quality_form1b AS SELECT
ovc_care_f1b.form_id,
ovc_care_f1b.domain,
ovc_care_f1b.entity,
ovc_care_f1b.value,
ovc_care_f1b.event_id,
reg_person.id as reg_person_id_f1b

FROM data_quality_view LEFT JOIN reg_person ON data_quality_view.reg_person_id=reg_person_id_f1b
LEFT JOIN ovc_care_events ON ovc_care_events.person_id = data_quality_view.reg_person_id_f1b;
