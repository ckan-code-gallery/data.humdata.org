import ckan.lib.helpers as h

import ckanext.hdx_theme.tests.hdx_test_with_inds_and_orgs as hdx_test_with_inds_and_orgs


class TestResponsiveRedirect(hdx_test_with_inds_and_orgs.HDXWithIndsAndOrgsTest):

    def test_responsive_redirect(self):
        desktop_url = h.url_for(controller='package', action='read', id='test_dataset_1')
        light_url = h.url_for('hdx_light_dataset.read', id='test_dataset_1')

        mobile_ua = 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36'
        desktop_ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
        googlebot_mobile_ua = 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        google_desktop1_ua = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        google_desktop2_ua = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36'

        result = self.app.get(desktop_url, headers={
            'User-Agent': desktop_ua
        })
        assert result.status_int == 200, 'Desktop users should get desktop page'

        result = self.app.get(light_url, headers={
            'User-Agent': mobile_ua
        })
        assert result.status_int == 200, 'Mobile users should get light page'

        result = self.app.get(desktop_url, headers={
            'User-Agent': mobile_ua
        })
        assert result.status_int == 302, 'Mobile users should be redirected to mobile page'

        result = self.app.get(light_url, headers={
            'User-Agent': desktop_ua
        })
        assert result.status_int == 302, 'Desktop users should be redirected to desktop page'

        result = self.app.get(light_url + '?force_layout=desktop', headers={
            'User-Agent': mobile_ua
        })
        assert result.status_int == 302, 'Mobile users forcing desktop layout should be redirected to desktop page'

        result = self.app.get(desktop_url, headers={
            'User-Agent': mobile_ua,
            'Cookie': 'hdx_force_layout=desktop'
        })
        assert result.status_int == 200, 'Mobile users with desktop cookie should get the desktop page'

        result = self.app.get(desktop_url + '?force_layout=light', headers={
            'User-Agent': desktop_ua
        })
        assert result.status_int == 302, 'Desktop users forcing light layout should be redirected to light page'

        result = self.app.get(light_url, headers={
            'User-Agent': desktop_ua,
            'Cookie': 'hdx_force_layout=light'
        })
        assert result.status_int == 200, 'Desktop users with light cookie should get the light page'

        # Testing Googlebot
        result = self.app.get(light_url, headers={
            'User-Agent': googlebot_mobile_ua,
        })
        assert result.status_int == 200, 'Googlebot mobile should get the light page'

        result = self.app.get(desktop_url, headers={
            'User-Agent': google_desktop1_ua,
        })
        assert result.status_int == 200, 'Googlebot desktop should get the desktop page'

        result = self.app.get(desktop_url, headers={
            'User-Agent': google_desktop2_ua,
        })
        assert result.status_int == 200, 'Googlebot desktop should get the desktop page'
