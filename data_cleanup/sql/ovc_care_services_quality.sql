
 DROP MATERIALIZED VIEW IF EXISTS data_quality_ovc_care_services;

 CREATE MATERIALIZED VIEW data_quality_ovc_care_services AS SELECT
 ovc_care_services.service_provided,
 ovc_care_services.domain,
 ovc_care_services.service_id as id,
 ovc_care_events.event,
 ovc_care_events.date_of_event,
 ovc_care_events.person_id as ovc_care_events_person_id,
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

 FROM ovc_care_services
 LEFT JOIN ovc_care_events ON ovc_care_events.event=ovc_care_services.event_id
 LEFT JOIN data_quality_view ON data_quality_view.person_id=ovc_care_events.person_id;

CREATE INDEX IF NOT EXISTS service_provided_index on data_quality_ovc_care_services USING btree (service_provided);
CREATE INDEX IF NOT EXISTS service_domain_index on data_quality_ovc_care_services USING btree (domain);