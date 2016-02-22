#!/usr/bin/env python
# coding:utf-8

import os
import sys
import tornado.web
import tornado.ioloop
import tornado.websocket
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

BASE_DIR = os.path.dirname(__file__)


class TemplateRendring(object):
    '''
    A simple class to hold methods for rendering templates.
    '''
    def render_template(self, template_name, **kwargs):
        template_dirs = []
        if self.settings.get('template_path', ''):
            template_dirs.append(self.settings['template_path'])
        env = Environment(loader=FileSystemLoader(template_dirs))

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content


class BaseHandler(tornado.web.RequestHandler, TemplateRendring):
    '''
    Tornado RequestHandler subclass.
    '''
    def initialize(self):
        pass

    def get_current_user(self):
        pass
        #user = self.get_secure_cookie('user')
        #return user if user else None

    def render(self, template_name, **kwargs):
        kwargs.update({
            'settings': self.settings,
            'STATIC_URL': self.settings.get('static_url_prefix', '/static/'),
            'request': self.request,
            'current_user': self.current_user,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
        })
        content = self.render_template(template_name, **kwargs)
        self.write(content)


class Main(BaseHandler):

    def get(self):
        self.render('chat.html')


class Signup(BaseHandler):

    def get(self):
        self.render('signup.html')


class Signin(BaseHandler):

    def get(self):
        self.render('signin.html')


class ChatRoom(tornado.websocket.WebSocketHandler):

    stores = set()

    def open(self):
        print('WebSocket opened', self.request.remote_ip, id(self))
        self.stores.add(self)

    def on_message(self, message):
        for obj in self.stores:
            if obj == self:
                obj.write_message('You said:' + message)
            else:
                obj.write_message('He said:' + message)

    def on_close(self):
        print('WebSocket closed')

settings = {'debug': True,
            'template_path': os.path.join(BASE_DIR, 'templates'),
            'static_path': os.path.join(BASE_DIR, 'static')}

application = tornado.web.Application([
    (r'/', Main),
    (r'/chat', ChatRoom),
    (r'/signup', Signup)
], **settings)

if __name__ == '__main__':
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
