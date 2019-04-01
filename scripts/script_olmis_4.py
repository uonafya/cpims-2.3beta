#!c:\python27\python.exe
import traceback
import pymssql
import psycopg2
import psycopg2.extras
import datetime
from time import time
import uuid
import csv

# --------------------------------NOTES--------------------------------#

"""
- -Pending insert to reg_person_orgunits
- Review insert into reg_org_unit
"""

""" NOTES """
# 1. XXXX represents failed translations because the values don't exist in
# the postgres look_up table.

# MODIFIED TO COUNT OVC REGISTRATION RECORD NUMBER -- WILLIAM WATEMBO
'''
Missing fields in AMURT VERSION
Clientdetails.bcertnumber AS ClientBirthCertNumber,
Clientdetails.IsDisabled AS ClientIsDisabled,
"Clientdetails.NCPWDNumber AS ClientNCPWDNumber," +
"Clientdetails.bcertnumber AS ClientBirthCertNumber, Clientdetails.IsDisabled AS ClientIsDisabled, Clientdetails.NCPWDNumber AS ClientNCPWDNumber," +
'''

USER_ID = 1
PROJ_DB = 'AMURT'
PROJ_USER = 'pass1234'
TMP_TABLE = 'TEMPORARY_FLAT_TABLE2'
CPIMS_CONN = ("dbname='cpims_amurt' user='postgres' "
              "host='localhost' password='postgres'")
CBOS = {}
WARDS = {}


def check_column(row, field):
    """To handle missing column cases."""
    data = row[field] if field in row else None
    return data


def check_int(value):
    """Handle None before int cast."""
    data = int(value) if value else 0
    return data


def check_value(value_names, value_name):
    """Get area names"""
    vname = value_name.upper()
    if vname in value_names:
        value_id = value_names[value_name]
    else:
        value_id = 0
    return value_id


