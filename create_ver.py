import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import fix_path
import models
from post_deploy import BLOGGART_VERSION


class PostDeployHandler(webapp.RequestHandler):
    def get(self):
        new_version = models.VersionInfo(
            key_name=os.environ['CURRENT_VERSION_ID'],
            bloggart_major = BLOGGART_VERSION[0],
            bloggart_minor = BLOGGART_VERSION[1],
            bloggart_rev = BLOGGART_VERSION[2])
        new_version.put()


application = webapp.WSGIApplication([
  ('/_ah/create_ver', PostDeployHandler),
])


def main():
  fix_path.fix_sys_path()
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
