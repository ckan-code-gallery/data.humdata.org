
from ckan.common import g
import ckan.lib.helpers as h
import ckan.plugins.toolkit as toolkit
import ckan.authz as authz

get_action = toolkit.get_action
check_access = toolkit.check_access
NotAuthorized = toolkit.NotAuthorized


def find_first_global_settings_url():
    context = {'user': g.user}
    url = None
    if authz.is_sysadmin(g.user):
        url = h.url_for('admin.index')

    if not url:
        try:
            check_access('hdx_carousel_update', context, {})
            url = h.url_for('carousel_settings')
        except NotAuthorized as e:
            pass

    if not url:
        try:
            check_access('hdx_request_data_admin_list', context, {})
            url = h.url_for('ckanadmin_requests_data')
        except NotAuthorized as e:
            pass

    if not url:
        try:
            check_access('admin_page_list', context, {})
            url = h.url_for('pages_show')
        except NotAuthorized as e:
            pass
    return url