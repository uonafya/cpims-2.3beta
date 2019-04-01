QUERIES = {}
# Reports
REPORTS = {}
# Reports listings
REPORTS[1] = 'registration'
REPORTS[2] = 'registration'
REPORTS[3] = 'registration'
REPORTS[4] = 'registration'
REPORTS[5] = 'not_served'
REPORTS[6] = 'pepfar_detailed'
REPORTS[7] = 'registration'
REPORTS[8] = 'ovc_priority_list'
REPORTS[9] = 'form1a_summary'
REPORTS[10] = 'needs_vs_served'
REPORTS[11] = 'form1b_summary'
REPORTS[12] = 'ovc_served_list'
REPORTS[13] = 'master_list'
REPORTS[14] = 'ovc_assessed_list'
REPORTS[51] = 'datim'
REPORTS[52] = 'pepfar'
REPORTS[53] = 'kpi'

# Master List
QUERIES['master_list'] = '''
select * from master_list where cbo_id in ({cbos})
'''

QUERIES['registration'] = '''
SELECT
DISTINCT(ovc_registration.person_id) AS cpims_ovc_id,
child_cbo_id AS cbo_id, reg_org_unit.org_unit_name AS cbo,
list_geo.area_id AS ward_id, list_geo.area_name AS ward,
scc.area_name AS constituency, cc.area_name AS county,
concat(reg_person.first_name,' ',reg_person.surname,' ',reg_person.other_names) AS ovc_names,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS gender,
reg_person.date_of_birth AS DOB,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
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
CASE chvs.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS CHV_Gender,
caretaker_id as caregiver_id,
concat(cgs.first_name,' ',cgs.other_names,' ',cgs.surname) as Caregiver_Names,
CASE cgs.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Caregiver_Gender,
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
ELSE 'Not Known' END AS immunization,
reg_persons_geo.id AS geo_record_id,
ovc_care_education.created_at AS education_date
FROM ovc_registration INNER JOIN reg_person ON reg_person.id=ovc_registration.person_id
LEFT OUTER JOIN reg_org_unit ON ovc_registration.child_cbo_id=reg_org_unit.id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id AND reg_persons_geo.area_id > 337 AND reg_persons_geo.is_void = False
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id AND reg_persons_geo.area_id > 337
LEFT OUTER JOIN list_geo AS scc ON scc.area_id=list_geo.parent_area_id
LEFT OUTER JOIN list_geo AS cc ON cc.area_id=scc.parent_area_id
LEFT OUTER JOIN list_general AS exits ON exits.item_id=ovc_registration.exit_reason AND exits.field_name='exit_reason_id' AND ovc_registration.is_active=False
LEFT OUTER JOIN reg_person cgs ON caretaker_id=cgs.id
LEFT OUTER JOIN reg_person chvs ON child_chv_id=chvs.id
LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id AND ovc_registration.hiv_status = 'HSTP'
LEFT OUTER JOIN ovc_facility ON ovc_care_health.facility_id=ovc_facility.id
LEFT OUTER JOIN ovc_care_education ON ovc_care_education.person_id=ovc_registration.person_id AND ovc_care_education.is_void = False AND
(ovc_registration.school_level = 'SLTV' or ovc_registration.school_level = 'SLUN' or ovc_registration.school_level = 'SLSE' or ovc_registration.school_level = 'SLPR' or ovc_registration.school_level = 'SLEC')
LEFT OUTER JOIN ovc_school ON ovc_care_education.school_id=ovc_school.id
LEFT OUTER JOIN ovc_household_members ON ovc_registration.caretaker_id=ovc_household_members.person_id
LEFT OUTER JOIN reg_persons_external_ids as exids on exids.person_id=ovc_registration.person_id and exids.identifier_type_id = 'ISOV'
LEFT OUTER JOIN reg_persons_external_ids as exidd on exidd.person_id=ovc_registration.person_id and exidd.identifier_type_id = 'IPWD'
WHERE ovc_registration.child_cbo_id IN ({cbos})
AND ovc_registration.is_void = False
and ovc_registration.registration_date between '{start_date}' and '{end_date}'
ORDER BY child_chv_id ASC, reg_persons_geo.id DESC, ovc_care_education.created_at DESC;
'''

# Registration List
QUERIES['registration_list'] = '''
select reg_org_unit.org_unit_name AS CBO,
reg_person.first_name, reg_person.other_names, reg_person.surname,
reg_person.date_of_birth, registration_date,
date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) AS age,
date_part('year', age(ovc_registration.registration_date,
reg_person.date_of_birth)) AS age_at_reg,
ovc_registration.org_unique_id as OVCID, list_geo.area_name as ward,
scc.area_name as constituency, cc.area_name as county,
CASE
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE has_bcert WHEN 'True' THEN 'HAS BIRTHCERT' ELSE 'NO BIRTHCERT' END AS BirthCert,
CASE has_bcert WHEN 'True' THEN exids.identifier ELSE NULL END AS BCertNumber,
CASE is_disabled WHEN 'True' THEN 'HAS DISABILITY' ELSE 'NO DISABILITY' END AS OVCDisability,
CASE is_Disabled WHEN 'True' THEN exidd.identifier ELSE NULL END AS NCPWDNumber,
CASE
WHEN ovc_registration.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN ovc_registration.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE ovc_registration.hiv_status WHEN 'HSTP' THEN 'ART' ELSE NULL END AS ARTStatus,
concat(chw.first_name,' ',chw.other_names,' ',chw.surname) as CHW,
concat(cgs.first_name,' ',cgs.other_names,' ',cgs.surname) as parent_names,
CASE is_active WHEN 'True' THEN 'ACTIVE' ELSE 'EXITED' END AS Exit_status,
CASE is_active WHEN 'False' THEN exit_date ELSE NULL END AS Exit_date,
exits.item_description as Exit_reason,
CASE
WHEN ovc_registration.school_level = 'SLTV' THEN 'Tertiary'
WHEN ovc_registration.school_level = 'SLUN' THEN 'University'
WHEN ovc_registration.school_level = 'SLSE' THEN 'Secondary'
WHEN ovc_registration.school_level = 'SLPR' THEN 'Primary'
WHEN ovc_registration.school_level = 'SLEC' THEN 'ECDE'
ELSE 'Not in School' END AS Schoollevel,
CASE immunization_status
WHEN 'IMFI' THEN 'Fully Immunized'
WHEN 'IMNI' THEN 'Not Immunized'
WHEN 'IMNC' THEN 'Not Completed'
ELSE 'Not Known' END AS immunization,
eligs.item_description as eligibility,
distinct(ovc_registration.person_id) as ovc_cpims_id,
ovc_care_health.date_linked, ovc_care_health.ccc_number,
ovc_facility.facility_name as facility,
ovc_care_education.school_class as class,
ovc_school.school_name as school,
CASE
WHEN ovc_household_members.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN ovc_household_members.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS CaregiverHIVstatus
from ovc_registration
left outer join reg_person on person_id=reg_person.id
left outer join reg_person chw on child_chv_id=chw.id
left outer join reg_person cgs on caretaker_id=cgs.id
left outer join list_general as exits on exits.item_id=ovc_registration.exit_reason and
exits.field_name='exit_reason_id'
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
left outer join reg_persons_geo on
ovc_registration.person_id=reg_persons_geo.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id and reg_persons_geo.area_id > 337
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id
left outer join ovc_facility on ovc_care_health.facility_id=ovc_facility.id
LEFT OUTER JOIN ovc_care_education ON ovc_care_education.person_id=ovc_registration.person_id
left outer join ovc_school on ovc_care_education.school_id=ovc_school.id
left outer join ovc_household_members ON
ovc_registration.caretaker_id=ovc_household_members.person_id
left outer join ovc_eligibility on ovc_eligibility.person_id=ovc_registration.person_id
left outer join list_general as eligs on eligs.item_id=ovc_eligibility.criteria and
eligs.field_name='eligibility_criteria_id'
LEFT OUTER JOIN reg_persons_external_ids as exids on
exids.person_id=ovc_registration.person_id and exids.identifier_type_id = 'ISOV'
LEFT OUTER JOIN reg_persons_external_ids as exidd on
exidd.person_id=ovc_registration.person_id and exidd.identifier_type_id = 'IPWD'
where reg_persons_geo.is_void = False
and child_cbo_id in ({cbos}) and ovc_registration.is_void = False
and ovc_registration.registration_date between '{start_date}' and '{end_date}'
order by child_chv_id ASC, reg_person.date_of_birth ASC, reg_persons_geo.id,
ovc_care_education.created_at DESC;'''

# PEPFAR
QUERIES['pepfar'] = '''
select
cast(count(distinct ovc_care_events.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_care_services.service_provided
WHEN 'HC1S' THEN 'Health' {domains}
ELSE 'Unknown'
END AS Domain
from ovc_care_services
INNER JOIN ovc_care_events ON ovc_care_events.event=ovc_care_services.event_id
INNER JOIN reg_person ON ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON ovc_care_events.person_id=ovc_registration.person_id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
WHERE reg_persons_geo.is_void = False
and ovc_care_services.is_void = False
and ovc_care_events.event_type_id='FSAM'
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and ovc_registration.child_cbo_id in ({cbos})
GROUP BY ovc_care_services.service_provided, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ward, constituency, county;'''