def write_csv(csv_file, rows):
    """Method to write csv."""
    with open(csv_file, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"',
                               quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            csvwriter.writerow(row)


def write_fl_data():
    """Method to write flattened data."""
    dts = []
    for row in mssql_cursor:
        rds = []
        for rd in row:
            val = row[rd]
            vl = str(val) if val is not None else ''
            rds.append(vl)
        rd = ', '.join(rds)
        dts.append([rd])
    write_csv('aplus.csv', dts)
    print 'Done copying to csv in %s secs ' % (time() - tic)
    exit()


def get_area(ward_name):
    """Method to get area."""
    fields = translator(7, ward_name)
    area_id = fields['area_id']
    return area_id


def get_orgs(pgsql_cursor, org_unit_name, area_id):
    """Method to handle org units."""
    sql = ("SELECT id, org_unit_id_vis, org_unit_name FROM reg_org_unit "
           "WHERE org_unit_name='" + org_unit_name + "' LIMIT 1")
    pgsql_cursor.execute(sql)
    if pgsql_cursor.rowcount > 0:
        orgs = pgsql_cursor.fetchone()
        org_unit_id = orgs[0]
        org_unit_name = orgs[2]
    else:
        org_unit_id_vis = 'U000000'
        org_unit_type_id = 'TNCB'
        date_operational = None
        date_closed = None
        handle_ovc = True
        is_void = False
        parent_org_unit_id = 1
        created_by_id = USER_ID
        pgsql_cursor.execute("INSERT INTO reg_org_unit(org_unit_id_vis, org_unit_name, org_unit_type_id, date_operational, date_closed, handle_ovc, is_void, parent_org_unit_id, created_at, created_by_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                             (org_unit_id_vis, org_unit_name, org_unit_type_id, date_operational, date_closed, handle_ovc, is_void, parent_org_unit_id, created_at, created_by_id))
        # conn2.commit()
        org_unit_id = pgsql_cursor.fetchone()[0]
        # insert into reg_org_units_geo
        date_linked = created_at
        date_delinked = None
        pgsql_cursor.execute("INSERT INTO reg_org_units_geo(date_linked, date_delinked, area_id, org_unit_id, is_void) VALUES(%s, %s, %s, %s, %s) RETURNING id;",
                             (date_linked, date_delinked, area_id, org_unit_id, is_void))
        # conn2.commit()
        # print 'inserting records into reg_org_units_geo . . .'
    return org_unit_id


def get_facility(pgsql_cursor, facility_name):
    """Method to handle org units."""
    sql = ("SELECT id, facility_name FROM ovc_facility "
           "WHERE facility_name='" + facility_name + "' LIMIT 1")
    pgsql_cursor.execute(sql)
    if pgsql_cursor.rowcount > 0:
        orgs = pgsql_cursor.fetchone()
        facility_id = orgs[0]
        facility_name = orgs[1]
    else:
        print facility_name
        pgsql_cursor.execute("INSERT INTO ovc_facility(facility_name, is_void) VALUES(%s, %s) RETURNING id;",
                             (facility_name, False))
        # conn2.commit()
        facility_id = pgsql_cursor.fetchone()[0]
    return facility_id


def translator(x, value):
    # translate look_ups(Service)
    conn2 = psycopg2.connect(CPIMS_CONN)
    if x == 0:
        fields = {'domain': 'ERR', 'service': 'ERR'}
        cur2 = conn2.cursor()
        cur2.execute("SELECT item_id, item_description, item_description_short, item_category, item_sub_category, field_name FROM list_general " +
                     "WHERE LOWER(item_description) LIKE '" + value.lower() + "%' AND item_category='Service' AND field_name LIKE 'olmis%'")
        if cur2.rowcount > 0:
            for row in cur2.fetchall():
                fields['service'] = row[0]
                field_name = row[5]
                if 'olmis_shelter' in field_name:
                    fields['domain'] = 'DSHC'
                if 'olmis_pss' in field_name:
                    fields['domain'] = 'DPSS'
                if 'olmis_protection' in field_name:
                    fields['domain'] = 'DPRO'
                if 'olmis_hes' in field_name:
                    fields['domain'] = 'DHES'
                if 'olmis_health' in field_name:
                    fields['domain'] = 'DHNU'
                if 'olmis_education' in field_name:
                    fields['domain'] = 'DEDU'
        else:
            fields = {'domain': 'XXXX', 'service': 'XXXX'}
        value = fields
        return value

    # translate subdomains
    if x == 1:

        if 'Food Security' in value:
            value = 'HNU1'
        if 'Nutrition and Growth' in value:
            value = 'HNU2'
        if 'Wellness' in value:
            value = 'HNU3'
        if 'Healthcare Services' in value:
            value = 'HNU4'
        if 'Shelter' in value:
            value = 'SHC1'
        if 'Care' in value:
            value = 'SHC2'
        if 'Abuse and Exploitation' in value:
            value = 'PRO1'
        if 'Legal Protection' in value:
            value = 'PRO2'
        if 'Emotional Health' in value:
            value = 'PSS1'
        if 'Social Behavior' in value:
            value = 'PSS2'
        if 'Performance' in value:
            value = 'EDU1'
        if 'Education and Work' in value:
            value = 'EDU2'
        return value

    # translate goal ids
    if x == 2:
        if value == '4 - Good':
            value = 'GOOD'
        if value == '3 - Fair':
            value = 'FAIR'
        if value == '2 - Bad':
            value = 'GBAD'
        if value == '1 - Very Bad':
            value = 'VBAD'
        return value

    # translate look_ups(Assessments)
    if x == 3:
        fields = {'domain': 'ERR', 'service': 'ERR', 'service_status': 'ERR'}
        cur1 = conn2.cursor()
        cur2 = conn2.cursor()
        cur1.execute("SELECT item_id, item_description, item_description_short, item_category, item_sub_category, field_name FROM list_general " +
                     "WHERE LOWER(item_description) = '" + value.lower() + "' AND item_category='Monitor' AND field_name LIKE 'olmis%'")
        if cur1.rowcount > 0:
            for row in cur1.fetchall():
                fields['service'] = row[0]
                field_name = row[5]
                if 'olmis_shelter' in field_name:
                    fields['domain'] = 'DSHC'
                if 'olmis_pss' in field_name:
                    fields['domain'] = 'DPSS'
                if 'olmis_protection' in field_name:
                    fields['domain'] = 'DPRO'
                if 'olmis_hes' in field_name:
                    fields['domain'] = 'DHES'
                if 'olmis_health' in field_name:
                    fields['domain'] = 'DHNU'
                if 'olmis_education' in field_name:
                    fields['domain'] = 'DEDU'
        else:
            fields = {'domain': 'XXXX', 'service': 'XXXX'}
        value = fields
        return value

    # translate look_ups(Generic)
    if x == 4:
        fields = {'domain': 'ERR', 'service': 'ERR'}
        cur1 = conn2.cursor()
        cur1.execute("SELECT item_id, item_description, item_description_short, item_category, item_sub_category, field_name FROM list_general " +
                     "WHERE LOWER(item_description) LIKE '" + value.lower() + "%' AND field_name LIKE 'olmis%'")
        if cur1.rowcount > 0:
            for row in cur1.fetchall():
                fields['service'] = row[0]
        else:
            fields = {'domain': 'XXXX', 'service': 'XXXX'}
        value = fields
        return value

    # translate look_ups(HHVA)
    if x == 5:
        response = (value[0]).strip()
        response_id = check_int(value[1])
        hhva_code = (value[2]).strip()
        amount = str(value[3])
        condition_size = str(value[4])
        fields = []

        # HA1.2.3.4
        if check_int(response_id) == 1:
            fields.append({
                'entity': 'HA1F',
                'attribute': 'HA1F',
                'value': amount,
                'value_for': ''
            })
        if check_int(response_id) == 2:
            fields.append({
                'entity': 'HA1M',
                'attribute': 'HA1M',
                'value': amount,
                'value_for': ''
            })
        if check_int(response_id) == 3:
            fields.append({
                'entity': 'HA2F',
                'attribute': 'HA2F',
                'value': amount,
                'value_for': ''
            })
        if check_int(response_id) == 4:
            fields.append({
                'entity': 'HA2M',
                'attribute': 'HA2M',
                'value': amount,
                'value_for': ''
            })
        if check_int(response_id) == 5:
            fields.append({
                'entity': 'HA3F',
                'attribute': 'HA3F',
                'value': amount,
                'value_for': ''
            })
        if check_int(response_id) == 6:
            fields.append({
                'entity': 'HA3M',
                'attribute': 'HA3M',
                'value': amount,
                'value_for': ''
            })
        if check_int(response_id) == 7:
            fields.append({
                'entity': 'HA4F',
                'attribute': 'HA4F',
                'value': amount,
                'value_for': ''
            })
        if check_int(response_id) == 8:
            fields.append({
                'entity': 'HA4M',
                'attribute': 'HA4M',
                'value': amount,
                'value_for': ''
            })

        cur1 = conn2.cursor()
        cur1.execute("SELECT item_id, item_description, item_description_short, item_category, item_sub_category, field_name FROM list_general " +
                     "WHERE LOWER(item_description) LIKE '" + response.lower() + "%' AND field_name LIKE 'olmis%'")
        if cur1.rowcount > 0:
            for row in cur1.fetchall():
                if(hhva_code == 'HA5'):
                    fields.append({
                        'entity': 'HA5',
                        'attribute': 'HA5',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA6'):
                    fields.append({
                        'entity': 'HA6',
                        'attribute': 'HA6',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA7'):
                    fields.append({
                        'entity': 'HA7',
                        'attribute': 'HA7',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA8'):
                    fields.append({
                        'entity': 'HA8',
                        'attribute': 'HA8',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA9'):
                    fields.append({
                        'entity': 'HA9',
                        'attribute': 'HA9',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA10'):
                    condition = condition_size
                    number = amount
                    field = translator(4, condition)
                    fields.append({
                        'entity': 'HA10',
                        'attribute': 'HA10',
                        'value': field['service'],
                        'value_for': 'CONDITION'
                    })
                    fields.append({
                        'entity': 'HA10',
                        'attribute': 'HA10',
                        'value': number,
                        'value_for': 'NUMBER'
                    })
                if(hhva_code == 'HA11'):
                    fields.append({
                        'entity': 'HA11',
                        'attribute': 'HA11',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA12'):
                    fields.append({
                        'entity': 'HA12',
                        'attribute': 'HA12',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA13'):
                    fields.append({
                        'entity': 'HA13',
                        'attribute': 'HA13',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA14'):
                    fields.append({
                        'entity': 'HA14',
                        'attribute': 'HA14',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA15'):
                    condition = condition_size
                    number = amount
                    fields.append({
                        'entity': 'HA15',
                        'attribute': 'HA15',
                        'value': condition,
                        'value_for': 'SIZE'
                    })
                    fields.append({
                        'entity': 'HA15',
                        'attribute': 'HA15',
                        'value': number,
                        'value_for': 'NUMBER'
                    })
                if(hhva_code == 'HA16'):
                    fields.append({
                        'entity': 'HA16',
                        'attribute': 'HA16',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA17'):
                    fields.append({
                        'entity': 'HA17',
                        'attribute': 'HA17',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA18'):
                    fields.append({
                        'entity': 'HA18',
                        'attribute': 'HA18',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA19'):
                    fields.append({
                        'entity': 'HA19',
                        'attribute': 'HA19',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA20'):
                    fields.append({
                        'entity': 'HA20',
                        'attribute': 'HA20',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA21'):
                    fields.append({
                        'entity': 'HA21',
                        'attribute': 'HA21',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA22'):
                    fields.append({
                        'entity': 'HA22',
                        'attribute': 'HA22',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA23'):
                    fields.append({
                        'entity': 'HA23',
                        'attribute': 'HA23',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA24'):
                    fields.append({
                        'entity': 'HA24',
                        'attribute': 'HA24',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA25'):
                    fields.append({
                        'entity': 'HA25',
                        'attribute': 'HA25',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA26' and response == 'Male'):
                    fields.append({
                        'entity': 'HA26M',
                        'attribute': 'HA26M',
                        'value': amount,
                        'value_for': ''
                    })
                if(hhva_code == 'HA26' and response == 'Female'):
                    fields.append({
                        'entity': 'HA26F',
                        'attribute': 'HA26F',
                        'value': amount,
                        'value_for': ''
                    })
                if(hhva_code == 'HA27' and response == 'Male'):
                    fields.append({
                        'entity': 'HA27M',
                        'attribute': 'HA27M',
                        'value': amount,
                        'value_for': ''
                    })
                if(hhva_code == 'HA27' and response == 'Female'):
                    fields.append({
                        'entity': 'HA27F',
                        'attribute': 'HA27F',
                        'value': amount,
                        'value_for': ''
                    })
                if(hhva_code == 'HA28'):
                    fields.append({
                        'entity': 'HA28',
                        'attribute': 'HA28',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA29'):
                    fields.append({
                        'entity': 'HA29',
                        'attribute': 'HA29',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA30'):
                    fields.append({
                        'entity': 'HA30',
                        'attribute': 'HA30',
                        'value': row[0],
                        'value_for': ''
                    })
                if(hhva_code == 'HA31'):
                    fields.append({
                        'entity': 'HA31',
                        'attribute': 'HA31',
                        'value': row[0],
                        'value_for': ''
                    })
        else:
            fields.append({
                'entity': hhva_code,
                'attribute': hhva_code,
                'value': 'XXXX',
                'value_for': 'XXXX'
            })

        value = fields
        return value

    # translate look_ups for service_provider
    if x == 6:
        if value == 'Religious Organization':
            value = 'PROG'
        elif value == 'GoK':
            value = 'PGOK'
        elif value == 'AMURT':
            value = 'PUSG'
        else:
            value = 'PUSG'
        return value

    # translate look_ups list_geo (county)
    if x == 7:
        conn2 = psycopg2.connect(CPIMS_CONN)
        fields = {'area_id': '1'}
        cur2 = conn2.cursor()
        value = value.replace('/ ', '/')
        value = value.replace(' /', '/')
        value = value.replace("'", "''")
        sql = ("SELECT area_id FROM list_geo WHERE area_type_id='GWRD' "
               "AND LOWER(area_name) = '%s'") % (value.lower())
        cur2.execute(sql)
        if cur2.rowcount > 0:
            for row in cur2.fetchall():
                fields['area_id'] = row[0]
        else:
            fields = {'area_id': '1'}
        value = fields
        return value
# -----------------------------END TRANSLATOR--------------------------------#

# ---------------------------DATA SCRIPTS ------------------------------------#


""" System Variables """
OVCCareEvents_CSI = []
OVCCareEvents_F1A = []
OVCCareEvents_HHVA = []
NeedsAssessmentPKs = []
ServicePKs = []
HHVAPKs = []
HouseHoldheadIDs = []
CBONames = []
OVCID_MATRIX = []
OVCIDS = []
dictXarray = []

org_unit_pk = None
mssql_conn = None
pgsql_conn = None

OVCID_OIDS = []

try:
    # connect to SQL SERVER & Postgresql
    mssql_conn = pymssql.connect(host='(local)', user='sa', port=1434,
                                 password=PROJ_USER, database=PROJ_DB)
    mssql_cursor = mssql_conn.cursor(as_dict=True)
    print 'connected to SQL SERVER! (%s)' % (PROJ_DB)
    pgsql_conn = psycopg2.connect(CPIMS_CONN)
    pgsql_cursor = pgsql_conn.cursor()
    print 'connected to PostgreSQL!'
    # flatten dataset/push to temp_table
    mssql_query_select = ("SELECT Clientdetails.ClientID AS ClientID, Clientdetails.OVCID AS OVCID, Clientdetails.FirstName AS ClientFirstName," +
                            "Clientdetails.MiddleName AS ClientMiddleName, Clientdetails.Surname AS ClientSurname, Clientdetails.Gender AS ClientGender," +
                            "Clientdetails.DateofBirth AS ClientDateofBirth, Clientdetails.BirthCert AS ClientBirthCert, Clientdetails.ClientType, " +
                            "Clientdetails.Cbo AS ClientCbo, Clientdetails.District AS ClientDistrict, Clientdetails.Location AS ClientLocation," 
                            "Clientdetails.Facility AS ClientFacility, Clientdetails.VolunteerId AS ClientVolunteerId," +
                            "Clientdetails.SchoolLevel AS ClientSchoolLevel, Clientdetails.HIVStatus AS ClientHivStatus, Clientdetails.ARTStatus AS ClientARTStatus," +
                            "Clientdetails.GuardianID AS ClientGuardianID, Clientdetails.FatherID AS ClientFatherID, Clientdetails.MotherID AS ClientMotherID," +
                            "Clientdetails.HouseHoldheadID AS ClientHouseHoldheadID, Clientdetails.CareTaker AS ClientCareTaker, Clientdetails.Exited AS ClientExited," +
                            "Clientdetails.ReasonforExit AS ClientReasonforExit, Clientdetails.DateofRegistration AS ClientDateofRegistration," +
                            "Clientdetails.DateofVisit AS ClientDateofVisit, Clientdetails.DateofExit AS ClientDateofExit, Clientdetails.School AS ClientSchool," +
                            "Clientdetails.class AS ClientClass, Clientdetails.EligibilityCriteria AS ClientEligibilityCriteria," +
                            "Clientdetails.HHVulnerabilityStatus AS ClientHHVulnerabilityStatus, Clientdetails.Immunization AS ClientImmunization," +
                            "Clientdetails.IsEnrolment AS ClientIsEnrolment, Clientdetails.SchoolingType AS ClientSchoolingType, Clientdetails.DateofLinkage AS ClientDateofLinkage," +
                            "ParentDetails.ParentId, ParentDetails.IDNumber AS ParentIDNumber, ParentDetails.FirstName AS ParentFirstName," +
                            "ParentDetails.MiddleName AS ParentMiddleName, ParentDetails.Surname AS ParentSurname, ParentDetails.DateofBirth AS ParentDateofBirth," +
                            "ParentDetails.IsDead AS ParentIsDead, ParentDetails.CauseofDeath AS ParentCauseofDeath, ParentDetails.HIVStatus AS ParentHIVStatus," +
                            "ParentDetails.Gender AS ParentGender, ParentDetails.MobileNumber AS ParentMobileNumber, ParentDetails.Relationship AS ParentRelationship," +
                            "ParentDetails.AgeRange AS ParentAgeRange, ParentDetails.DateofVisit AS ParentDateofVisit, ParentDetails.IsHCBCClient AS ParentIsHCBCClient," +
                            "ParentDetails.District AS ParentDistrict, ParentDetails.Location AS ParentLocation, ParentDetails.MaritalStatus AS ParentMaritalStatus," +
                            "ParentDetails.TypeofEmployment AS ParentTypeofEmployment, ParentDetails.Schoollevel AS ParentSchoollevel," +
                            "ParentDetails.ChildreninHousehold AS ParentChildreninHousehold, ParentDetails.ChildreninOVCProg AS ParentChildreninOVCProg," +
                            "ParentDetails.YearconfirmedHIV AS ParentYearconfirmedHIV, ParentDetails.HBCProgram AS ParentHBCProgram," +
                            "ParentDetails.YearsinHBC AS ParentYearsinHBC, ParentDetails.CHW AS ParentCHW, ParentDetails.ARTStatus AS ParentARTStatus," +
                            "ParentDetails.Facility AS ParentFacility, ParentDetails.CCCNo AS ParentCCCNo, ParentDetails.DateofRegistration AS ParentDateofRegistration," +
                            "ParentDetails.ovccbo AS ParentCbo, County.County, CHW.FirstName AS CHWFirstName, CHW.MiddleName AS CHWMiddleName," +
                            "CHW.Surname AS CHWSurname, CHW.CBOID AS CHWCBOID, CHW.IsActive AS CHWIsActive, CHW.Gender AS CHWGender, Facilities.Facility," + 
                            "CBO.CBO AS CBOName, District.District, Wards.Ward AS WardName INTO TEMPORARY_FLAT_TABLE2 " +
                            "FROM ParentDetails RIGHT OUTER JOIN " +
                            "Facilities RIGHT OUTER JOIN " +
                            "District INNER JOIN " +
                            "County ON District.Countyid = County.CountyID RIGHT OUTER JOIN " +
                            "Clientdetails INNER JOIN " +
                            "CBO ON Clientdetails.Cbo = CBO.CBOID LEFT OUTER JOIN " +
                            "Location ON Clientdetails.Location = Location.LocationID LEFT OUTER JOIN " +
                            "Wards ON Location.Wardid = Wards.Wardid LEFT OUTER JOIN " +
                            "CHW ON Clientdetails.VolunteerId = CHW.CHWID ON District.DistrictID = Clientdetails.District ON " +
                            "Facilities.Facilityid = Clientdetails.Facility ON ParentDetails.ParentId = Clientdetails.HouseHoldheadID ORDER BY ClientID")

    tic = time()
    mssql_cursor.execute(mssql_query_select)
    mssql_conn.commit()
    toc = time()
    print 'Flattening dataset to tmp in (%s) secs ...' % (toc - tic)
    # interface with PostgreSQL
    tic = time()
    cnt_sql = ("SELECT COUNT(OVCID) as ovc_count FROM %s") % (TMP_TABLE)
    mssql_cursor.execute(cnt_sql)
    ovcs = mssql_cursor.fetchone()
    total_ovc = ovcs['ovc_count']
    mssql_temp_sql = ("SELECT * FROM %s ORDER BY OVCID ASC") % (TMP_TABLE)
    mssql_cursor.execute(mssql_temp_sql)
    hrcnt, thrcnt = 0, mssql_cursor.rowcount
    # csv
    for row in mssql_cursor:
        OVCID = row['OVCID']
        is_void = False
        created_at = datetime.datetime.now()
        hrcnt += 1
        td = round(((time() - tic) / 60), 2)
        print 'OVC registration record', hrcnt, '/', total_ovc, td, 'min'

        # harvest OVCIDS
        OVCIDS.append(str(row['OVCID']))

        # insert into reg_org_unit
        # Re-use wards data
        ward_name = row['WardName']
        area_id = check_value(WARDS, ward_name)
        if area_id == 0:
            area_id = get_area(ward_name)
            WARDS[ward_name] = area_id
        # Re-use cbo data
        org_unit_name = row['CBOName']
        org_unit_id = check_value(CBOS, org_unit_name)
        if org_unit_id == 0:
            org_unit_id = get_orgs(pgsql_cursor, org_unit_name, area_id)
            CBOS[org_unit_name] = org_unit_id
        # insert reg_person_user (CHW)
        ufirst_name = row['CHWFirstName']
        ufirst_name = row['CHWFirstName'] if row['CHWFirstName'] else 'XXXX'
        uother_names = row['CHWMiddleName']
        usurname = row['CHWSurname']
        usurname = row['CHWSurname'] if row['CHWSurname'] else 'XXXX'
        udesignation = 'DVCO'
        usex_id = 'SMAL' if str(row['CHWGender']) == 'Male' else 'SFEM'
        udate_of_birth = None
        pgsql_cursor.execute("INSERT INTO reg_person(first_name, other_names, surname, designation, sex_id, date_of_birth, is_void, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                             (ufirst_name, uother_names, usurname, udesignation, usex_id, udate_of_birth, is_void, created_at))
        # conn2.commit()
        user_pk = pgsql_cursor.fetchone()[0]
        chv_pk = user_pk

        # insert reg_persons_types_user (CHW)
        person_type_id = 'TWVL'
        date_began = created_at
        date_ended = None
        person_id = chv_pk
        pgsql_cursor.execute("INSERT INTO reg_persons_types(person_type_id, date_began, date_ended, person_id, is_void) VALUES(%s, %s, %s, %s, %s) RETURNING id;",
                             (person_type_id, date_began, date_ended, person_id, is_void))

        # insert into reg_persons_geo_user (CHW)
        date_linked = created_at
        date_delinked = None
        area_type = 'GWRD'
        # fields = translator(7, row['WardName'])
        # area_id = fields['area_id']
        person_id = user_pk
        pgsql_cursor.execute("INSERT INTO reg_persons_geo(date_linked, date_delinked, area_type, area_id, person_id, is_void) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;",
                             (date_linked, date_delinked, area_type, area_id, person_id, is_void))
        # print 'inserting records into reg_persons_geo(ovc) . . .'

        # insert to reg_persons_org_units (CHW)
        person = user_pk
        org_unit = org_unit_id
        date_linked = created_at
        date_delinked = None
        primary_unit = True
        reg_assistant = True
        pgsql_cursor.execute("INSERT INTO reg_persons_org_units(person_id, org_unit_id, date_linked, date_delinked, primary_unit, reg_assistant, is_void) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                             (person_id, org_unit, date_linked, date_delinked, primary_unit, reg_assistant, is_void))

        # insert reg_person_client
        cfirst_name = row['ClientFirstName']
        cfirst_name = row['ClientFirstName'] if row['ClientFirstName'] else 'XXXX'
        cother_names = row['ClientMiddleName']
        csurname = row['ClientSurname']
        csurname = row['ClientSurname'] if row['ClientSurname'] else 'XXXX'
        cdesignation = 'COVC'
        csex_id = 'SMAL' if str(row['ClientGender']) == 'Male' else 'SFEM'
        cdate_of_birth = row['ClientDateofBirth']
        pgsql_cursor.execute("INSERT INTO reg_person(first_name, other_names, surname, designation, sex_id, date_of_birth, is_void, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                             (cfirst_name, cother_names, csurname, cdesignation, csex_id, cdate_of_birth, is_void, created_at))
        person_pk = pgsql_cursor.fetchone()[0]
        # print 'inserting records into reg_person(ovc) . . .'

        # insert reg_persons_types_client
        person_type_id = 'TBVC'
        date_began = created_at
        date_ended = None
        person_id = person_pk
        pgsql_cursor.execute("INSERT INTO reg_persons_types(person_type_id, date_began, date_ended, person_id, is_void) VALUES(%s, %s, %s, %s, %s) RETURNING id;",
                             (person_type_id, date_began, date_ended, person_id, is_void))
        # print 'inserting records into reg_persons_types(ovc) . . .'

        # insert into reg_persons_geo_client
        date_linked = created_at
        date_delinked = None
        area_type = 'GWRD'
        # fields = translator(7, row['WardName'])
        # area_id = fields['area_id']
        person_id = person_pk
        pgsql_cursor.execute("INSERT INTO reg_persons_geo(date_linked, date_delinked, area_type, area_id, person_id, is_void) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;",
                             (date_linked, date_delinked, area_type, area_id, person_id, is_void))
        # print 'inserting records into reg_persons_geo(ovc) . . .'

        if not (row['ClientHouseHoldheadID']) in HouseHoldheadIDs:
            # insert into reg_person_parent
            pfirst_name = row['ParentFirstName']
            pfirst_name = row['ParentFirstName'] if row['ParentFirstName'] else 'XXXX'
            pother_names = row['ParentMiddleName']
            psurname = row['ParentSurname']
            psurname = row['ParentSurname'] if row['ParentSurname'] else 'XXXX'
            pdesignation = 'CCGV'
            psex_id = 'SMAL' if str(row['ParentGender']) == 'Male' else 'SFEM'
            pdate_of_birth = row['ParentDateofBirth']
            pgsql_cursor.execute("INSERT INTO reg_person(first_name, other_names, surname, designation, sex_id, date_of_birth, is_void, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                                 (pfirst_name, pother_names, psurname, pdesignation, psex_id, pdate_of_birth, is_void, created_at))
            # conn2.commit()
            parent_pk = pgsql_cursor.fetchone()[0]
            # print 'inserting records into reg_person(parent) . . .'

            # insert into reg_person_parent
            identifier_type_id = 'INTL'
            identifier = row['ParentIDNumber']
            identifier = row['ParentIDNumber'] if row['ParentIDNumber'] else 'XXXX'
            person_id = parent_pk
            pgsql_cursor.execute("INSERT INTO reg_persons_external_ids(identifier_type_id, identifier, is_void, person_id) VALUES(%s, %s, %s, %s) RETURNING id;",
                                 (identifier_type_id, identifier, is_void, person_id))
            # conn2.commit()
            # print 'inserting records into reg_persons_external_ids . . .'

            # insert into ovc_household
            hash_key = uuid.uuid4()
            psycopg2.extras.register_uuid()
            head_person_id = parent_pk
            pgsql_cursor.execute("INSERT INTO ovc_household(id, head_identifier, created_at, is_void, head_person_id) VALUES(%s, %s, %s, %s, %s) RETURNING id;",
                                 (hash_key, identifier, created_at, is_void, head_person_id))
            # conn2.commit()
            household_pk = pgsql_cursor.fetchone()[0]

            HouseHoldheadIDs.append(row['ClientHouseHoldheadID'])
            dictXarray.append({
                'child_person_id': person_pk,
                'householdhead_id': row['ClientHouseHoldheadID'],
                'household_id': household_pk,
                'parent_id': parent_pk
            })
            # print 'inserting records into ovc_household . . .'

            hash_key = uuid.uuid4()
            psycopg2.extras.register_uuid()
            hh_head = False
            member_type = 'CCGV'
            member_alive = 'AYES'
            death_cause = None
            date_linked = created_at
            date_delinked = None
            house_hold_id = household_pk
            person_id = parent_pk
            pgsql_cursor.execute("INSERT INTO ovc_household_members(id, hh_head, member_type, member_alive, death_cause, date_linked, date_delinked, is_void,house_hold_id, person_id) VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s) RETURNING id;",
                                 (hash_key, hh_head, member_type, member_alive, death_cause, date_linked, date_delinked, is_void, house_hold_id, person_id))
            # conn2.commit()
            # print 'inserting records into ovc_household_members (parent) . . .'

            # insert reg_persons_types_parent
            person_type_id = 'TBGR'
            date_began = created_at
            date_ended = None
            person_id = parent_pk
            pgsql_cursor.execute("INSERT INTO reg_persons_types(person_type_id, date_began, date_ended, person_id, is_void) VALUES(%s, %s, %s, %s, %s) RETURNING id;",
                                 (person_type_id, date_began, date_ended, person_id, is_void))
            # conn2.commit()
            # print 'inserting records into reg_persons_types . . .'

            # insert into reg_persons_geo_parent
            date_linked = created_at
            date_delinked = None
            area_type = 'GPRV'
            # fields = translator(7, row['WardName'])
            # area_id = fields['area_id']
            person_id = parent_pk
            pgsql_cursor.execute("INSERT INTO reg_persons_geo(date_linked, date_delinked, area_type, area_id, person_id, is_void) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;",
                                 (date_linked, date_delinked, area_type, area_id, person_id, is_void))
            # conn2.commit()
            # print 'inserting records into reg_persons_geo(parent) . . .'

            # insert into reg_persons_guardians
            date_linked = created_at
            date_delinked = None
            relationship = 'CGPF' if row[
                'ClientCareTaker'] == 'Father' else 'CGPM'
            child_headed = False
            child_person_id = person_pk
            guardian_person_id = parent_pk
            pgsql_cursor.execute("INSERT INTO reg_persons_guardians(date_linked, date_delinked, relationship, child_headed, child_person_id, guardian_person_id, is_void) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                                 (date_linked, date_delinked, relationship, child_headed, child_person_id, guardian_person_id, is_void))
            # conn2.commit()
            # print 'inserting records into reg_persons_guardians . . .'

        # insert into reg_persons_siblings.insert into ovc_household_members
        date_linked = created_at
        date_delinked = None
        remarks = ''
        child_person_id = None
        sibling_person_id = person_pk
        if dictXarray:
            for d in dictXarray:
                if d['householdhead_id'] == row['ClientHouseHoldheadID']:
                    child_person_id = d['child_person_id']
                    if child_person_id != person_pk:
                        pgsql_cursor.execute("INSERT INTO reg_persons_siblings(date_linked, date_delinked, remarks, child_person_id, sibling_person_id, is_void) VALUES(%s, %s, %s, %s, %s, %s) RETURNING id;",
                                             (date_linked, date_delinked, remarks, d['child_person_id'], sibling_person_id, is_void))
                        # conn2.commit()
                        # print 'inserting records into reg_persons_siblings . . .'
                    hash_key = uuid.uuid4()
                    psycopg2.extras.register_uuid()
                    hh_head = False
                    member_type = 'TBVC'
                    member_alive = 'AYES'
                    death_cause = None
                    date_linked = created_at
                    date_delinked = None
                    house_hold_id = d['household_id']
                    person_id = person_pk
                    pgsql_cursor.execute("INSERT INTO ovc_household_members(id, hh_head, member_type, member_alive, death_cause, date_linked, date_delinked, is_void,house_hold_id, person_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                                         (hash_key, hh_head, member_type, member_alive, death_cause, date_linked, date_delinked, is_void, house_hold_id, person_id))
                    # conn2.commit()
                    # print 'inserting records into ovc_household_members(ovc). . .'        

        # insert into ovc_registration
        registration_date = row['ClientDateofRegistration']
        # Changed from  AMURT
        client_disabled = check_column(row, 'ClientIsDisabled')
        has_bcert = True if check_int(row['ClientBirthCert']) == 1 else False
        is_disabled = True if client_disabled else False

        hiv_status = None
        if check_int(row['ClientHivStatus'])==1:
            hiv_status = 'HSTP'
        elif check_int(row['ClientHivStatus'])==2:
            hiv_status = 'HSTN'
        elif check_int(row['ClientHivStatus'])==3:
            hiv_status = 'HSKN'
        else:
            hiv_status = 'XXXX'

        school_level = None
        if check_int(row['ClientSchoolLevel'])==1:
            school_level = 'SLEC'
        elif check_int(row['ClientSchoolLevel'])==2:
            school_level = 'SLPR'
        elif check_int(row['ClientSchoolLevel'])==3:
            school_level = 'SLSE'
        elif check_int(row['ClientSchoolLevel'])==4:
            school_level = 'SLTV'
        elif check_int(row['ClientSchoolLevel'])==5:
            school_level = 'SLNS'
        else:
            school_level = 'XXXX'

        immunization_status = None
        if check_int(row['ClientImmunization'])==1:
            immunization_status = 'IMFI'
        elif check_int(row['ClientImmunization'])==2:
            immunization_status = 'IMNC'
        elif check_int(row['ClientImmunization'])==3:
            immunization_status = 'IMNI'
        elif check_int(row['ClientImmunization'])==4:
            immunization_status = 'IMKN'
        else:
            immunization_status = 'XXXX'

        org_unique_id = org_unit_id
        exit_date = row['ClientDateofExit']
        exited = row['ClientExited']
        caretaker_id = row['ClientHouseHoldheadID']
        art_status = row['ClientARTStatus']
        facility = row['Facility']
        ccc_number = 'XXXX'
        date_linked = created_at
        child_cbo_id = org_unit_id
        child_chv_id = chv_pk if chv_pk else 1
        is_active = False if exited else True
        hash_key = uuid.uuid4()
        psycopg2.extras.register_uuid()
        pgsql_cursor.execute("INSERT INTO ovc_registration(id, registration_date, has_bcert, is_disabled, hiv_status, school_level, immunization_status, org_unique_id, exit_date, created_at, is_void, caretaker_id, child_cbo_id, child_chv_id, person_id, is_active) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                             (hash_key, registration_date, has_bcert, is_disabled, hiv_status, school_level, immunization_status, org_unique_id, exit_date, created_at, is_void, parent_pk, child_cbo_id, child_chv_id, person_pk, is_active))

        hkey = uuid.uuid4()
        '''
        if facility:
            facility_id = get_facility(pgsql_cursor, facility)
            psycopg2.extras.register_uuid()
            pgsql_cursor.execute("INSERT INTO ovc_care_health(id, person_id, "
                                 "facility_id, art_status, date_linked, "
                                 "ccc_number, created_at, is_void) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (hkey, person_pk, facility_id, art_status,
                                  date_linked, ccc_number, created_at, is_void))
        # conn2.commit()
        '''
        # print 'inserting records into ovc_registration . . .'
        OVCID_MATRIX.append({
            'person_pk': person_pk,
            'OVCID': OVCID,
            'household_pk': household_pk
        })
        OVCID_OIDS.append([person_pk, OVCID, household_pk])

    write_csv('test.csv', OVCID_OIDS)
    pgsql_conn.commit()
    exit()
    # ---------------  MIGRATE CSI DATA ------------------- ###
    for data in OVCID_MATRIX:
        person_pk = data['person_pk']
        OVCID = data['OVCID']
        mssql_cursor.execute("SELECT NeedsAssessmentMain.NeedsAssessmentID AS NeedsAssessmentID, NeedsAssessmentMain.DateofAssessment AS DateofAssessment, NeedsAssessmentMain.Is_InitialAssessment AS Is_InitialAssessment FROM NeedsAssessmentMain WHERE NeedsAssessmentMain.OVCID='" + OVCID + "'")
        for row in mssql_cursor.fetchall():
            OVCCareEvents_CSI.append({
                'person_pk': person_pk,
                'needs_assessment_pk': row['NeedsAssessmentID'],
                'date_of_assessment': row['DateofAssessment'],
                'is_initial': row['Is_InitialAssessment']})
    cscnt, tcscnt = 0, len(OVCCareEvents_CSI)
    for OVCCareEvents in OVCCareEvents_CSI:
        cscnt += 1
        print 'events record number ', cscnt, '/', tcscnt
        NeedsAssessmentPK = OVCCareEvents['needs_assessment_pk']

        # insert into ovc_care_events
        hash_key = uuid.uuid4()
        hash_key2 = uuid.uuid4()
        psycopg2.extras.register_uuid()
        event_type_id = 'FCSI'
        event_counter = 0 if OVCCareEvents['is_initial'] else 1
        event_score = 0
        date_of_event = OVCCareEvents['date_of_assessment']
        created_by = USER_ID
        timestamp_created = datetime.datetime.now()
        is_void = False
        sync_id = None
        # app_user = models.ForeignKey(AppUser, default=1)
        person = OVCCareEvents['person_pk']
        house_hold = None
        pgsql_cursor.execute("INSERT INTO ovc_care_events(event, event_type_id, event_counter, event_score, date_of_event, is_void, person_id, house_hold_id, timestamp_created, created_by, sync_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING event;",
                             (hash_key, event_type_id, event_counter, event_score, date_of_event, is_void, person, house_hold, timestamp_created, created_by, hash_key2))
        # conn2.commit()
        event_pk = pgsql_cursor.fetchone()[0]
        # print 'inserting records into ovc_care_events(CSI) . . .'

        # TAB1
        mssql_cursor.execute("SELECT NeedsAssessmentMain.NeedsAssessmentID AS NeedsAssessmentID, NeedsAssessmentMain.OVCID AS OVCID, NeedsAssessmentMain.DateofAssessment AS DateofAssessment, " +
                             "NeedsAssessmentMain.Is_InitialAssessment AS Is_InitialAssessment, NeedsAssessment.DomainID, NeedsAssessment.SubdomainID, Domain.Domain AS Domain, Goal.Goal AS Goal, " +
                             "SubDomain.Subdomain AS SubDomain FROM NeedsAssessmentMain INNER JOIN " +
                             "NeedsAssessment ON NeedsAssessmentMain.NeedsAssessmentID = NeedsAssessment.NeedsAssessmentID INNER JOIN " +
                             "Domain ON NeedsAssessment.DomainID = Domain.DomainID INNER JOIN " +
                             "Goal ON NeedsAssessment.GoalID = Goal.GoalID INNER JOIN " +
                             "SubDomain ON NeedsAssessment.SubdomainID = SubDomain.SubdomainID " +
                             "WHERE NeedsAssessmentMain.NeedsAssessmentID='" + NeedsAssessmentPK + "'")
        for row in mssql_cursor:
            # insert into ovc_care_eav
            hash_key = uuid.uuid4()
            hash_key2 = uuid.uuid4()
            psycopg2.extras.register_uuid()
            eav_id = hash_key
            entity = translator(1, row['SubDomain'])
            attribute = 'FCSI'
            value = translator(2, row['Goal'])
            value_for = None
            event = event_pk
            is_void = False
            sync_id = hash_key2
            pgsql_cursor.execute("INSERT INTO ovc_care_eav(eav_id, entity, attribute, value, value_for, event_id, is_void, sync_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING eav_id;",
                                 (eav_id, entity, attribute, value, value_for, event, is_void, sync_id))
            # conn2.commit()
            # print 'inserting records into ovc_care_eav(CSI) . . .'

        # TAB2
        mssql_cursor.execute("SELECT NeedsAssessmentMain.NeedsAssessmentID, NeedsAssessmentMain.OVCID, NeedsAssessmentMain.DateofAssessment," +
                             "NeedsAssessmentMain.Is_InitialAssessment, PriorityNeeds.PriorityID," +
                             "ServiceStatus.ServiceStatus AS ServiceStatus, ServicesProvided.Domainid, ServicesProvided.Providerid, Provider.Provider AS ServiceProvider " +
                             "FROM NeedsAssessmentMain INNER JOIN " +
                             "PriorityNeeds ON NeedsAssessmentMain.NeedsAssessmentID = PriorityNeeds.NeedsAssessmentID INNER JOIN " +
                             "ServiceStatus ON PriorityNeeds.PriorityID = ServiceStatus.SSID INNER JOIN " +
                             "ServicesProvided ON NeedsAssessmentMain.NeedsAssessmentID = ServicesProvided.NeedsAssessmentId INNER JOIN " +
                             "Provider ON ServicesProvided.Providerid = Provider.ProviderID " +
                             "WHERE NeedsAssessmentMain.NeedsAssessmentID='" + NeedsAssessmentPK + "'")
        for row in mssql_cursor:
            hash_key = uuid.uuid4()
            hash_key2 = uuid.uuid4()
            hash_key3 = uuid.uuid4()
            psycopg2.extras.register_uuid()
            priority_id = hash_key
            fields = translator(0, row['ServiceStatus'])
            domain = fields['domain']
            service = fields['service']
            event = event_pk
            service_grouping_id = hash_key3
            is_void = False
            sync_id = hash_key2
            pgsql_cursor.execute("INSERT INTO ovc_care_priority(priority_id, domain, service, service_grouping_id, event_id, is_void, sync_id) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING priority_id;",
                                 (priority_id, domain, service, service_grouping_id, event, is_void, sync_id))
            # conn2.commit()
            # print 'inserting records into ovc_care_priority(CSI) . . .'

        # TAB3
        mssql_cursor.execute("SELECT NeedsAssessmentMain.NeedsAssessmentID, NeedsAssessmentMain.OVCID, NeedsAssessmentMain.DateofAssessment," +
                             "NeedsAssessmentMain.Is_InitialAssessment, ServiceStatus.ServiceStatus AS ServiceStatus," +
                             "ServicesProvided.Domainid, Provider.Provider AS ServiceProvider " +
                             "FROM NeedsAssessmentMain INNER JOIN " +
                             "ServicesProvided ON NeedsAssessmentMain.NeedsAssessmentID = ServicesProvided.NeedsAssessmentId INNER JOIN " +
                             "ServiceStatus ON ServicesProvided.SSID = ServiceStatus.SSID INNER JOIN " +
                             "Provider ON ServicesProvided.Providerid = Provider.ProviderID " +
                             "WHERE NeedsAssessmentMain.NeedsAssessmentID='" + NeedsAssessmentPK + "'")
        for row in mssql_cursor:
            hash_key = uuid.uuid4()
            hash_key2 = uuid.uuid4()
            hash_key3 = uuid.uuid4()
            psycopg2.extras.register_uuid()
            service_id = hash_key
            fields = translator(0, row['ServiceStatus'])
            service_provided = fields['service']
            # service_provider = translator(6, row['ServiceProvider'])
            service_provider = 'PUSG'
            place_of_service = org_unit_name
            date_of_encounter_event = None
            event = event_pk
            service_grouping_id = hash_key2
            is_void = False
            sync_id = hash_key3
            pgsql_cursor.execute("INSERT INTO ovc_care_services(service_id, service_provided, service_provider, place_of_service, date_of_encounter_event, service_grouping_id, event_id, is_void, sync_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING service_id;",
                                 (service_id, service_provided, service_provider, place_of_service, date_of_encounter_event, service_grouping_id, event, is_void, sync_id))
            # conn2.commit()
            # print 'inserting records into ovc_care_services(CSI) . . .'

    # ---------------  MIGRATE F1A DATA ------------------- ###
    for data in OVCID_MATRIX:
        person_pk = data['person_pk']
        OVCID = data['OVCID']

        mssql_cursor.execute(
            "SELECT SSVID, DateofVisit, VisitType FROM StatusAndServiceVisit WHERE OVCID='" + OVCID + "'")
        for row in mssql_cursor.fetchall():
            OVCCareEvents_F1A.append({
                'person_pk': person_pk,
                'service_pk': row['SSVID'],
                'date_of_visit': row['DateofVisit'],
                'visit_type': row['VisitType']})
    crcnt, tcrcnt = 0, len(OVCCareEvents_F1A)
    for OVCCareEvents in OVCCareEvents_F1A:
        crcnt += 1
        print 'F1A record number ', crcnt, '/', tcrcnt
        ServicePK = OVCCareEvents['service_pk']

        # insert into ovc_care_events
        hash_key = uuid.uuid4()
        hash_key2 = uuid.uuid4()
        psycopg2.extras.register_uuid()
        event_type_id = 'FSAM'
        event_counter = 0
        event_score = 0
        date_of_event = OVCCareEvents['date_of_visit']
        created_by = USER_ID
        timestamp_created = datetime.datetime.now()
        is_void = False
        sync_id = None
        # app_user = models.ForeignKey(AppUser, default=1)
        person = OVCCareEvents['person_pk']
        house_hold = None
        pgsql_cursor.execute("INSERT INTO ovc_care_events(event, event_type_id, event_counter, event_score, date_of_event, is_void, person_id, house_hold_id, timestamp_created, created_by, sync_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING event;",
                             (hash_key, event_type_id, event_counter, event_score, date_of_event, is_void, person, house_hold, timestamp_created, created_by, hash_key2))
        # conn2.commit()
        event_pk = pgsql_cursor.fetchone()[0]
        # print 'inserting records into ovc_care_events(F1A) . . .'

        # TAB 1
        mssql_cursor.execute("SELECT StatusAndServiceVisit.SSVID, StatusAndServiceVisit.OVCID, StatusAndServiceVisit.DateofVisit, StatusAndServiceVisit.VisitType, StatusAndServiceMonitoring_Assessment.SSID," +
                             "ServiceStatus.ServiceStatus AS ServiceStatus, ServiceStatus.CSID, CoreServices.CoreService AS CoreService, Domain.Domain FROM StatusAndServiceVisit INNER JOIN " +
                             "StatusAndServiceMonitoring_Assessment ON StatusAndServiceVisit.SSVID = StatusAndServiceMonitoring_Assessment.SSVID INNER JOIN " +
                             "ServiceStatus ON StatusAndServiceMonitoring_Assessment.SSID = ServiceStatus.SSID INNER JOIN " +
                             "CoreServices ON ServiceStatus.CSID = CoreServices.CSID INNER JOIN " +
                             "Domain ON CoreServices.Domainid = Domain.DomainID " +
                             "WHERE (StatusAndServiceVisit.VisitType = 'monitor') AND StatusAndServiceVisit.SSVID ='" + ServicePK + "'")
        for row in mssql_cursor:
            hash_key = uuid.uuid4()
            hash_key2 = uuid.uuid4()
            hash_key3 = uuid.uuid4()
            psycopg2.extras.register_uuid()
            assessment_id = hash_key
            fields = translator(3, row['ServiceStatus'])
            domain = fields['domain']
            service = fields['service']
            fields = translator(3, row['CoreService'])
            service_status = fields['service']
            event = event_pk
            service_grouping_id = hash_key2
            is_void = True
            sync_id = hash_key3
            pgsql_cursor.execute("INSERT INTO ovc_care_assessment(assessment_id, domain, service, service_status, service_grouping_id, is_void, sync_id, event_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING assessment_id;",
                                 (assessment_id, domain, service, service_status, service_grouping_id, is_void, sync_id, event))
            # conn2.commit()
            # print 'inserting records into ovc_care_assessment(F1A) . . .'

        # TAB2
        mssql_cursor.execute("SELECT StatusAndServiceVisit.SSVID, StatusAndServiceVisit.OVCID, StatusAndServiceVisit.DateofVisit," +
                             "OVCVisitsCriticalEvents.CriticalEventID, CriticalEvents.EventName AS EventName FROM StatusAndServiceVisit INNER JOIN " +
                             "OVCVisitsCriticalEvents ON StatusAndServiceVisit.SSVID = OVCVisitsCriticalEvents.SSVID INNER JOIN " +
                             "CriticalEvents ON OVCVisitsCriticalEvents.CriticalEventID = CriticalEvents.CriticalEventsID " +
                             "WHERE StatusAndServiceVisit.SSVID ='" + ServicePK + "'")
        for row in mssql_cursor:
            # insert into ovc_care_eav
            hash_key = uuid.uuid4()
            hash_key2 = uuid.uuid4()
            psycopg2.extras.register_uuid()
            eav_id = hash_key
            entity = 'CEVT'
            attribute = 'FSAM'
            fields = translator(4, row['EventName'])
            value = fields['service']
            value_for = None
            event = event_pk
            is_void = False
            sync_id = hash_key2
            pgsql_cursor.execute("INSERT INTO ovc_care_eav(eav_id, entity, attribute, value, value_for, event_id, is_void, sync_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING eav_id;",
                                 (eav_id, entity, attribute, value, value_for, event, is_void, sync_id))
            # conn2.commit()
            # print 'inserting records into ovc_care_eav(F1A) . . .'

        # TAB3
        mssql_cursor.execute("SELECT StatusAndServiceVisit.SSVID, StatusAndServiceVisit.OVCID, StatusAndServiceVisit.DateofVisit," +
                             "ServiceStatus.ServiceStatus AS ServiceStatus, PriorityMonitoring.PriorityID FROM StatusAndServiceVisit INNER JOIN " +
                             "PriorityMonitoring ON StatusAndServiceVisit.SSVID = PriorityMonitoring.SSVID INNER JOIN " +
                             "ServiceStatus ON PriorityMonitoring.PriorityID = ServiceStatus.SSID " +
                             "WHERE StatusAndServiceVisit.SSVID ='" + ServicePK + "'")
        for row in mssql_cursor:
            hash_key = uuid.uuid4()
            hash_key2 = uuid.uuid4()
            hash_key3 = uuid.uuid4()
            psycopg2.extras.register_uuid()
            priority_id = hash_key
            fields = translator(0, row['ServiceStatus'])
            domain = fields['domain']
            service = fields['service']
            event = event_pk
            service_grouping_id = hash_key3
            is_void = False
            sync_id = hash_key2
            pgsql_cursor.execute("INSERT INTO ovc_care_priority(priority_id, domain, service, service_grouping_id, event_id, is_void, sync_id) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING priority_id;",
                                 (priority_id, domain, service, service_grouping_id, event, is_void, sync_id))
            # conn2.commit()
            # print 'inserting records into ovc_care_priority(F1A) . . .'

        # TAB4
        mssql_cursor.execute("SELECT StatusAndServiceVisit.SSVID, StatusAndServiceVisit.OVCID, StatusAndServiceVisit.DateofVisit, StatusAndServiceVisit.VisitType, StatusAndServiceMonitoring_Service.SSID," +
                             "ServiceStatus.ServiceStatus AS ServiceStatus, ServiceStatus.CSID, CoreServices.CoreService AS CoreService, Domain.Domain FROM StatusAndServiceVisit INNER JOIN " +
                             "StatusAndServiceMonitoring_Service ON StatusAndServiceVisit.SSVID = StatusAndServiceMonitoring_Service.SSVID INNER JOIN " +
                             "ServiceStatus ON StatusAndServiceMonitoring_Service.SSID = ServiceStatus.SSID INNER JOIN " +
                             "CoreServices ON ServiceStatus.CSID = CoreServices.CSID INNER JOIN " +
                             "Domain ON CoreServices.Domainid = Domain.DomainID " +
                             "WHERE (StatusAndServiceVisit.VisitType = 'service') AND StatusAndServiceVisit.SSVID ='" + ServicePK + "'")
        for row in mssql_cursor:
            hash_key = uuid.uuid4()
            hash_key2 = uuid.uuid4()
            hash_key3 = uuid.uuid4()
            psycopg2.extras.register_uuid()
            service_id = hash_key
            fields = translator(0, row['ServiceStatus'])
            service_provided = fields['service']
            service_provider = 'PUSG'
            place_of_service = org_unit_name
            date_of_encounter_event = None
            event = event_pk
            service_grouping_id = hash_key2
            is_void = False
            sync_id = hash_key3
            pgsql_cursor.execute("INSERT INTO ovc_care_services(service_id, service_provided, service_provider, place_of_service, date_of_encounter_event, service_grouping_id, event_id, is_void, sync_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING service_id;",
                                 (service_id, service_provided, service_provider, place_of_service, date_of_encounter_event, service_grouping_id, event, is_void, sync_id))
            # conn2.commit()
            # print 'inserting records into ovc_care_services(F1A) . . .'

    # ---------------  MIGRATE HHVA DATA ------------------- ###
    for data in OVCID_MATRIX:
        person_pk = data['person_pk']
        household_pk = data['household_pk']
        OVCID = data['OVCID']
        mssql_cursor.execute(
            "SELECT HHAssessmentid, OVCID, DateofAssessment, Is_InitialAssessment FROM HHAssessmentMain WHERE OVCID='" + OVCID + "'")
        for row in mssql_cursor.fetchall():
            if row['HHAssessmentid'] not in HHVAPKs:
                HHVAPKs.append(row['HHAssessmentid'])
                OVCCareEvents_HHVA.append({
                    'person_pk': person_pk,
                    'household_pk': household_pk,
                    'hhva_pk': row['HHAssessmentid'],
                    'date_of_assessment': row['DateofAssessment'],
                    'is_initial': row['Is_InitialAssessment']})

    hvcnt, thvcnt = 0, len(HHVAPKs)
    for OVCCareEvents in OVCCareEvents_HHVA:
        hvcnt += 1
        print 'HHVA record number ', hvcnt, '/', thvcnt
        HHVAFK = OVCCareEvents['hhva_pk']

        # insert into ovc_care_events
        hash_key = uuid.uuid4()
        hash_key2 = uuid.uuid4()
        psycopg2.extras.register_uuid()
        event_type_id = 'FHSA'
        event_counter = 0 if OVCCareEvents['is_initial'] else 1
        event_score = 0
        date_of_event = OVCCareEvents['date_of_assessment']
        created_by = USER_ID
        timestamp_created = datetime.datetime.now()
        is_void = False
        sync_id = None
        person = None
        house_hold = OVCCareEvents['household_pk']
        pgsql_cursor.execute("INSERT INTO ovc_care_events(event, event_type_id, event_counter, event_score, date_of_event, is_void, person_id, house_hold_id, timestamp_created, created_by, sync_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING event;",
                             (hash_key, event_type_id, event_counter, event_score, date_of_event, is_void, person, house_hold, timestamp_created, created_by, hash_key2))
        # conn2.commit()
        event_pk = pgsql_cursor.fetchone()[0]
        # print 'inserting records into ovc_care_events(HHVA) . . .'

        mssql_cursor.execute("SELECT HHAssessmentMain.HHAssessmentid, HHAssessmentMain.OVCID, HHAssessmentMain.DateofAssessment," +
                             "HHAssessmentMain.Is_InitialAssessment,HHAssessment.Responseid AS ResponseId, HHAssessment.Amount AS Amount, HHAssessment.Condition_Size AS Size," +
                             "HHResponses.HHCodeid, HHResponses.Response AS Response, HHAssessentCodes.HHDomainid, HHAssessentCodes.HHCode AS HHCode " +
                             "FROM HHAssessmentMain INNER JOIN " +
                             "HHAssessment ON HHAssessmentMain.HHAssessmentid = HHAssessment.HHAssessmentid INNER JOIN " +
                             "HHResponses ON HHAssessment.Responseid = HHResponses.Responseid INNER JOIN " +
                             "HHAssessentCodes ON HHResponses.HHCodeid = HHAssessentCodes.HHCodeid " +
                             "WHERE HHAssessmentMain.HHAssessmentid ='" + HHVAFK + "'")
        for row in mssql_cursor:
            values = []
            values.append(row['Response'])
            values.append(row['ResponseId'])
            values.append(row['HHCode'])
            values.append(row['Amount'])
            values.append(row['Size'])
            fields = translator(5, values)
            for field in fields:
                hash_key = uuid.uuid4()
                hash_key2 = uuid.uuid4()
                psycopg2.extras.register_uuid()
                eav_id = hash_key
                entity = field['entity']
                attribute = field['attribute']
                value = field['value']
                value_for = field['value_for']
                event = event_pk
                is_void = False
                sync_id = hash_key2
            pgsql_cursor.execute("INSERT INTO ovc_care_eav(eav_id, entity, attribute, value, value_for, event_id, is_void, sync_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING eav_id;",
                                 (eav_id, entity, attribute, value, value_for, event, is_void, sync_id))
            # conn2.commit()
            # print 'inserting records into ovc_care_eav(HHVA) . . .'

    # commit
    mssql_cursor.execute("DROP TABLE TEMPORARY_FLAT_TABLE")
    mssql_conn.commit()
    pgsql_conn.commit()

    toc = time()
    print 'extracted data into postgresql in (%s) secs ...' % (toc - tic)

    # close connections to Sql Server & Postgresql
    mssql_conn.close()
    pgsql_conn.close()
    print 'Data imported successfully.'

except Exception as e:
    print 'An error occured when running the script - (%s)' % str(e)

    mssql_cursor.execute("DROP TABLE %s" % (TMP_TABLE))
    mssql_conn.commit()
    mssql_conn.close()
    pgsql_conn.close()
    traceback.print_exc()
    raise e
else:
    pass
# ---------------------------------END DATA SCRIPT ----------------#
