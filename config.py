# Name of the blog
blog_name = 'My Blog'

# Your name (used for copyright info)
author_name = 'the author'

# (Optional) slogan
slogan = 'This is my blog'

# Selects the theme to use. Theme names correspond to directories under
# the 'themes' directory, containing templates and static content.
theme = 'default'

# Defines the URL organization to use for blog postings. Valid substitutions:
#   slug - the identifier for the post, derived from the title
#   year - the year the post was published in
#   month - the month the post was published in
#   day - the day the post was published in
post_path_format = '/%(year)d/%(month)02d/%(slug)s'

# A nested list of sidebar menus, for convenience. If this isn't versatile
# enough, you can edit themes/default/base.html instead.
sidebars = [
  ('Blogroll', [
    '<a href="http://blog.notdot.net/">Nick Johnsonz</a>',
    '<a href="http://www.billkatz.com/">Bill Katz</a>',
    '<a href="http://www.codinghorror.com/blog/">Coding Horror</a>',
    '<a href="http://craphound.com/">Craphound</a>',
    '<a href="http://www.neopythonic.blogspot.com/">Neopythonic</a>',
    '<a href="http://www.schneier.com/blog/">Schneier on Security</a>',
  ]),
]