# PEPFAR SUMMARY
QUERIES['pepfar_summary'] = '''
SELECT 
CAST(COUNT(DISTINCT ovc_registration.person_id) AS integer) AS OVCCount,
reg_org_unit.org_unit_name as CBO,reg_org_unit.id as cboid
into TEMP temp_Actives
from (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1)  derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_registration LEFT OUTER JOIN
         reg_person ON ovc_registration.person_id = reg_person.id LEFT OUTER JOIN
         reg_person AS chw ON ovc_registration.child_chv_id = chw.id LEFT OUTER JOIN
         reg_person AS cgs ON ovc_registration.caretaker_id = cgs.id LEFT OUTER JOIN
         reg_org_unit ON ovc_registration.child_cbo_id = reg_org_unit.id LEFT OUTER JOIN
         reg_persons_geo ON ovc_registration.person_id = reg_persons_geo.person_id ON list_geo.area_id = reg_persons_geo.area_id
where ovc_registration.child_cbo_id IN ({cbos}) and ((is_active = 'True' and ovc_registration.registration_date <= '{end_date}') 
	or (is_active = 'False' and  (ovc_registration.registration_date between '{start_date}' and '{end_date}' )) 
	or (is_active = 'False' and ovc_registration.registration_date <= '{start_date}'  and exit_date > '{end_date}' ) 
	or (is_active = 'False' and ovc_registration.registration_date <= '{start_date}'  and exit_date between '{start_date}' and '{end_date}' )
										)
	group by reg_org_unit.org_unit_name,reg_org_unit.id ;								
SELECT CAST(COUNT(DISTINCT person_id) AS integer) AS OVCCount, CBO, ward, County,AgeRange,
tbl_pepfar.cboid,tbl_pepfar.countyid,CASE sex_id WHEN 'SMAL' THEN 'Female' ELSE 'Male' END AS Gender,derived_Actives.CboActive
FROM
(
SELECT ovc_care_events.person_id, reg_org_unit.org_unit_name AS CBO, list_geo.area_name AS ward, list_general.item_description, 
derivedtbl_1.area_name as County,
reg_person.sex_id,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,reg_org_unit.id as cboid,list_geo.parent_area_id as Countyid
FROM  (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1) AS derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_care_services INNER JOIN
         ovc_care_events ON ovc_care_events.event = ovc_care_services.event_id INNER JOIN
         reg_person ON ovc_care_events.person_id = reg_person.id INNER JOIN
         list_general ON ovc_care_services.service_provided = list_general.item_id LEFT OUTER JOIN
         ovc_registration ON ovc_care_events.person_id = ovc_registration.person_id LEFT OUTER JOIN
         reg_org_unit ON reg_org_unit.id = ovc_registration.child_cbo_id LEFT OUTER JOIN
         reg_persons_geo ON reg_persons_geo.person_id = ovc_registration.person_id ON list_geo.area_id = reg_persons_geo.area_id
WHERE ovc_registration.child_cbo_id IN ({cbos}) AND (ovc_care_services.is_void = 'False') AND 
(ovc_care_events.event_type_id = 'FSAM') AND (ovc_care_events.date_of_event BETWEEN '{start_date}' AND '{end_date}')
GROUP BY ovc_care_events.person_id,ovc_care_services.service_provided, reg_person.date_of_birth, reg_person.sex_id, 
ovc_registration.child_cbo_id, reg_org_unit.org_unit_name, reg_persons_geo.area_id, list_geo.area_name, list_general.item_description,
derivedtbl_1.area_name,date_part('year', age(reg_person.date_of_birth)),reg_org_unit.id ,list_geo.parent_area_id
UNION
SELECT ovc_care_events.person_id, reg_org_unit.org_unit_name AS CBO, list_geo.area_name AS ward, list_general.item_description, 
derivedtbl_1.area_name as County,
reg_person.sex_id,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,reg_org_unit.id as cboid,list_geo.parent_area_id as Countyid
FROM  (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1) AS derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_care_assessment INNER JOIN
         ovc_care_events ON ovc_care_events.event = ovc_care_assessment.event_id INNER JOIN
         reg_person ON ovc_care_events.person_id = reg_person.id INNER JOIN
         list_general ON ovc_care_assessment.service = list_general.item_id LEFT OUTER JOIN
         ovc_registration ON ovc_care_events.person_id = ovc_registration.person_id LEFT OUTER JOIN
         reg_org_unit ON reg_org_unit.id = ovc_registration.child_cbo_id LEFT OUTER JOIN
         reg_persons_geo ON reg_persons_geo.person_id = ovc_registration.person_id ON list_geo.area_id = reg_persons_geo.area_id
WHERE ovc_registration.child_cbo_id IN ({cbos}) AND (ovc_care_assessment.domain in ('DHNU','DPSS')) and (ovc_care_assessment.is_void = 'False') 
AND (ovc_care_events.event_type_id = 'FSAM') AND (ovc_care_events.date_of_event BETWEEN '{start_date}' AND '{end_date}')
GROUP BY ovc_care_events.person_id,ovc_care_assessment.service, reg_person.date_of_birth, reg_person.sex_id, 
ovc_registration.child_cbo_id, reg_org_unit.org_unit_name, reg_persons_geo.area_id, list_geo.area_name, 
list_general.item_description,derivedtbl_1.area_name,date_part('year', age(reg_person.date_of_birth)),reg_org_unit.id ,list_geo.parent_area_id) tbl_pepfar
INNER JOIN
(select ovccount as cboActive,cboid from temp_Actives) derived_Actives ON derived_Actives.cboid = tbl_pepfar.cboid
group by CBO, ward, County,AgeRange,tbl_pepfar.cboid,tbl_pepfar.countyid,Gender,CboActive;
'''

# DATIM
QUERIES['datim'] = '''
select
cast(count(distinct ovc_registration.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_registration.hiv_status
WHEN 'HSTP' THEN '2a. (i) OVC_HIVSTAT: HIV+'
WHEN 'HSTN' THEN '2b. OVC_HIVSTAT: HIV-'
ELSE '2c. OVC_HIVSTAT: HIV Status NOT Known'
END AS Domain,
0 as Wardactive, 0 as WARDGraduated, 0 as WARDTransferred,
0 as WARDExitedWithoutGraduation
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
WHERE reg_persons_geo.is_void = False
and ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
and ((ovc_registration.is_active = True and ovc_registration.registration_date <= '{end_date}') 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= '{end_date}' 
and ovc_registration.exit_date <= '{end_date}' )) 
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ovc_registration.hiv_status, ward, constituency, county
;'''

'''
# Remove >=18 and not in school clause in query
and not (ovc_registration.school_level = 'SLNS'
and date_part('year', '{end_date}'::date) -
date_part('year', reg_person.date_of_birth::date) > 17)
'''

# DATIM - Served
QUERIES['datim_1'] = '''
select 
cast(count(distinct ovc_care_events.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
'1. OVC_Serv' as Domain
from ovc_care_services
INNER JOIN ovc_care_events ON ovc_care_events.event=ovc_care_services.event_id
INNER JOIN reg_person ON ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON ovc_care_events.person_id=ovc_registration.person_id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
WHERE reg_persons_geo.is_void = False
and ovc_care_services.is_void = False 
and ovc_care_events.event_type_id='FSAM'
and ovc_care_events.date_of_event between '{datim_start_date}' and '{end_date}'
and ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
and ((ovc_registration.is_active = True and ovc_registration.registration_date <= '{end_date}') 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= '{end_date}' 
and ovc_registration.exit_date <= '{end_date}' )) 
GROUP BY reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ward, constituency, county;'''

# DATIM ART
QUERIES['datim_2'] = '''
select
cast(count(distinct ovc_registration.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_care_health.art_status
WHEN 'ARAR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
WHEN 'ARPR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
ELSE '2a. (iii) OVC_HIVSTAT: HIV+ NOT on ARV Treatment'
END AS Domain,
0 as Wardactive, 0 as WARDGraduated, 0 as WARDTransferred,
0 as WARDExitedWithoutGraduation
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
WHERE reg_persons_geo.is_void = False
AND ovc_registration.hiv_status = 'HSTP'
and ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
and ((ovc_registration.is_active = True and ovc_registration.registration_date <= '{end_date}') 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= '{end_date}' 
and ovc_registration.exit_date <= '{end_date}' ))
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id, list_geo.parent_area_id,
ovc_registration.hiv_status, ovc_registration.art_status,
ward, constituency, county;'''
# Remove LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id

