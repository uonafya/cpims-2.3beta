DROP TABLE IF EXISTS master_list;
SELECT * INTO master_list FROM (
SELECT 
child_cbo_id AS cbo_id, reg_org_unit.org_unit_name AS cbo,
list_geo.area_id AS ward_id, list_geo.area_name AS ward,
scc.area_name AS constituency, cc.area_name AS county,
ovc_registration.person_id AS cpims_ovc_id,
concat(reg_person.first_name,' ',reg_person.surname,' ',reg_person.other_names) AS ovc_names,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS gender,
reg_person.date_of_birth AS DOB,
date_part('year', age(timestamp '2018-03-31', reg_person.date_of_birth)) AS age,
CASE
WHEN  date_part('year', age(timestamp '2018-03-31', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '2018-03-31', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '2018-03-31', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '2018-03-31', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '2018-03-31', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '2018-03-31', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE has_bcert WHEN 'True' THEN 'HAS BIRTHCERT' ELSE 'NO BIRTHCERT' END AS BirthCert,
CASE has_bcert WHEN 'True' THEN exids.identifier ELSE NULL END AS BCertNumber,
CASE is_disabled WHEN 'True' THEN 'HAS DISABILITY' ELSE 'NO DISABILITY' END AS OVCDisability,
CASE is_Disabled WHEN 'True' THEN exidd.identifier ELSE NULL END AS NCPWDNumber,
CASE ovc_registration.hiv_status
WHEN 'HSTP' THEN 'POSITIVE'
WHEN 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE ovc_registration.hiv_status WHEN 'HSTP' THEN 'ART' ELSE NULL END AS ARTStatus,
ovc_care_health.facility_id as facility_id,
ovc_facility.facility_name as facility,
ovc_care_health.date_linked as date_of_linkage, ovc_care_health.ccc_number,
child_chv_id as chv_id,
concat(chvs.first_name,' ',chvs.other_names,' ',chvs.surname) as CHV_Names,
caretaker_id as caregiver_id,
concat(cgs.first_name,' ',cgs.other_names,' ',cgs.surname) as Caregiver_Names,
CASE
WHEN ovc_household_members.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN ovc_household_members.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS CaregiverHIVstatus,
CASE ovc_registration.school_level
WHEN 'SLTV' THEN 'Tertiary'
WHEN 'SLUN' THEN 'University'
WHEN 'SLSE' THEN 'Secondary'
WHEN 'SLPR' THEN 'Primary'
WHEN 'SLEC' THEN 'ECDE'
ELSE 'Not in School' END AS Schoollevel,
ovc_care_education.school_id as school_id,
ovc_school.school_name as school_name,
ovc_care_education.school_class as class,
registration_date,
CASE is_active WHEN 'True' THEN 'ACTIVE' ELSE 'EXITED' END AS Exit_Status,
exits.item_description as Exit_Reason,
CASE is_active WHEN 'False' THEN exit_date ELSE NULL END AS Exit_Date,
CASE immunization_status
WHEN 'IMFI' THEN 'Fully Immunized'
WHEN 'IMNI' THEN 'Not Immunized'
WHEN 'IMNC' THEN 'Not Completed'
ELSE 'Not Known' END AS immunization
FROM ovc_registration INNER JOIN reg_person ON reg_person.id=ovc_registration.person_id
LEFT OUTER JOIN reg_org_unit ON ovc_registration.child_cbo_id=reg_org_unit.id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id AND reg_persons_geo.area_id > 337
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id AND reg_persons_geo.area_id > 337
LEFT OUTER JOIN list_geo AS scc ON scc.area_id=list_geo.parent_area_id
LEFT OUTER JOIN list_geo AS cc ON cc.area_id=scc.parent_area_id
LEFT OUTER JOIN list_general AS exits ON exits.item_id=ovc_registration.exit_reason AND exits.field_name='exit_reason_id'
LEFT OUTER JOIN reg_person cgs ON caretaker_id=cgs.id
LEFT OUTER JOIN reg_person chvs ON child_chv_id=chvs.id
LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id
LEFT OUTER JOIN ovc_facility ON ovc_care_health.facility_id=ovc_facility.id
LEFT OUTER JOIN ovc_care_education ON ovc_care_education.person_id=ovc_registration.person_id
LEFT OUTER JOIN ovc_school ON ovc_care_education.school_id=ovc_school.id
LEFT OUTER JOIN ovc_household_members ON ovc_registration.caretaker_id=ovc_household_members.person_id
LEFT OUTER JOIN reg_persons_external_ids as exids on exids.person_id=ovc_registration.person_id and exids.identifier_type_id = 'ISOV'
LEFT OUTER JOIN reg_persons_external_ids as exidd on exidd.person_id=ovc_registration.person_id and exidd.identifier_type_id = 'IPWD') as mls;
