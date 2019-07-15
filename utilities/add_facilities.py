from cpovc_ovc.models import OVCFacility as facility
import csv

# read facilities from csv and save to facilities model
with open('cpims-facilities-addition.csv') as csvfile:
    facilities = csv.reader(csvfile, delimiter=',')
    for row in facilities:
        f = facility(facility_code=row[0], facility_name=row[1], sub_county_id=row[2])
        print (row[0] + "  " + row[1] + "  " + row[2])
        f.save()
