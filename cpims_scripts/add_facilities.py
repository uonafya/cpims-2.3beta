from cpovc_ovc.models import OVCFacility as facility
import csv

# read facilities from csv and save to facilities model
with open('cpims-facilities-addition.csv') as csvfile:
    facilities = csv.reader(csvfile, delimiter=',')
    for row in facilities:
        facility.facility_code = row[0]
        facility.facility_name = row[1]
        facility.sub_county = row[2]
        print (row[0] + "  " + row[1] + "  " + row[2])
        facility.save()
