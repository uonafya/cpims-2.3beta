DROP MATERIALIZED VIEW IF EXISTS data_quality_ovc_care_services;
DROP MATERIALIZED VIEW IF EXISTS data_quality_form1b;
DROP MATERIALIZED VIEW IF EXISTS  data_quality_priority;
DROP MATERIALIZED VIEW IF EXISTS data_quality_case_plan;
DROP MATERIALIZED VIEW IF EXISTS data_quality_view;


create MATERIALIZED view data_quality_view as select
 ovc_registration.id as ovc_registration_id,
 ovc_registration.registration_date,
 ovc_registration.has_bcert,
 ovc_registration.is_disabled,
 ovc_registration.hiv_status,
 ovc_registration.school_level,
 ovc_registration.immunization_status,
 ovc_registration.org_unique_id,
 ovc_registration.exit_reason,
 ovc_registration.exit_date,
 ovc_registration.created_at as ovc_registration_created_at,
 ovc_registration.is_active as ovc_registration_is_active,
 ovc_registration.is_void as ovc_registration_is_void,
 ovc_registration.caretaker_id,
 ovc_registration.child_cbo_id,
 ovc_registration.child_chv_id,
 ovc_registration.person_id,
 ovc_registration.art_status,
 reg_person.id as reg_person_id,
 reg_person.designation,
 reg_person.first_name,
 reg_person.other_names,
 reg_person.surname,
 reg_person.email,
 reg_person.des_phone_number,
 reg_person.date_of_birth,
 reg_person.date_of_death,
 reg_person.sex_id,
 reg_person.is_void,
 reg_person.created_at as reg_person_created_at,
 reg_person.created_by_id,
 extract ( year from age(reg_person.date_of_birth)) as age,
 reg_org_unit.org_unit_name
 from ovc_registration inner join reg_person on ovc_registration.person_id=reg_person.id
 inner join reg_org_unit on reg_org_unit.id=ovc_registration.child_cbo_id;

CREATE INDEX IF NOT EXISTS hiv_status_index on data_quality_view USING btree (hiv_status);
CREATE INDEX IF NOT EXISTS art_status_index on data_quality_view USING btree (art_status);
CREATE INDEX IF NOT EXISTS school_level_index on data_quality_view USING btree (school_level);
CREATE INDEX IF NOT EXISTS age_index on data_quality_view USING btree (age);
