import csv
import datetime

from cpovc_forms.models import OVCCareEvents, OVCCareCpara, RegPerson, OVCCareQuestions, OVCHouseHold
from cpovc_main.functions import convert_date
from cpovc_ovc.models import OVCHHMembers

keys = ('CP_GEN_01', 'CP_GEN_02', 'CP_HEL_1.1', 'CP_HEL_1.2', 'CP_HEL_1.3', 'CP_HEL_1.4', 'CP_HEL_B1', 'CP_HEL_2.1',
        'CP_HEL_2.2', 'CP_HEL_2.3', 'CP_HEL_B2', 'CP_HEL_3.1', 'CP_HEL_3.2', 'CP_HEL_3.3', 'CP_HEL_3.4', 'CP_HEL_3.5',
        'CP_HEL_3.6', 'CP_HEL_3.7', 'CP_HEL_3.8', 'CP_HEL_3.9', 'CP_HEL_3.10a', 'CP_HEL_3.10b', 'CP_HEL_B3',
        'CP_HEL_4.1', 'CP_HEL_4.2', 'CP_HEL_4.3', 'CP_HEL_4.4', 'CP_HEL_4.5', 'CP_HEL_B4', 'CP_HEL_5.1', 'CP_HEL_5.2',
        'CP_HEL_5.3', 'CP_HEL_5.4', 'CP_HEL_5.5', 'CP_HEL_5.6', 'CP_HEL_B5', 'CP_HEL_6.1', 'CP_HEL_6.2', 'CP_HEL_B6',
        'CP_STA_7.1', 'CP_STA_7.2', 'CP_STA_7.3', 'CP_STA_B7', 'CP_STA_8.1', 'CP_STA_8.2', 'CP_STA_8.3', 'CP_STA_B8',
        'CP_STA_9.1', 'CP_STA_9.2', 'CP_STA_B9', 'CP_STA_10.1', 'CP_STA_10.3', 'CP_STA_B10', 'CP_SAF_11.1',
        'CP_SAF_11.2', 'CP_SAF_11.3', 'CP_SAF_11.4', 'CP_SAF_11.5', 'CP_SAF_B11', 'CP_SAF_12.1', 'CP_SAF_12.2',
        'CP_SAF_12.3', 'CP_SAF_12.4a', 'CP_SAF_12.4b', 'CP_SAF_12.4c', 'CP_SAF_B12', 'CP_SAF_13.1', 'CP_SAF_13.2',
        'CP_SAF_13.3', 'CP_SAF_13.4', 'CP_SAF_13.5', 'CP_SAF_B13', 'CP_SAF_14.1', 'CP_SAF_14.2', 'CP_SAF_B14',
        'CP_SAF_15.2', 'CP_SAF_15.3', 'CP_SAF_15.4', 'CP_SAF_B15', 'CP_SCH_16.1', 'CP_SCH_16.2', 'CP_SCH_16.3',
        'CP_SCH_16.4', 'CP_SCH_16.5', 'CP_SCH_B16', 'CP_SCH_17.1', 'CP_SCH_17.2', 'CP_SCH_17.3', 'CP_SCH_B17')

event_records_count = 0
cpara_records_count = 0


# try:
with open('/home/fegati/py_projects/cpims_scripts/nilinde-cpara-data-entries.csv') as cpara_file:
    file_reader = csv.DictReader(cpara_file)
    for row in file_reader:
        # create event based on assessment date and return event id
        # print(int(row['OVC CPIMSID']))
        # print (OVCHHMembers.objects.get(person_id=int(row['OVC CPIMSID'])).house_hold_id)
        event_records_count += 1
        try:
            event = OVCCareEvents(event_type_id='CPARA', event_counter=0, event_score=1,
                                  date_of_event=convert_date(row['Date of assessment'], fmt='%d/%m/%Y'),
                                  date_of_previous_event=convert_date(row['Date of assessment'], fmt='%d/%m/%Y'),
                                  created_by=1, timestamp_created=datetime.datetime.now(), is_void=False,
                                  person=RegPerson.objects.get(id=int(row['OVC CPIMSID'])),
                                  house_hold=OVCHouseHold.objects.get(id=OVCHHMembers.objects.get(person_id=int(row['OVC CPIMSID'])).house_hold_id))
            # save the event instance
            event.save()
            answers = {k: row[k] for k in keys}
            for item in answers.keys():
                print({
                    'answer': answers[item],
                    'question_type': OVCCareQuestions.objects.get(question=item).question_type,
                    'domain': OVCCareQuestions.objects.get(question=item).domain,
                    'event': event,
                    'household': OVCHouseHold.objects.get(
                        id=OVCHHMembers.objects.get(person_id=int(row['OVC CPIMSID'])).house_hold_id),
                    'question': OVCCareQuestions.objects.get(question=item),
                    'date_of_event': convert_date(row['Date of assessment'], fmt='%d/%m/%Y'),
                    'question_code': OVCCareQuestions.objects.get(question=item).code
                })
                # construct cpara instance for each each answer in each question
                cpara = OVCCareCpara(person=RegPerson.objects.get(id=int(row['OVC CPIMSID'])),
                                     answer=answers[item],
                                     question_type=OVCCareQuestions.objects.get(question=item).question_type,
                                     domain=OVCCareQuestions.objects.get(question=item).domain,
                                     event=event,
                                     household=OVCHouseHold.objects.get(
                                         id=OVCHHMembers.objects.get(person_id=int(row['OVC CPIMSID'])).house_hold_id),
                                     question=OVCCareQuestions.objects.get(question=item),
                                     date_of_event=convert_date(row['Date of assessment'], fmt='%d/%m/%Y')
                                     )
                # save the cpara instance
                cpara.save()
                cpara_records_count += 1

        except:
            pass
        print(event.event)
        # filter answers from each row based on question codes

print("Event Records:{}, CPARA Records:{}".format(event_records_count,cpara_records_count))
# except Exception as e:
#     print("The following error occurred: ", e)