# Datim Ward summary
QUERIES['datim_3'] = '''
SELECT *
FROM crosstab(
  'select cast(ward as text), graduation,
  cast(sum(ccount) as integer) as ovcs from (
select cast(count(*) as integer) as ccount,
list_geo.area_name as ward,
case exit_reason
WHEN ''ERDE'' THEN ''WARDExitedWithoutGraduation''
WHEN ''EROE'' THEN ''WARDGraduated''
WHEN ''ERFI'' THEN ''WARDGraduated''
WHEN ''ERFR'' THEN ''WARDGraduated''
WHEN ''ERFS'' THEN ''WARDGraduated''
WHEN ''ERAD'' THEN ''WARDGraduated''
WHEN ''ERSE'' THEN ''WARDGraduated''
WHEN ''ERIN'' THEN ''WARDExitedWithoutGraduation''
WHEN ''ERRL'' THEN ''WARDTransferred''
WHEN ''ERDU'' THEN ''WARDTransferred''
WHEN ''ERTR'' THEN ''WARDGraduated''
WHEN ''ERLW'' THEN ''WARDExitedWithoutGraduation''
WHEN ''ERMA'' THEN ''WARDExitedWithoutGraduation''
WHEN ''ERTL'' THEN ''WARDTransferred''
WHEN ''ERDO'' THEN ''WARDExitedWithoutGraduation''
else ''WardActive'' END AS Graduation
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_persons_geo
ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
WHERE reg_persons_geo.is_void = False
and ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
and ((ovc_registration.is_active = True and ovc_registration.registration_date <= ''{end_date}'' ) 
or (ovc_registration.is_active = False and ovc_registration.registration_date <= ''{end_date}'' 
and ovc_registration.exit_date <= ''{end_date}'' )) 
group by exit_reason, list_geo.area_name order by ward) as wc
group by ward, graduation order by 1,2')
AS ct("ward" text, "WardActive" int, "WARDGraduated" int,
"WARDTransferred" int, "WARDExitedWithoutGraduation" int);;'''

# KPI
QUERIES['kpi'] = '''
select
cast(count(distinct ovc_registration.person_id) as integer) as OVCCount,
ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name,
reg_persons_geo.area_id,
list_geo.area_name,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_care_health.art_status
WHEN 'ARAR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
WHEN 'ARPR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
ELSE '2a. (iii) OVC_HIVSTAT: HIV+ NOT on ARV Treatment'
END AS Domain
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id
WHERE reg_persons_geo.is_void = False
and ovc_registration.is_active = True
AND ovc_registration.hiv_status = 'HSTP'
%s
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ovc_registration.hiv_status, list_geo.area_name, ovc_care_health.art_status;'''

QUERIES['served'] = '''
SELECT * FROM (%s) a
INNER JOIN (%s) b
ON a.ward = b.ward;'''

# NOT SERVED LIST
QUERIES['served_list'] = '''
select person_id from(
select person_id, count(person_id) as scnts
from(
select person_id, domain, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id = ovc_registration.person_id
where ovc_registration.child_cbo_id in ({cbos})
and ovc_registration.is_active = True AND ovc_registration.is_void = False
and domain in ('DHNU', 'DPSS')
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
     or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
     or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
     or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
     or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
     or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
     or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
     or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
     or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
     or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
     or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id = ovc_registration.person_id
where ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}') as dcs
group by person_id, domain) as scounts
group by person_id) as fp where scnts > 0'''

# NOT Served
QUERIES['not_served'] = '''
select reg_org_unit.org_unit_name AS CBO,
reg_person.first_name, reg_person.surname,
reg_person.other_names, reg_person.date_of_birth, registration_date,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
date_part('year', age(ovc_registration.registration_date,
reg_person.date_of_birth)) AS age_at_reg,
child_cbo_id as OVCID,
list_geo.area_name as ward, scc.area_name as constituency, cc.area_name as county,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', 
age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE has_bcert WHEN 'True' THEN 'HAS BIRTHCERT' ELSE 'NO BIRTHCERT' END AS BirthCert,
CASE has_bcert WHEN 'True' THEN 'BCERT' ELSE NULL END AS BCertNumber,
CASE is_disabled WHEN 'True' THEN 'HAS DISABILITY' ELSE 'NO DISABILITY' END AS OVCDisability,
CASE is_Disabled WHEN 'True' THEN 'NCPWD' ELSE NULL END AS NCPWDNumber,
CASE
WHEN hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE hiv_status WHEN 'HSTP' THEN 'ART' ELSE NULL END AS ARTStatus,
concat(chw.first_name,' ',chw.surname,' ',chw.other_names) as CHW,
concat(cgs.first_name,' ',cgs.surname,' ',cgs.other_names) as parent_names,
CASE is_active WHEN 'True' THEN 'ACTIVE' ELSE 'EXITED' END AS Exit_status,
CASE is_active WHEN 'False' THEN exit_date ELSE NULL END AS Exit_date,
CASE
WHEN school_level = 'SLTV' THEN 'Tertiary'
WHEN school_level = 'SLUN' THEN 'University'
WHEN school_level = 'SLSE' THEN 'Secondary'
WHEN school_level = 'SLPR' THEN 'Primary'
WHEN school_level = 'SLEC' THEN 'ECDE'
ELSE 'Not in School' END AS Schoollevel,
CASE immunization_status
WHEN 'IMFI' THEN 'Fully Immunized'
WHEN 'IMNI' THEN 'Not Immunized'
WHEN 'IMNC' THEN 'Not Completed'
ELSE 'Not Known' END AS immunization
from ovc_registration
left outer join reg_person on person_id=reg_person.id
left outer join reg_person chw on child_chv_id=chw.id
left outer join reg_person cgs on caretaker_id=cgs.id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
left outer join reg_persons_geo on ovc_registration.person_id=reg_persons_geo.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.is_void = False
and child_cbo_id in ({cbos})
and ovc_registration.person_id not in (%s)
and ovc_registration.is_active = True AND ovc_registration.is_void = False
order by child_chv_id ASC,
reg_person.date_of_birth ASC;''' % (QUERIES['served_list'])
# and ovc_registration.registration_date between '{start_date}' and '{end_date}'


# PEPFAR DETAILED SUMMARY
QUERIES['pepfar_detailed'] = '''
select * FROM (
select cast('CBO' as text) as level,
CASE
WHEN scnts = 0 THEN 'Not Served' 
WHEN scnts = 1 THEN '1 or 2 Services' 
WHEN scnts = 2 THEN '1 or 2 Services' 
WHEN scnts > 2 THEN '3 or More Services' END AS Services,
Gender, age, AgeRange, CBO as name, count(scnts) AS OVCCOUNT from(
select person_id, count(person_id) as scnts, Gender, age, AgeRange, CBO
from(
select person_id, domain, Gender, age, AgeRange, CBO, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
reg_org_unit.org_unit_name AS CBO
 from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
left outer join reg_org_unit on ovc_registration.child_cbo_id=reg_org_unit.id
where domain in ('DHNU', 'DPSS')
AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
    or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
    or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
    or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
    or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
    or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
    or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
    or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
    or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
    or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
    or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain,
 CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
reg_org_unit.org_unit_name AS CBO
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
left outer join reg_org_unit on ovc_registration.child_cbo_id=reg_org_unit.id
where  ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})) as dcs
group by person_id, domain, Gender, age, AgeRange, CBO) as scounts
group by person_id, Gender, age, AgeRange, CBO
union all
select ovc_registration.person_id, 0 as scnts,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
reg_org_unit.org_unit_name AS CBO
 from ovc_registration
 inner join reg_person on reg_person.id = ovc_registration.person_id
 left outer join reg_org_unit on ovc_registration.child_cbo_id=reg_org_unit.id
 where ovc_registration.is_active = True AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.person_id not in
(
select person_id from(
select person_id, count(person_id) as scnts
from(
select person_id, domain, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id = ovc_registration.person_id
where ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.is_void = False
and domain in ('DHNU', 'DPSS')
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
     or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
     or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
     or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
     or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
     or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
     or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
     or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
     or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
     or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
     or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id = ovc_registration.person_id
where ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}') as dcs
group by person_id, domain) as scounts
group by person_id) as fp where scnts > 0
)
 ) as fp group by Gender, age, AgeRange, scnts, cbo) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
reg_org_unit.org_unit_name as name
from ovc_registration
inner join reg_org_unit on reg_org_unit.id = ovc_registration.child_cbo_id
WHERE ovc_registration.is_active = True AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
group by ovc_registration.child_cbo_id, name) b
ON a.name = b.name;'''

# Blanks to fill up all services, ages, genders
QUERIES['pepfar_detailed_blank'] = '''
select * FROM (
select cast('CBO' as text) as level,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) < 15 THEN cast('1 or 2 Services' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) BETWEEN 15 AND 28 THEN cast('3 or More Services' as text)
ELSE cast('Not Served' as text) END AS Services,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (
1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41) THEN cast('Female' as text)
ELSE cast('Male' as text) END AS Gender,
0 as age,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (1,2,15,16,29,30) THEN cast('a.[<1yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (3,4,16,17,31,32) THEN cast('b.[1-4yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (5,6,18,19,33,34) THEN cast('c.[5-9yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (7,8,20,21,35,36) THEN cast('d.[10-14yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (9,10,22,23,37,38) THEN cast('e.[15-17yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (11,12,24,25,39,40) THEN cast('f.[18-24yrs]' as text)
ELSE cast('g.[25+yrs]' as text) END AS AgeRange,
reg_org_unit.org_unit_name AS name,
0 as OVCCOUNT from ovc_registration
left outer join reg_org_unit on ovc_registration.child_cbo_id=reg_org_unit.id
where ovc_registration.child_cbo_id in ({cbos}) limit 42) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
reg_org_unit.org_unit_name as name
from ovc_registration
inner join reg_org_unit on reg_org_unit.id = ovc_registration.child_cbo_id
WHERE ovc_registration.is_active = True AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
group by ovc_registration.child_cbo_id, name) b
ON a.name = b.name;'''

