from django.test import TestCase
from model_mommy import mommy

from cpovc_main.models import SetupList 


class Testsetuplist(TestCase):
    """Tests for the Setup_Geography model """
    def test_setup_list(self):
      data = {
            'item_id' : 12,
            'item_description' : 'FSM', 
            'item_description_short' : 'female sex workets', 
            'item_category' : 'sex workers', 
            'item_sub_category' : 'sex worker', 
            'the_order' : 123, 
            'user_configurable' : True, 
            'sms_keyword' : False
          }      
        
      testsetuplist = mommy.make(SetupList, **data)    # let create the recored on setupgeo model
      self.assertEqual(1, SetupList.objects.count())   # count created to  be one
      self.assertEqual(data.get('item_id'), testsetuplist.item_id )
      self.assertEqual(data.get('item_description'), testsetuplist.item_description )
      self.assertEqual(data.get('item_description_short'), testsetuplist.item_description_short)
      self.assertEqual(data.get('item_category'), testsetuplist.item_category)
      self.assertEqual( data.get('item_sub_category'), testsetuplist.item_sub_category)
      self.assertEqual(data.get('the_order'), testsetuplist.the_order)
      self.assertEqual(data.get('user_configurable'), testsetuplist.user_configurable)
      self.assertEqual(data.get('sms_keyword'), testsetuplist.sms_keyword)
      