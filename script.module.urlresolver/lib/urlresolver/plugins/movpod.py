"""
    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from lib import helpers
from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError


class MovpodResolver(UrlResolver):
    name = "movpod"
    domains = ["movpod.net", "movpod.in"]
    pattern = '(?://|\.)(movpod\.(?:net|in))/(?:embed-)?([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.FF_USER_AGENT}
        response = self.net.http_GET(web_url, headers=headers)
        html = response.content
        data = helpers.get_hidden(html)
        headers['Cookie'] = response.get_headers(as_dict=True).get('Set-Cookie', '')
        html = self.net.http_POST(response.get_url(), headers=headers, form_data=data).content
        sources = helpers.scrape_sources(html)
        return helpers.pick_source(sources) + helpers.append_headers(headers)

    def get_url(self, host, media_id):
        return 'http://movpod.in/embed-%s.html' % (media_id)
