# -*- coding: utf-8 -*-
from flask import Response
from flask import request
from flask_restful import Resource
from dateutil.parser import parse
from langconv import Converter
from datetime import datetime
import pandas as pd
import math
import json
import re
import requests
import constants
import logging
LOG = logging.getLogger(__name__)

def setup_route(api):
    """
        return map of endpoint and handler
    """
    api.add_resource(ASR_test, '/rest/ASR_test')
    
def encapsule_rtn_format(update_kv_map, remove_kv_map):
    rtn_obj = {
                "status_code": 0,
                "msg_response": {}
            }
    if update_kv_map is not None:
        rtn_obj['msg_response']['update'] = update_kv_map
    if remove_kv_map is not None:
        rtn_obj['msg_response']['remove'] = remove_kv_map
    return rtn_obj

def isnan(value):
  try:
      import math
      return math.isnan(float(value))
  except:
      return False

class ASR_test(Resource):
    def post(self):
        json_from_request = json.loads(Converter('zh-hant').convert(request.stream.read().decode('utf-8')))
        LOG.debug('In Give_Fake_Data, data received from TE: %s' % json.dumps(json_from_request, ensure_ascii=False, indent=4))
        df = pd.read_excel("ASR_test.xlsx")
        ID = int(json_from_request['task_info']['ID'])
        # find 
        update_kv_map = {}
        if 'counter' not in json_from_request['task_info']:
            update_kv_map['counter'] = 0
            ans = df.at[df[df['ID'] == ID].index[update_kv_map['counter']], "answer"]
        else:
            update_kv_map['counter'] = json_from_request['task_info']['counter'] + 1
            ans = df.at[df[df['ID'] == ID].index[update_kv_map['counter']], "answer"]
        
        if update_kv_map['counter'] == (len(df[df['ID'] == ID])-1):
            update_kv_map['last_ans'] = "ture"
        update_kv_map['ans'] = ans
            
        ret = encapsule_rtn_format(update_kv_map, None)
        return Response(json.dumps(ret), status=200)