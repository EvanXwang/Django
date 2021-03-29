# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import json
import requests


class ErrorResponse(Exception):
    def __init__(self, *args, **kwargs):
        """ Error response.

        :param args:
        :param kwargs:
        """
        super(self.__class__, self).__init__(*args, **kwargs)


class LineFrontendFramework:
    def __init__(self, channel_access_token):
        """ Create a new LineFrontendFramework instance.

        :param channel_access_token:
        """
        self._headers = {
            'Authorization': 'Bearer {0}'.format(channel_access_token),
            'Content-Type': 'application/json',
        }

    def add(self, view_type, view_url):
        """ Adds an app to LIFF. You can add up to 30 LIFF apps on one channel.

        :param view_type: Size of the LIFF app view to be updated.
            ・ compact:  50% of the screen height of the device
            ・ tall   :  80% of the screen height of the device.
            ・ full   : 100% of the screen height of the device.
        :param view_url: URL of the LIFF app to be updated. Must start with HTTPS.
        :return liffId: URL of the LIFF app. The URL scheme must be https.
        """
        api_url = 'https://api.line.me/liff/v1/apps'
        data = json.dumps({"view": {"type": view_type, "url": view_url}})
        result = requests.post(api_url, headers=self._headers, data=data)
        if result.status_code == 400:
            raise ErrorResponse("""\
[400 Error] The following error reasons are possible.
・The request contains an invalid value.
・The maximum number of LIFF applications that can be added to the channel has been reached.""")
        elif result.status_code == 401:
            raise ErrorResponse("[401 Error] Certification failed.")
        return json.loads(result.content)['liffId']

    def update(self, liff_id, view_type, view_url):
        """ Updates LIFF app settings.

        :param liff_id: ID of the LIFF app to be updated.
        :param view_type: Size of the LIFF app view to be updated.
            ・ compact:  50% of the screen height of the device
            ・ tall   :  80% of the screen height of the device.
            ・ full   : 100% of the screen height of the device.
        :param view_url: URL of the LIFF app to be updated. Must start with HTTPS.
        :return:
        """
        api_url = 'https://api.line.me/liff/v1/apps/{}/view'.format(liff_id)
        data = json.dumps({"type": view_type, "url": view_url})
        result = requests.put(api_url, headers=self._headers, data=data)
        if result.status_code == 401:
            raise ErrorResponse("[401 Error] Certification failed.")
        elif result.status_code == 404:
            raise ErrorResponse("""\
[404 Error] The following error reasons are possible.
・The specified LIFF application does not exist.
・The specified LIFF application belongs to another channel.""")

    def get(self):
        """ Gets information on all the LIFF apps registered in the channel.

        :return:
        """
        api_url = 'https://api.line.me/liff/v1/apps'
        result = requests.get(api_url, headers={"Authorization": self._headers["Authorization"]})
        if result.status_code == 401:
            raise ErrorResponse("[401 Error] Certification failed.")
        elif result.status_code == 404:
            raise ErrorResponse("[404 Error] There is no LIFF application on the channel.")
        return json.loads(result.content)['apps']

    def delete(self, liff_id):
        """ Deletes a LIFF app.

        :param liff_id: ID of the LIFF app to be deleted.
        :return: None
        """
        api_url = 'https://api.line.me/liff/v1/apps/{0}'.format(liff_id)
        result = requests.delete(api_url, headers={"Authorization": self._headers["Authorization"]})
        if result.status_code == 401:
            raise ErrorResponse("[401 Error] Certification failed.")
        elif result.status_code == 404:
            raise ErrorResponse("""\
[404 Error] The following error reasons are possible.
・The specified LIFF application does not exist.
・The specified LIFF application belongs to another channel.""")