# For constituency
QUERIES['pepfar_detailed_1'] = '''
select * FROM (
select cast('Ward' as text) as level,
CASE
WHEN scnts = 0 THEN 'Not Served' 
WHEN scnts = 1 THEN '1 or 2 Services' 
WHEN scnts = 2 THEN '1 or 2 Services' 
WHEN scnts > 2 THEN '3 or More Services' END AS Services,
Gender, age, AgeRange, scounty as name, count(scnts) AS OVCCOUNT from(
select person_id, count(person_id) as scnts, Gender, age, AgeRange, scounty
from(
select person_id, domain, Gender, age, AgeRange, scounty, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
list_geo.area_name as scounty
 from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
where reg_persons_geo.is_void = False
and domain in ('DHNU', 'DPSS')
and ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
    or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
    or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
    or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
    or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
    or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
    or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
    or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
    or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
    or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
    or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain,
 CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
list_geo.area_name AS scounty
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
where reg_persons_geo.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})) as dcs
group by person_id, domain, Gender, age, AgeRange, scounty) as scounts
group by person_id, Gender, age, AgeRange, scounty
union all
select ovc_registration.person_id, 0 as scnts,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
list_geo.area_name AS scounty
 from ovc_registration
 inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
where reg_persons_geo.is_void = False
and ovc_registration.is_active = True AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.person_id not in
(
select person_id from(
select person_id, count(person_id) as scnts
from(
select person_id, domain, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id = ovc_registration.person_id
where ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.is_void = False
and domain in ('DHNU', 'DPSS')
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
     or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
     or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
     or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
     or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
     or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
     or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
     or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
     or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
     or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
     or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id = ovc_registration.person_id
where ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}') as dcs
group by person_id, domain) as scounts
group by person_id) as fp where scnts > 0
)
 ) as fp group by Gender, age, AgeRange, scnts, scounty) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
list_geo.area_name AS name
from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
where reg_persons_geo.is_void = False
AND ovc_registration.is_active = True AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
group by name) b
ON a.name = b.name;'''

# For consituency blanks
QUERIES['pepfar_detailed_blank_1'] = '''
select * FROM (
select cast('Ward' as text) as level,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) < 15 THEN cast('1 or 2 Services' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) BETWEEN 15 AND 28 THEN cast('3 or More Services' as text)
ELSE cast('Not Served' as text) END AS Services,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (
1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41) THEN cast('Female' as text)
ELSE cast('Male' as text) END AS Gender,
0 as age,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (1,2,15,16,29,30) THEN cast('a.[<1yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (3,4,16,17,31,32) THEN cast('b.[1-4yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (5,6,18,19,33,34) THEN cast('c.[5-9yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (7,8,20,21,35,36) THEN cast('d.[10-14yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (9,10,22,23,37,38) THEN cast('e.[15-17yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (11,12,24,25,39,40) THEN cast('f.[18-24yrs]' as text)
ELSE cast('g.[25+yrs]' as text) END AS AgeRange,
list_geo.area_name AS name,
0 as OVCCOUNT from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
where reg_persons_geo.is_void = False
and ovc_registration.child_cbo_id in ({cbos}) limit 42) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
list_geo.area_name as name
from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
where reg_persons_geo.is_void = False
AND ovc_registration.is_active = True AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
group by name) b
ON a.name = b.name;'''

# For County
QUERIES['pepfar_detailed_2'] = '''
select * FROM (
select cast('County' as text) as level,
CASE
WHEN scnts = 0 THEN 'Not Served' 
WHEN scnts = 1 THEN '1 or 2 Services' 
WHEN scnts = 2 THEN '1 or 2 Services' 
WHEN scnts > 2 THEN '3 or More Services' END AS Services,
Gender, age, AgeRange, scounty as name, count(scnts) AS OVCCOUNT from(
select person_id, count(person_id) as scnts, Gender, age, AgeRange, scounty
from(
select person_id, domain, Gender, age, AgeRange, scounty, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
cc.area_name AS scounty
 from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.is_void = False
and domain in ('DHNU', 'DPSS')
and ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
    or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
    or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
    or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
    or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
    or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
    or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
    or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
    or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
    or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
    or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain,
 CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
cc.area_name AS scounty
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id=ovc_registration.person_id
inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})) as dcs
group by person_id, domain, Gender, age, AgeRange, scounty) as scounts
group by person_id, Gender, age, AgeRange, scounty
union all
select ovc_registration.person_id, 0 as scnts,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
 date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
 CASE
WHEN date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
cc.area_name AS scounty
 from ovc_registration
 inner join reg_person on reg_person.id = ovc_registration.person_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.is_void = False
and ovc_registration.is_active = True AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.person_id not in
(
select person_id from(
select person_id, count(person_id) as scnts
from(
select person_id, domain, count(distinct(domain)) as domaincount from (
select ovc_registration.person_id, event_type_id, domain from ovc_care_assessment
inner join ovc_care_events on ovc_care_assessment.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id = ovc_registration.person_id
where ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.is_void = False
and domain in ('DHNU', 'DPSS')
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
union all
select ovc_registration.person_id, event_type_id,
CASE
  WHEN (service_provided = 'SC1S' or service_provided = 'SC2S' or service_provided = 'SC3S'
     or service_provided = 'SC4S' or service_provided = 'SC5S' or service_provided = 'SC6S'
     or service_provided = 'SC7S') THEN 'DSHC'
  WHEN (service_provided = 'PS1S' or service_provided = 'PS2S' or service_provided = 'PS3S'
     or service_provided = 'PS4S' or service_provided = 'PS5S') THEN 'DPSS'
  WHEN (service_provided = 'PT1S' or service_provided = 'PT2S' or service_provided = 'PT3S'
     or service_provided = 'PT4S' or service_provided = 'PT5S') THEN 'DPRO'
  WHEN (service_provided = 'HE1S' or service_provided = 'HE2S' or service_provided = 'HE3S'
     or service_provided = 'HE4S') THEN 'DHES'
  WHEN (service_provided = 'HC1S' or service_provided = 'HC2S' or service_provided = 'HC3S'
     or service_provided = 'HC4S' or service_provided = 'HC5S' or service_provided = 'HC6S'
     or service_provided = 'HC7S' or service_provided = 'HC8S' or service_provided = 'HC9S'
     or service_provided = 'HC10S') THEN 'DHNU'
  WHEN (service_provided = 'SE1S' or service_provided = 'SE2S' or service_provided = 'SE3S'
     or service_provided = 'SE4S' or service_provided = 'SE5S' or service_provided = 'SE6S'
     or service_provided = 'SE7S' or service_provided = 'SE8S') THEN 'DEDU'
  ELSE 'NULL'
 END AS domain
from ovc_care_services
inner join ovc_care_events on ovc_care_services.event_id=ovc_care_events.event
inner join ovc_registration on ovc_care_events.person_id = ovc_registration.person_id
where ovc_registration.child_cbo_id in ({cbos})
AND ovc_registration.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}') as dcs
group by person_id, domain) as scounts
group by person_id) as fp where scnts > 0
)
 ) as fp group by Gender, age, AgeRange, scnts, scounty) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
cc.area_name as name
from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.is_void = False
AND ovc_registration.is_active = True AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
group by name) b
ON a.name = b.name;'''

# For county blank
QUERIES['pepfar_detailed_blank_2'] = '''
select * FROM (
select cast('County' as text) as level,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) < 15 THEN cast('1 or 2 Services' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) BETWEEN 15 AND 28 THEN cast('3 or More Services' as text)
ELSE cast('Not Served' as text) END AS Services,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (
1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41) THEN cast('Female' as text)
ELSE cast('Male' as text) END AS Gender,
0 as age,
CASE
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (1,2,15,16,29,30) THEN cast('a.[<1yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (3,4,16,17,31,32) THEN cast('b.[1-4yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (5,6,18,19,33,34) THEN cast('c.[5-9yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (7,8,20,21,35,36) THEN cast('d.[10-14yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (9,10,22,23,37,38) THEN cast('e.[15-17yrs]' as text)
WHEN ROW_NUMBER () OVER (ORDER BY ovc_registration ASC) IN (11,12,24,25,39,40) THEN cast('f.[18-24yrs]' as text)
ELSE cast('g.[25+yrs]' as text) END AS AgeRange,
cc.area_name AS name,
0 as OVCCOUNT from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.is_void = False
and ovc_registration.child_cbo_id in ({cbos}) limit 42) a
INNER JOIN (
select count(ovc_registration.person_id) as active,
cc.area_name as name
from ovc_registration
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
where reg_persons_geo.is_void = False
AND ovc_registration.is_active = True AND ovc_registration.is_void = False
and ovc_registration.child_cbo_id in ({cbos})
group by name) b
ON a.name = b.name;'''

