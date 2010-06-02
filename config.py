debug = True
should_defer = not debug

# Name of the blog
blog_name = "rctay's blog"

# Your name (used for copyright info)
author_name = 'Tay Ray Chuan'

# (Optional) slogan
slogan = '&lt;a oh-so-witty line goes here&gt;'

# The hostname this site will primarially serve off (used for Atom feeds)
host = 'localhost:8080'

# Selects the theme to use. Theme names correspond to directories under
# the 'themes' directory, containing templates and static content.
theme = 'coolblue'

# Defines the URL organization to use for blog postings. Valid substitutions:
#   slug - the identifier for the post, derived from the title
#   year - the year the post was published in
#   month - the month the post was published in
#   day - the day the post was published in
post_path_format = '/%(year)d/%(month)02d/%(slug)s'

# A nested list of sidebar menus, for convenience. If this isn't versatile
# enough, you can edit themes/default/base.html instead.
sidebars = [
]

# Number of entries per page in indexes.
posts_per_page = 10

# The mime type to serve HTML files as.
html_mime_type = "text/html; charset=utf-8"

# To use disqus for comments, set this to the 'short name' of the disqus forum
# created for the purpose.
disqus_forum = None

# Length (in words) of summaries, by default
summary_length = 50

# If you want to use Google Analytics, enter your 'web property id' here
analytics_id = None

# If you want to use PubSubHubbub, supply the hub URL to use here.
# Note that Feedburner supports PubSubHubbub via Pingshot, so you can disable
# this and just use Feedburner.
hubbub_hub_url = None

# If you want to ping Google Sitemap when your sitemap is generated change this to True, else False
# see: http://www.google.com/support/webmasters/bin/answer.py?hl=en&answer=34609 for more information
google_sitemap_ping = False

# If you want to use Google Site verification, go to
# https://www.google.com/webmasters/tools/ , add your site, choose the 'upload
# an html file' method, then set the NAME of the file below.
# Note that you do not need to download the file provided - just enter its name
# here.
google_site_verification = None

# The part that goes after http://feeds.feedburner.com/.
feedburner_name = None

# Default markup language for entry bodies (defaults to html).
default_markup = 'markdown'

# Syntax highlighting style for RestructuredText and Markdown,
# one of 'manni', 'perldoc', 'borland', 'colorful', 'default', 'murphy',
# 'vs', 'trac', 'tango', 'fruity', 'autumn', 'bw', 'emacs', 'pastie',
# 'friendly', 'native'.
highlighting_style = 'friendly'

# Absolute url of the blog application use '/blog' for host/blog/
# and '' for host/.Also remember to change app.yaml accordingly
url_prefix = ''

# Defines where the user is defined in the rel="me" of your pages.
# This allows you to expand on your social graph.
rel_me = None

# The dotted module name of a concrete implementation of tzinfo.
tzinfo_class = None
