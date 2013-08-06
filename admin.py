from google.appengine.ext import webapp

import fix_path
import config
import post_deploy
import handlers


post_deploy.run_deploy_task()


application = webapp.WSGIApplication([
  (config.url_prefix + '/admin/', handlers.AdminHandler),
  (config.url_prefix + '/admin/newpost', handlers.PostHandler),
  (config.url_prefix + '/admin/post/(\d+)', handlers.PostHandler),
  (config.url_prefix + '/admin/regenerate', handlers.RegenerateHandler),
  (config.url_prefix + '/admin/post/delete/(\d+)', handlers.DeleteHandler),
  (config.url_prefix + '/admin/post/preview/(\d+)', handlers.PreviewHandler),
])
