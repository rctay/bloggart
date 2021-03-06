import datetime
import logging
import os

from google.appengine.ext import deferred
from google.appengine.ext import webapp

import config
import markup
import models
import post_deploy
import utils

from django import forms


class ModelFormOptions(object):
  """A simple class to hold internal options for a ModelForm class.

  Instance attributes:
    model: a db.Model class, or None
    fields: list of field names to be defined, or None
    exclude: list of field names to be skipped, or None

  These instance attributes are copied from the 'Meta' class that is
  usually present in a ModelForm class, and all default to None.
  """

  def __init__(self, options=None):
    self.model = getattr(options, 'model', None)
    self.fields = getattr(options, 'fields', None)
    self.exclude = getattr(options, 'exclude', None)


class InitialDataForm(object):
  def __init__(self, instance=None, initial=None, *args, **kwargs):
    opts = ModelFormOptions(getattr(self, 'meta', None))
    object_data = {}
    if instance is not None:
      for name, prop in instance.properties().iteritems():
        if opts.fields and name not in opts.fields:
          continue
        if opts.exclude and name in opts.exclude:
          continue
        if hasattr(prop, 'get_value_for_form'):
          object_data[name] = prop.get_value_for_form(instance)
        else:
          object_data[name] = getattr(instance, name)
    if initial is not None:
      object_data.update(initial)

    kwargs['initial'] = object_data
    super(InitialDataForm, self).__init__(*args, **kwargs)


class PostForm(InitialDataForm, forms.Form):
  title = forms.CharField(widget=forms.TextInput(attrs={'id':'name'}))
  body = forms.CharField(widget=forms.Textarea(attrs={
      'id':'message',
      'rows': 10,
      'cols': 20}))
  body_markup = forms.ChoiceField(
    choices=[(k, v[0]) for k, v in markup.MARKUP_MAP.iteritems()])
  tags = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 20}))
  draft = forms.BooleanField(required=False)
  class Meta:
    model = models.BlogPost
    fields = [ 'title', 'body', 'tags' ]


def with_post(fun):
  def decorate(self, post_id=None):
    post = None
    if post_id:
      post = models.BlogPost.get_by_id(int(post_id))
      if not post:
        self.error(404)
        return
    fun(self, post)
  return decorate


class BaseHandler(webapp.RequestHandler):
  def render_to_response(self, template_name, template_vals=None, theme=None):
    if not template_vals:
      template_vals = {}
    template_vals.update({
        'path': self.request.path,
        'handler_class': self.__class__.__name__,
        'is_admin': True,
    })
    template_name = os.path.join("admin", template_name)
    self.response.out.write(utils.render_template(template_name, template_vals,
                                                  theme))


class AdminHandler(BaseHandler):
  def get(self):
    from generators import generator_list
    offset = int(self.request.get('start', 0))
    count = int(self.request.get('count', 20))
    posts = models.BlogPost.all().order('-published').fetch(count, offset)
    template_vals = {
        'offset': offset,
        'count': count,
        'last_post': offset + len(posts) - 1,
        'prev_offset': max(0, offset - count),
        'next_offset': offset + count,
        'posts': posts,
        'generators': [cls.__name__ for cls in generator_list],
    }
    self.render_to_response("index.html", template_vals)


class PostHandler(BaseHandler):
  def render_form(self, form):
    self.render_to_response("edit.html", {'form': form})

  @with_post
  def get(self, post):
    self.render_form(PostForm(
        instance=post,
        initial={
          'draft': post and not post.path,
          'body_markup': post and post.body_markup or config.default_markup,
        }))

  @with_post
  def post(self, post):
    form = PostForm(data=self.request.POST, instance=post,
                    initial={'draft': post and post.published is None})
    if form.is_valid():
      data = {
        'title': form.cleaned_data['title'],
        'body': form.cleaned_data['body'],
        'body_markup': form.cleaned_data['body_markup'],
      }
      if post is None:
        post = models.BlogPost(**data)
      else:
        for name, value in data.iteritems():
          setattr(post, name, value)

      post.tags = post.properties()['tags'] \
          .make_value_from_form(form.cleaned_data['tags'])

      if form.cleaned_data['draft']:# Draft post
        post.published = datetime.datetime.max
        post.put()
      else:
        if not post.path: # Publish post
          post.updated = post.published = datetime.datetime.now()
        else:# Edit post
          post.updated = datetime.datetime.now()
        post.publish(regenerate=True)
      self.render_to_response("published.html", {
          'post': post,
          'draft': form.cleaned_data['draft']})
    else:
      self.render_form(form)

class DeleteHandler(BaseHandler):
  @with_post
  def post(self, post):
    if post.path:# Published post
      post.remove()
    else:# Draft
      post.delete()
    self.render_to_response("deleted.html", None)


class PreviewHandler(BaseHandler):
  @with_post
  def get(self, post):
    # Temporary set a published date iff it's still
    # datetime.max. Django's date filter has a problem with
    # datetime.max and a "real" date looks better.
    if post.published == datetime.datetime.max:
      post.published = datetime.datetime.now()
    self.response.out.write(utils.render_template('post.html', {
        'post': post,
        'is_admin': True}))

class RegenerateHandler(BaseHandler):
  def post(self):
    generators = self.request.get_all("generators")

    deferred.defer(post_deploy.try_post_deploy, force=True, regenerate_kwargs={
      'classes': generators
    })
    self.render_to_response("regenerating.html")