# Form 1B summary
QUERIES['form1b_summary'] = '''
select count(ovc_care_events.person_id) as CGCOUNT,
reg_org_unit.org_unit_name as CBO,
list_general.item_description as Service,
list_geo.area_name as ward, scc.area_name as constituency,
cc.area_name as county,
CASE domain WHEN 'DSHC' THEN 'Shelter and Care'
WHEN 'DPSS' THEN 'Psychosocial Support'
WHEN 'DPRO' THEN 'Protection'
WHEN 'DHES' THEN 'HouseHold Economic Strengthening'
WHEN 'DHNU' THEN 'Health and Nutrition'
ELSE 'Education' END AS Domain,
CASE right(entity, 1) WHEN 's' THEN 'Service' ELSE 'Assessment'
END AS visittype,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
CASE WHEN date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) < 50 THEN 'a.Below 50'
ELSE 'b.50+ years ' END AS AgeRange
from ovc_care_f1b
inner join ovc_care_events on event_id=ovc_care_events.event
left outer join reg_person on ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON
ovc_care_events.person_id=ovc_registration.caretaker_id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
LEFT OUTER JOIN reg_persons_geo ON
reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
left outer join list_general on entity=list_general.item_id
where ovc_registration.is_active = True
and ovc_registration.child_cbo_id in ({cbos})
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and list_general.field_name = 'form1b_items'
group by ovc_care_events.person_id, domain, entity,
reg_person.sex_id, reg_org_unit.org_unit_name, reg_person.date_of_birth,
list_geo.area_name, scc.area_name, cc.area_name, list_general.item_description
'''
# Form 1A summary
QUERIES['form1a_summary'] = '''
select count(ovc_care_events.person_id) as OVCCOUNT,
reg_org_unit.org_unit_name as CBO,
list_general.item_description as Service,
service_provided as Service_ID,
list_geo.area_name as ward, scc.area_name as constituency,
cc.area_name as county,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) AS age,
CASE list_general.field_name
WHEN 'olmis_shelter_service_id' THEN 'Shelter and Care'
WHEN 'olmis_pss_service_id' THEN 'Psychosocial Support'
WHEN 'olmis_protection_service_id' THEN 'Protection'
WHEN 'olmis_hes_service_id' THEN 'HouseHold Economic Strengthening'
WHEN 'olmis_health_service_id' THEN 'Health and Nutrition'
WHEN 'olmis_education_service_id' THEN 'Education'
ELSE 'Unknown' END AS Domain,
CASE
WHEN ovc_registration.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN ovc_registration.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE
WHEN ovc_household_members.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN ovc_household_members.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS CaregiverHIVstatus,
CASE ovc_registration.is_active
WHEN 'True' THEN 'ACTIVE' ELSE 'EXITED' END AS Exit_status,
exits.item_description as Exit_reason,
CASE ovc_registration.is_active
WHEN 'False' THEN ovc_registration.exit_date ELSE NULL END AS Exit_date,
CASE
WHEN ovc_registration.school_level = 'SLTV' THEN 'Tertiary'
WHEN ovc_registration.school_level = 'SLUN' THEN 'University'
WHEN ovc_registration.school_level = 'SLSE' THEN 'Secondary'
WHEN ovc_registration.school_level = 'SLPR' THEN 'Primary'
WHEN ovc_registration.school_level = 'SLEC' THEN 'ECDE'
ELSE 'Not in School' END AS Schoollevel,
CASE
WHEN date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange
from ovc_care_services
inner join ovc_care_events on event_id=ovc_care_events.event
inner join reg_person on ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON
ovc_care_events.person_id=ovc_registration.person_id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
LEFT OUTER JOIN reg_persons_geo ON
reg_persons_geo.person_id=ovc_registration.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
left outer join list_general as exits on
exits.item_id=ovc_registration.exit_reason and
exits.field_name='exit_reason_id'
left outer join list_general on service_provided=list_general.item_id
left outer join ovc_household_members ON
ovc_registration.caretaker_id=ovc_household_members.person_id
where ovc_registration.child_cbo_id in ({cbos})
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and service_provided != '' and service_provided is not null
group by ovc_care_events.person_id, service_provided,
list_geo.area_name, scc.area_name, cc.area_name,
reg_person.sex_id, reg_person.date_of_birth,
list_general.item_description, list_general.field_name,
ovc_registration.school_level, ovc_registration.is_active,
ovc_registration.hiv_status, ovc_registration.exit_date,
ovc_household_members.hiv_status, reg_org_unit.org_unit_name,
exits.item_description
'''

# List of OVC Served
QUERIES['ovc_served_list'] = '''
select reg_person.id AS cpims_id,
concat(reg_person.first_name,' ',reg_person.other_names,' ',reg_person.surname) as NAMES,
reg_person.date_of_birth as ovc_dob,
reg_org_unit.org_unit_name as CBO,
list_general.item_description as Service,
ovc_care_events.date_of_event as date_of_service,
list_geo.area_name as ward, scc.area_name as constituency,
cc.area_name as county,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
ovc_registration.registration_date,
date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) AS age,
CASE list_general.field_name
WHEN 'olmis_shelter_service_id' THEN 'Shelter and Care'
WHEN 'olmis_pss_service_id' THEN 'Psychosocial Support'
WHEN 'olmis_protection_service_id' THEN 'Protection'
WHEN 'olmis_hes_service_id' THEN 'HouseHold Economic Strengthening'
WHEN 'olmis_health_service_id' THEN 'Health and Nutrition'
WHEN 'olmis_education_service_id' THEN 'Education'
ELSE 'Unknown' END AS Domain,
CASE
WHEN ovc_registration.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN ovc_registration.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE ovc_care_health.art_status
WHEN 'ARAR' THEN 'ART'
WHEN 'ARPR' THEN 'ART'
ELSE NULL END AS ART_STATUS,
ovc_care_health.date_linked, ovc_care_health.ccc_number,
ovc_facility.facility_name as facility,
concat(chw.first_name,' ',chw.surname,' ',chw.other_names) as CHW,
caretaker_id as caregiver_id,
concat(cgs.first_name,' ',cgs.surname,' ',cgs.other_names) as CAREGIVER,
CASE cgs.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS caregiver_gender,
date_part('year', age(timestamp '{end_date}', cgs.date_of_birth)) AS caregiver_age,
cgt.item_description as caregiver_relation,
cgm.person_id as mother_id,
concat(cgmd.first_name,' ',cgmd.other_names,' ',cgmd.surname) as mother,
CASE cgm.member_alive WHEN 'AYES' THEN 'Yes' WHEN 'ANNO' THEN 'Yes' ELSE NULL END AS mother_alive,
CASE cgm.hiv_status WHEN 'HSTP' THEN 'POSITIVE' WHEN 'HSTN' THEN 'NEGATIVE'
WHEN 'HSKN' THEN 'NEGATIVE' ELSE NULL END AS mother_hiv_status,
cgf.person_id as father_id,
concat(cgfd.first_name,' ',cgfd.other_names,' ',cgfd.surname) as father,
CASE cgf.member_alive WHEN 'AYES' THEN 'Yes' WHEN 'ANNO' THEN 'Yes' ELSE NULL END AS father_alive,
CASE cgf.hiv_status WHEN 'HSTP' THEN 'POSITIVE' WHEN 'HSTN' THEN 'NEGATIVE'
WHEN 'HSKN' THEN 'NEGATIVE' ELSE NULL END AS father_hiv_status,
CASE
WHEN hhm.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN hhm.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS CaregiverHIVstatus,
CASE ovc_registration.is_active
WHEN 'True' THEN 'ACTIVE' ELSE 'EXITED' END AS Exit_status,
exits.item_description as Exit_reason,
CASE ovc_registration.is_active
WHEN 'False' THEN ovc_registration.exit_date ELSE NULL END AS Exit_date,
CASE
WHEN ovc_registration.school_level = 'SLTV' THEN 'Tertiary'
WHEN ovc_registration.school_level = 'SLUN' THEN 'University'
WHEN ovc_registration.school_level = 'SLSE' THEN 'Secondary'
WHEN ovc_registration.school_level = 'SLPR' THEN 'Primary'
WHEN ovc_registration.school_level = 'SLEC' THEN 'ECDE'
ELSE 'Not in School' END AS Schoollevel,
CASE
WHEN date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange
from ovc_care_services
inner join ovc_care_events on event_id=ovc_care_events.event
inner join reg_person on ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON
ovc_care_events.person_id=ovc_registration.person_id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
LEFT OUTER JOIN reg_persons_geo ON
reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
left outer join reg_person chw on child_chv_id=chw.id
left outer join reg_person cgs on caretaker_id=cgs.id
left outer join list_general as exits on
exits.item_id=ovc_registration.exit_reason and
exits.field_name='exit_reason_id'
left outer join list_general on service_provided=list_general.item_id
left outer join ovc_household_members as hhm ON
ovc_registration.caretaker_id=hhm.person_id
left outer join ovc_household_members as cgm ON
hhm.house_hold_id=cgm.house_hold_id AND cgm.member_type='CGPM'
left outer join ovc_household_members as cgf ON
hhm.house_hold_id=cgf.house_hold_id AND cgf.member_type='CGPF'
left outer join reg_person as cgmd on cgmd.id=cgm.person_id
left outer join reg_person as cgfd on cgfd.id=cgf.person_id
left outer join list_general AS cgt on hhm.member_type=cgt.item_id AND cgt.field_name='relationship_type_id'
LEFT OUTER JOIN ovc_care_health ON
ovc_care_health.person_id=ovc_registration.person_id
left outer join ovc_facility on ovc_care_health.facility_id=ovc_facility.id
where reg_persons_geo.is_void = False and ovc_registration.child_cbo_id in ({cbos})
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and service_provided != '' and service_provided is not null
'''

