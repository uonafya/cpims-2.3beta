import csv

with open('cpims_ovc_facility.csv') as csvfile:
    facilities_dict = dict()
    all_facilities = csv.DictReader(csvfile)
    for row in all_facilities:
        # curr_group = []
        curr_item = row.get('id')
        # curr_item.append(row.get('id'))
        if row.get('facility_subcounty') in facilities_dict:
            curr_group = facilities_dict.get(row.get('facility_subcounty'))
            curr_group.append(curr_item)
            facilities_dict[row.get('facility_subcounty')] = curr_group
        else:
            new_item = []
            new_item.append(row.get('id'))
            key = row.get('facility_subcounty')
            facilities_dict[key] = new_item
    # print(facilities_dict)

    with open('mapped-duplicates.csv', 'a') as f:
        for key, value in facilities_dict.items():
            if len(value) > 1:
                for id in value:
                    # print(value[0] + " --> " + id + " --> " + str(len(value)))
                    writer = csv.writer(f)
                    if str(value[0]) != str(id):
                        print(value[0] + " --> " + id + " --> " + str(len(value)))
                        writer.writerow([value[0], id, len(value)])

