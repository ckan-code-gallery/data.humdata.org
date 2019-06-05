'''
Created on July 2nd, 2015

@author: dan
'''

import sys

import ckan.logic as logic

from ckan.plugins import toolkit as tk

import ckanext.hdx_user_extra.model as ue_model

NotFound = logic.NotFound

check_access = tk.check_access

def user_extra_update(context, data_dict):
    '''
    Updates an user_extra record in database
    :param context:
    :param data_dict: contains 'extras' which is a list of dictionaries. An extras contains 'user_id', 'key',
    and 'new_value'
    :return: list of extras updated
    '''
    session = context['session']
    # model = context['model']
    result = []
    check_access('user_extra_update', context, data_dict)
    for ue in data_dict['extras']:
        try:
            user_extra = ue_model.UserExtra.get(user_id=data_dict['user_id'], key=ue['key'])
            if user_extra is None:
                raise NotFound
            user_extra.value = ue['new_value']
            session.add(user_extra)
            session.commit()
            result.append(user_extra.as_dict())
        except:
            print sys.exc_info()[0]
    return result