# List of OVC Assessed
QUERIES['ovc_assessed_list'] = '''
select reg_person.id AS cpims_id,
concat(reg_person.first_name,' ',reg_person.other_names,' ',reg_person.surname) as NAMES,
reg_person.date_of_birth as ovc_dob,
reg_org_unit.org_unit_name as CBO,
list_general.item_description as Assessment,
ovc_care_events.date_of_event as date_of_assessment,
list_geo.area_name as ward, scc.area_name as constituency,
cc.area_name as county,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
ovc_registration.registration_date,
date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) AS age,
CASE 
WHEN list_general.field_name LIKE 'olmis_education_assessment_id%' THEN 'Education'
WHEN list_general.field_name LIKE 'olmis_shelter_assessment_id%' THEN 'Shelter and Care'
WHEN list_general.field_name LIKE 'olmis_pss_assessment_id%' THEN 'Psychosocial Support'
WHEN list_general.field_name LIKE 'olmis_protection_assessment_id%' THEN 'Protection'
WHEN list_general.field_name LIKE 'olmis_hes_assessment_id%' THEN 'HouseHold Economic Strengthening'
WHEN list_general.field_name LIKE 'olmis_health_assessment_id%' THEN 'Health and Nutrition'
ELSE 'Unknown' END AS Domain,
CASE
WHEN ovc_registration.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN ovc_registration.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE ovc_care_health.art_status
WHEN 'ARAR' THEN 'ART'
WHEN 'ARPR' THEN 'ART'
ELSE NULL END AS ART_STATUS,
ovc_care_health.date_linked, ovc_care_health.ccc_number,
ovc_facility.facility_name as facility,
concat(chw.first_name,' ',chw.surname,' ',chw.other_names) as CHW,
caretaker_id as caregiver_id,
concat(cgs.first_name,' ',cgs.surname,' ',cgs.other_names) as CAREGIVER,
CASE cgs.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS caregiver_gender,
date_part('year', age(timestamp '{end_date}', cgs.date_of_birth)) AS caregiver_age,
cgt.item_description as caregiver_relation,
cgm.person_id as mother_id,
concat(cgmd.first_name,' ',cgmd.other_names,' ',cgmd.surname) as mother,
CASE cgm.member_alive WHEN 'AYES' THEN 'Yes' WHEN 'ANNO' THEN 'Yes' ELSE NULL END AS mother_alive,
CASE cgm.hiv_status WHEN 'HSTP' THEN 'POSITIVE' WHEN 'HSTN' THEN 'NEGATIVE'
WHEN 'HSKN' THEN 'NEGATIVE' ELSE NULL END AS mother_hiv_status,
cgf.person_id as father_id,
concat(cgfd.first_name,' ',cgfd.other_names,' ',cgfd.surname) as father,
CASE cgf.member_alive WHEN 'AYES' THEN 'Yes' WHEN 'ANNO' THEN 'Yes' ELSE NULL END AS father_alive,
CASE cgf.hiv_status WHEN 'HSTP' THEN 'POSITIVE' WHEN 'HSTN' THEN 'NEGATIVE'
WHEN 'HSKN' THEN 'NEGATIVE' ELSE NULL END AS father_hiv_status,
CASE
WHEN hhm.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN hhm.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS CaregiverHIVstatus,
CASE ovc_registration.is_active
WHEN 'True' THEN 'ACTIVE' ELSE 'EXITED' END AS Exit_status,
exits.item_description as Exit_reason,
CASE ovc_registration.is_active
WHEN 'False' THEN ovc_registration.exit_date ELSE NULL END AS Exit_date,
CASE
WHEN ovc_registration.school_level = 'SLTV' THEN 'Tertiary'
WHEN ovc_registration.school_level = 'SLUN' THEN 'University'
WHEN ovc_registration.school_level = 'SLSE' THEN 'Secondary'
WHEN ovc_registration.school_level = 'SLPR' THEN 'Primary'
WHEN ovc_registration.school_level = 'SLEC' THEN 'ECDE'
ELSE 'Not in School' END AS Schoollevel,
CASE
WHEN date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange
from ovc_care_assessment
inner join ovc_care_events on event_id=ovc_care_events.event
inner join reg_person on ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON
ovc_care_events.person_id=ovc_registration.person_id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
LEFT OUTER JOIN reg_persons_geo ON
reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
left outer join reg_person chw on child_chv_id=chw.id
left outer join reg_person cgs on caretaker_id=cgs.id
left outer join list_general as exits on
exits.item_id=ovc_registration.exit_reason and
exits.field_name='exit_reason_id'
left outer join list_general on service_status=list_general.item_id
left outer join ovc_household_members as hhm ON
ovc_registration.caretaker_id=hhm.person_id
left outer join ovc_household_members as cgm ON
hhm.house_hold_id=cgm.house_hold_id AND cgm.member_type='CGPM'
left outer join ovc_household_members as cgf ON
hhm.house_hold_id=cgf.house_hold_id AND cgf.member_type='CGPF'
left outer join reg_person as cgmd on cgmd.id=cgm.person_id
left outer join reg_person as cgfd on cgfd.id=cgf.person_id
left outer join list_general AS cgt on hhm.member_type=cgt.item_id AND cgt.field_name='relationship_type_id'
LEFT OUTER JOIN ovc_care_health ON
ovc_care_health.person_id=ovc_registration.person_id
left outer join ovc_facility on ovc_care_health.facility_id=ovc_facility.id
where ovc_registration.child_cbo_id in ({cbos})
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and service_status != '' and service_status is not null
'''

# List of OVC Priorities Served
QUERIES['ovc_priority_list'] = '''
select reg_person.id AS cpims_id,
concat(reg_person.first_name,' ',reg_person.other_names,' ',reg_person.surname) as NAMES,
reg_person.date_of_birth as ovc_dob,
reg_org_unit.org_unit_name as CBO,
list_general.item_description as Service,
ovc_care_events.date_of_event as date_of_service,
list_geo.area_name as ward, scc.area_name as constituency,
cc.area_name as county,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS Gender,
ovc_registration.registration_date,
date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) AS age,
CASE list_general.field_name
WHEN 'olmis_shelter_service_id' THEN 'Shelter and Care'
WHEN 'olmis_pss_service_id' THEN 'Psychosocial Support'
WHEN 'olmis_protection_service_id' THEN 'Protection'
WHEN 'olmis_hes_service_id' THEN 'HouseHold Economic Strengthening'
WHEN 'olmis_health_service_id' THEN 'Health and Nutrition'
WHEN 'olmis_education_service_id' THEN 'Education'
ELSE 'Unknown' END AS Domain,
CASE
WHEN ovc_registration.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN ovc_registration.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE ovc_care_health.art_status
WHEN 'ARAR' THEN 'ART'
WHEN 'ARPR' THEN 'ART'
ELSE NULL END AS ART_STATUS,
ovc_care_health.date_linked, ovc_care_health.ccc_number,
ovc_facility.facility_name as facility,
concat(chw.first_name,' ',chw.surname,' ',chw.other_names) as CHW,
caretaker_id as caregiver_id,
concat(cgs.first_name,' ',cgs.surname,' ',cgs.other_names) as CAREGIVER,
CASE cgs.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS caregiver_gender,
date_part('year', age(timestamp '{end_date}', cgs.date_of_birth)) AS caregiver_age,
cgt.item_description as caregiver_relation,
cgm.person_id as mother_id,
concat(cgmd.first_name,' ',cgmd.other_names,' ',cgmd.surname) as mother,
CASE cgm.member_alive WHEN 'AYES' THEN 'Yes' WHEN 'ANNO' THEN 'Yes' ELSE NULL END AS mother_alive,
CASE cgm.hiv_status WHEN 'HSTP' THEN 'POSITIVE' WHEN 'HSTN' THEN 'NEGATIVE'
WHEN 'HSKN' THEN 'NEGATIVE' ELSE NULL END AS mother_hiv_status,
cgf.person_id as father_id,
concat(cgfd.first_name,' ',cgfd.other_names,' ',cgfd.surname) as father,
CASE cgf.member_alive WHEN 'AYES' THEN 'Yes' WHEN 'ANNO' THEN 'Yes' ELSE NULL END AS father_alive,
CASE cgf.hiv_status WHEN 'HSTP' THEN 'POSITIVE' WHEN 'HSTN' THEN 'NEGATIVE'
WHEN 'HSKN' THEN 'NEGATIVE' ELSE NULL END AS father_hiv_status,
CASE
WHEN hhm.hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN hhm.hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS CaregiverHIVstatus,
CASE ovc_registration.is_active
WHEN 'True' THEN 'ACTIVE' ELSE 'EXITED' END AS Exit_status,
exits.item_description as Exit_reason,
CASE ovc_registration.is_active
WHEN 'False' THEN ovc_registration.exit_date ELSE NULL END AS Exit_date,
CASE
WHEN ovc_registration.school_level = 'SLTV' THEN 'Tertiary'
WHEN ovc_registration.school_level = 'SLUN' THEN 'University'
WHEN ovc_registration.school_level = 'SLSE' THEN 'Secondary'
WHEN ovc_registration.school_level = 'SLPR' THEN 'Primary'
WHEN ovc_registration.school_level = 'SLEC' THEN 'ECDE'
ELSE 'Not in School' END AS Schoollevel,
CASE
WHEN date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]'
WHEN  date_part('year', age(timestamp '{end_date}',
reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange
from ovc_care_priority
inner join ovc_care_events on event_id=ovc_care_events.event
inner join reg_person on ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON
ovc_care_events.person_id=ovc_registration.person_id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
LEFT OUTER JOIN reg_persons_geo ON
reg_persons_geo.person_id=ovc_registration.person_id and reg_persons_geo.area_id > 337
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
left outer join list_geo as scc on scc.area_id=list_geo.parent_area_id
left outer join list_geo as cc on cc.area_id=scc.parent_area_id
left outer join reg_person chw on child_chv_id=chw.id
left outer join reg_person cgs on caretaker_id=cgs.id
left outer join list_general as exits on
exits.item_id=ovc_registration.exit_reason and
exits.field_name='exit_reason_id'
left outer join list_general on service=list_general.item_id
left outer join ovc_household_members as hhm ON
ovc_registration.caretaker_id=hhm.person_id
left outer join ovc_household_members as cgm ON
hhm.house_hold_id=cgm.house_hold_id AND cgm.member_type='CGPM'
left outer join ovc_household_members as cgf ON
hhm.house_hold_id=cgf.house_hold_id AND cgf.member_type='CGPF'
left outer join reg_person as cgmd on cgmd.id=cgm.person_id
left outer join reg_person as cgfd on cgfd.id=cgf.person_id
left outer join list_general AS cgt on hhm.member_type=cgt.item_id AND cgt.field_name='relationship_type_id'
LEFT OUTER JOIN ovc_care_health ON
ovc_care_health.person_id=ovc_registration.person_id
left outer join ovc_facility on ovc_care_health.facility_id=ovc_facility.id
where ovc_registration.child_cbo_id in ({cbos})
and reg_persons_geo.is_void = False
and ovc_care_events.date_of_event between '{start_date}' and '{end_date}'
and service != '' and service is not null
'''

