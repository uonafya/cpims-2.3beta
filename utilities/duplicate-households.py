import csv

with open('ovc_households_cleaning.csv') as csvfile:
    households_dict = dict()
    all_households = csv.DictReader(csvfile)
    for row in all_households:
        # curr_group = []
        curr_item = row.get('id')
        # curr_item.append(row.get('id'))
        if row.get('head_person_id') in households_dict:
            curr_group = households_dict.get(row.get('head_person_id'))
            curr_group.append(curr_item)
            households_dict[row.get('head_person_id')] = curr_group
        else:
            new_item = []
            new_item.append(row.get('id'))
            key = row.get('head_person_id')
            households_dict[key] = new_item
    # print(households_dict)

    with open('de-duplicated-households.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(['household_head_id', 'hh_id_to_retain', 'hh_id_to_move', 'tree_depth'])
        for key, value in households_dict.items():
            if len(value) > 1:
                for id in value:
                    # print(value[0] + " --> " + id + " --> " + str(len(value)))
                    if str(value[0]) != str(id):
                        print(key + "  " + value[0] + " <-- " + id + "  " + str(len(value)))
                        writer.writerow([key, value[0], id, len(value)])
