import csv
from cpovc_main.models import SetupList
with open('/home/richie/Desktop/fixtures3 - Sheet1.csv') as csv_file:
	dict_reader = csv.DictReader(csv_file)
	for row in dict_reader:
         item_category = row['item_category']
         uc = row['user_configurable']
         fn = row['field_name']
         isc = row['item_sub_category']
         itd = row['item_id']
         ids = row['item_description_short']
        #  order = row['the_order']
         item_dis = row['item_description'] 
	 
	 
         setuplist = SetupList(item_description=item_dis,item_id=itd,item_description_short=ids,item_category=item_category,item_sub_category=isc
                              ,field_name=fn,user_configurable=uc,)
         setuplist.save()