QUERIES['needs_vs_served'] = '''
SELECT CAST(COUNT(DISTINCT person_id) AS integer) AS OVCCount, CBO, ward, item_description as Service,County,AgeRange,
CASE sex_id WHEN 'SMAL' THEN 'Female' ELSE 'Male' END AS Gender,
Indicator
FROM
(
SELECT ovc_care_events.person_id, reg_org_unit.org_unit_name AS CBO, list_geo.area_name AS ward, list_general.item_description,
derivedtbl_1.area_name as County,
reg_person.sex_id,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange, 'Needs ' || ' '  as Indicator
FROM  (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1) AS derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_care_priority INNER JOIN
         ovc_care_events ON ovc_care_events.event = ovc_care_priority.event_id INNER JOIN
         reg_person ON ovc_care_events.person_id = reg_person.id INNER JOIN
         list_general ON ovc_care_priority.service = list_general.item_id LEFT OUTER JOIN
         ovc_registration ON ovc_care_events.person_id = ovc_registration.person_id LEFT OUTER JOIN
         reg_org_unit ON reg_org_unit.id = ovc_registration.child_cbo_id LEFT OUTER JOIN
         reg_persons_geo ON reg_persons_geo.person_id = ovc_registration.person_id ON list_geo.area_id = reg_persons_geo.area_id
WHERE reg_org_unit.id in ({cbos})  and (ovc_care_priority.is_void = 'False') AND (ovc_care_events.event_type_id = 'FSAM') AND (ovc_care_events.date_of_event BETWEEN '{start_date}' AND '{end_date}')
GROUP BY ovc_care_events.person_id,ovc_care_priority.service, reg_person.date_of_birth, reg_person.sex_id, 
ovc_registration.child_cbo_id, reg_org_unit.org_unit_name, reg_persons_geo.area_id, list_geo.area_name, list_general.item_description,
derivedtbl_1.area_name,date_part('year', age(reg_person.date_of_birth))

union
SELECT ovc_care_events.person_id, reg_org_unit.org_unit_name AS CBO, list_geo.area_name AS ward, list_general.item_description, 
derivedtbl_1.area_name as County,
reg_person.sex_id,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange, 'Services ' || ' '  as Indicator
FROM  (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1) AS derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_care_services INNER JOIN
         ovc_care_events ON ovc_care_events.event = ovc_care_services.event_id INNER JOIN
         reg_person ON ovc_care_events.person_id = reg_person.id INNER JOIN
         list_general ON ovc_care_services.service_provided = list_general.item_id LEFT OUTER JOIN
         ovc_registration ON ovc_care_events.person_id = ovc_registration.person_id LEFT OUTER JOIN
         reg_org_unit ON reg_org_unit.id = ovc_registration.child_cbo_id LEFT OUTER JOIN
         reg_persons_geo ON reg_persons_geo.person_id = ovc_registration.person_id ON list_geo.area_id = reg_persons_geo.area_id
WHERE reg_org_unit.id in ({cbos}) and (ovc_care_services.is_void = 'False') AND (ovc_care_events.event_type_id = 'FSAM') AND (ovc_care_events.date_of_event BETWEEN '{start_date}' AND '{end_date}')
GROUP BY ovc_care_events.person_id,ovc_care_services.service_provided, reg_person.date_of_birth, reg_person.sex_id, 
ovc_registration.child_cbo_id, reg_org_unit.org_unit_name, reg_persons_geo.area_id, list_geo.area_name, list_general.item_description,
derivedtbl_1.area_name,date_part('year', age(reg_person.date_of_birth))

) tbl_pepfar
group by CBO, ward, item_description,County,AgeRange,Gender,Indicator
'''

QUERIES['ovc_overall_view'] = '''
SELECT person_id AS OVCid, CBO, ward, item_description as Service,County,AgeRange,
OVCName
FROM
(SELECT ovc_care_events.person_id, reg_org_unit.org_unit_name AS CBO, list_geo.area_name AS ward, list_general.item_description, 
derivedtbl_1.area_name as County,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
concat(reg_person.first_name,' ',reg_person.surname,' ',reg_person.other_names) as OVCName
FROM  (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1) AS derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_care_services INNER JOIN
         ovc_care_events ON ovc_care_events.event = ovc_care_services.event_id INNER JOIN
         reg_person ON ovc_care_events.person_id = reg_person.id INNER JOIN
         list_general ON ovc_care_services.service_provided = list_general.item_id LEFT OUTER JOIN
         ovc_registration ON ovc_care_events.person_id = ovc_registration.person_id LEFT OUTER JOIN
         reg_org_unit ON reg_org_unit.id = ovc_registration.child_cbo_id LEFT OUTER JOIN
         reg_persons_geo ON reg_persons_geo.person_id = ovc_registration.person_id ON list_geo.area_id = reg_persons_geo.area_id
WHERE reg_org_unit.id in ({cbos}) AND (ovc_care_services.is_void = 'False') AND (ovc_care_events.event_type_id = 'FSAM') AND (ovc_care_events.date_of_event BETWEEN '{start_date}' AND '{end_date}')
GROUP BY ovc_care_events.person_id,ovc_care_services.service_provided, reg_person.date_of_birth, reg_person.sex_id, 
ovc_registration.child_cbo_id, reg_org_unit.org_unit_name, reg_persons_geo.area_id, list_geo.area_name, list_general.item_description,
derivedtbl_1.area_name,date_part('year', age(reg_person.date_of_birth)),
reg_person.first_name,reg_person.surname,reg_person.other_names

UNION
SELECT ovc_care_events.person_id, reg_org_unit.org_unit_name AS CBO, list_geo.area_name AS ward, list_general.item_description,
 derivedtbl_1.area_name as County,
 CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
concat(reg_person.first_name,' ',reg_person.surname,' ',reg_person.other_names) as OVCName
FROM  (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1) AS derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_care_assessment INNER JOIN
         ovc_care_events ON ovc_care_events.event = ovc_care_assessment.event_id INNER JOIN
         reg_person ON ovc_care_events.person_id = reg_person.id INNER JOIN
         list_general ON ovc_care_assessment.service = list_general.item_id LEFT OUTER JOIN
         ovc_registration ON ovc_care_events.person_id = ovc_registration.person_id LEFT OUTER JOIN
         reg_org_unit ON reg_org_unit.id = ovc_registration.child_cbo_id LEFT OUTER JOIN
         reg_persons_geo ON reg_persons_geo.person_id = ovc_registration.person_id ON list_geo.area_id = reg_persons_geo.area_id
WHERE reg_org_unit.id in ({cbos}) AND (ovc_care_assessment.domain in ('DHNU','DPSS')) and (ovc_care_assessment.is_void = 'False') 
AND (ovc_care_events.event_type_id = 'FSAM') AND (ovc_care_events.date_of_event BETWEEN '{start_date}' AND '{end_date}')
GROUP BY ovc_care_events.person_id,ovc_care_assessment.service, reg_person.date_of_birth, reg_person.sex_id, 
ovc_registration.child_cbo_id, reg_org_unit.org_unit_name, reg_persons_geo.area_id, list_geo.area_name, 
list_general.item_description,derivedtbl_1.area_name,date_part('year', age(reg_person.date_of_birth)),reg_person.first_name,reg_person.surname,reg_person.other_names) tbl_ovc_overall_view
group by CBO, ward, item_description,County,AgeRange,OVCName,tbl_ovc_overall_view.person_id
'''

