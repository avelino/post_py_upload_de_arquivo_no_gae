#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import blobstore_handlers

class DatastoreFile(db.Model):
    data = db.BlobProperty(required=True)
    mimetype = db.StringProperty(required=True)


class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render("upload.html", {}))

    def post(self):
        file = self.request.POST['file']
        
        entity = DatastoreFile(data=file.value, mimetype=file.type)
        entity.put()

        file_url = "http://%s/%d/%s" % (self.request.host, entity.key().id(), file.name)
        self.response.out.write("Your uploaded file is now available at %s" % (file_url,))


class DownloadHandler(webapp.RequestHandler):
    def get(self, id, filename):
        entity = DatastoreFile.get_by_id(int(id))
        self.response.headers['Content-Type'] = entity.mimetype
        self.response.out.write(entity.data)


def main():
    application = webapp.WSGIApplication([('/', MainHandler),('/(\d+)/(.*)', DownloadHandler),],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