QUERIES['reporting_rates'] = '''
select 
CAST(COUNT(DISTINCT ovc_registration.person_id) AS integer) AS OVCCount,
reg_org_unit.org_unit_name as CBO,reg_org_unit.id as cboid
into TEMP temp_Actives
from (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1)  derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_registration LEFT OUTER JOIN
         reg_person ON ovc_registration.person_id = reg_person.id LEFT OUTER JOIN
         reg_person AS chw ON ovc_registration.child_chv_id = chw.id LEFT OUTER JOIN
         reg_person AS cgs ON ovc_registration.caretaker_id = cgs.id LEFT OUTER JOIN
         reg_org_unit ON ovc_registration.child_cbo_id = reg_org_unit.id LEFT OUTER JOIN
         reg_persons_geo ON ovc_registration.person_id = reg_persons_geo.person_id ON list_geo.area_id = reg_persons_geo.area_id
where ((is_active = 'True' and ovc_registration.registration_date <= '30-mar-2018') 
	or (is_active = 'False' and  (ovc_registration.registration_date between '01-jan-2017' and '30-mar-2018' )) 
	or (is_active = 'False' and ovc_registration.registration_date <= '01-jan-2017'  and exit_date > '30-mar-2018' ) 
	or (is_active = 'False' and ovc_registration.registration_date <= '01-jan-2017'  and exit_date between '01-jan-2017' and '30-mar-2018' )
										)
	group by 	reg_org_unit.org_unit_name,reg_org_unit.id ;								

SELECT CAST(COUNT(DISTINCT person_id) AS integer) AS OVCCount, CBO, ward, County,AgeRange,
tbl_pepfar.cboid,tbl_pepfar.countyid,CASE sex_id WHEN 'SMAL' THEN 'Female' ELSE 'Male' END AS Gender,derived_Actives.CboActive
FROM
(
SELECT ovc_care_events.person_id, reg_org_unit.org_unit_name AS CBO, list_geo.area_name AS ward, list_general.item_description, 
derivedtbl_1.area_name as County,
reg_person.sex_id,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,reg_org_unit.id as cboid,list_geo.parent_area_id as Countyid
FROM  (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1) AS derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_care_services INNER JOIN
         ovc_care_events ON ovc_care_events.event = ovc_care_services.event_id INNER JOIN
         reg_person ON ovc_care_events.person_id = reg_person.id INNER JOIN
         list_general ON ovc_care_services.service_provided = list_general.item_id LEFT OUTER JOIN
         ovc_registration ON ovc_care_events.person_id = ovc_registration.person_id LEFT OUTER JOIN
         reg_org_unit ON reg_org_unit.id = ovc_registration.child_cbo_id LEFT OUTER JOIN
         reg_persons_geo ON reg_persons_geo.person_id = ovc_registration.person_id ON list_geo.area_id = reg_persons_geo.area_id
WHERE (ovc_care_services.is_void = 'False') AND (ovc_care_events.event_type_id = 'FSAM') AND (ovc_care_events.date_of_event BETWEEN '01-jan-2017' AND '30-sep-2017')
GROUP BY ovc_care_events.person_id,ovc_care_services.service_provided, reg_person.date_of_birth, reg_person.sex_id, 
ovc_registration.child_cbo_id, reg_org_unit.org_unit_name, reg_persons_geo.area_id, list_geo.area_name, list_general.item_description,
derivedtbl_1.area_name,date_part('year', age(reg_person.date_of_birth)),reg_org_unit.id ,list_geo.parent_area_id

UNION

SELECT ovc_care_events.person_id, reg_org_unit.org_unit_name AS CBO, list_geo.area_name AS ward, list_general.item_description, 
derivedtbl_1.area_name as County,
reg_person.sex_id,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,reg_org_unit.id as cboid,list_geo.parent_area_id as Countyid
FROM  (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1) AS derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_care_assessment INNER JOIN
         ovc_care_events ON ovc_care_events.event = ovc_care_assessment.event_id INNER JOIN
         reg_person ON ovc_care_events.person_id = reg_person.id INNER JOIN
         list_general ON ovc_care_assessment.service = list_general.item_id LEFT OUTER JOIN
         ovc_registration ON ovc_care_events.person_id = ovc_registration.person_id LEFT OUTER JOIN
         reg_org_unit ON reg_org_unit.id = ovc_registration.child_cbo_id LEFT OUTER JOIN
         reg_persons_geo ON reg_persons_geo.person_id = ovc_registration.person_id ON list_geo.area_id = reg_persons_geo.area_id
WHERE (ovc_care_assessment.domain in ('DHNU','DPSS')) and (ovc_care_assessment.is_void = 'False') 
AND (ovc_care_events.event_type_id = 'FSAM') AND (ovc_care_events.date_of_event BETWEEN '01-jan-2017' AND '30-sep-2017')
GROUP BY ovc_care_events.person_id,ovc_care_assessment.service, reg_person.date_of_birth, reg_person.sex_id, 
ovc_registration.child_cbo_id, reg_org_unit.org_unit_name, reg_persons_geo.area_id, list_geo.area_name, 
list_general.item_description,derivedtbl_1.area_name,date_part('year', age(reg_person.date_of_birth)),reg_org_unit.id ,list_geo.parent_area_id) tbl_pepfar
INNER JOIN
(select ovccount as cboActive,cboid from temp_Actives) derived_Actives ON derived_Actives.cboid = tbl_pepfar.cboid
group by CBO, ward, County,AgeRange,tbl_pepfar.cboid,tbl_pepfar.countyid,Gender,CboActive;
'''
# OVC Not Served
QUERIES['ovc_not_served'] = '''
SELECT 
child_cbo_id AS cbo_id, reg_org_unit.org_unit_name AS cbo,
list_geo.area_id AS ward_id, list_geo.area_name AS ward,
scc.area_name AS constituency, cc.area_name AS county,
ovc_registration.person_id AS cpims_id,
concat(reg_person.first_name,' ',reg_person.surname,' ',reg_person.other_names) AS ovc_names,
CASE reg_person.sex_id WHEN 'SFEM' THEN 'Female' ELSE 'Male' END AS gender,
reg_person.date_of_birth AS DOB,
date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) AS age,
CASE
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(timestamp '{end_date}', reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
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
LEFT OUTER JOIN reg_persons_external_ids as exidd on exidd.person_id=ovc_registration.person_id and exidd.identifier_type_id = 'IPWD'
WHERE reg_org_unit.id in ({cbos}) AND ovc_registration.person_id NOT IN
(
SELECT DISTINCT ovc_care_events.person_id
FROM  (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1) AS derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_care_services INNER JOIN
         ovc_care_events ON ovc_care_events.event = ovc_care_services.event_id INNER JOIN
         reg_person ON ovc_care_events.person_id = reg_person.id INNER JOIN
         list_general ON ovc_care_services.service_provided = list_general.item_id LEFT OUTER JOIN
         ovc_registration ON ovc_care_events.person_id = ovc_registration.person_id LEFT OUTER JOIN
         reg_org_unit ON reg_org_unit.id = ovc_registration.child_cbo_id LEFT OUTER JOIN
         reg_persons_geo ON reg_persons_geo.person_id = ovc_registration.person_id ON list_geo.area_id = reg_persons_geo.area_id
WHERE reg_org_unit.id in ({cbos}) AND (ovc_care_services.is_void = 'False') AND (ovc_care_events.event_type_id = 'FSAM') AND (ovc_care_events.date_of_event BETWEEN '{start_date}' AND '{end_date}')

UNION

SELECT ovc_care_events.person_id
FROM  (SELECT area_id, area_name, area_code, parent_area_id
        FROM   list_geo AS list_geo_1) AS derivedtbl_1 INNER JOIN
         list_geo ON derivedtbl_1.area_id = list_geo.parent_area_id RIGHT OUTER JOIN
         ovc_care_assessment INNER JOIN
         ovc_care_events ON ovc_care_events.event = ovc_care_assessment.event_id INNER JOIN
         reg_person ON ovc_care_events.person_id = reg_person.id INNER JOIN
         list_general ON ovc_care_assessment.service = list_general.item_id LEFT OUTER JOIN
         ovc_registration ON ovc_care_events.person_id = ovc_registration.person_id LEFT OUTER JOIN
         reg_org_unit ON reg_org_unit.id = ovc_registration.child_cbo_id LEFT OUTER JOIN
         reg_persons_geo ON reg_persons_geo.person_id = ovc_registration.person_id ON list_geo.area_id = reg_persons_geo.area_id
WHERE reg_org_unit.id in ({cbos}) AND (ovc_care_assessment.domain in ('DHNU','DPSS')) and (ovc_care_assessment.is_void = 'False') 
AND (ovc_care_events.event_type_id = 'FSAM') AND (ovc_care_events.date_of_event BETWEEN '{start_date}' AND '{end_date}')
)
'''