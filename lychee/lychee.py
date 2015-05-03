import os
import argparse
import shutil
import sys
from math import ceil
from jinja2 import Environment, FileSystemLoader
from pkg_resources import resource_string

from .post import Post
from .paginator import Paginator


templates_page = resource_string(__name__, 'data/templates/page.html')
templates_base = resource_string(__name__, 'data/templates/base.html')
templates_index = resource_string(__name__, 'data/templates/index.html')
templates_post = resource_string(__name__, 'data/templates/post.html')
templates_about = resource_string(__name__, 'data/templates/about.html')
static_blog = resource_string(__name__, 'data/static/blog.css')
posts_about = resource_string(__name__, 'data/posts/2015-05-01-about.md')
posts_index = resource_string(__name__, 'data/posts/2015-05-01-index.md')
posts_introducing = resource_string(__name__, 'data/posts/2015-05-01-introducing-lychee.md')

TEMPLATES = 'templates'
STATIC = 'static'
SOURCE = 'posts'
ASSERT = 'assert'
DESTINATION = ''

EXT = ['markdown', 'mkdown', 'mkdn', 'mkd', 'md']
NOT_CLEARN = [TEMPLATES, STATIC, SOURCE, ASSERT, 'CNAME']


class Site:
    def __init__(self):
        self.posts = []
        self.pages = []


def get_posts(path):
    posts = []
    filenames = os.listdir(path)
    filenames.sort(reverse=True)
    for filename in filenames:
        if os.path.isfile(os.path.join(path, filename)):
            if os.path.splitext(filename)[1][1:] in EXT:
                post = Post()
                post.from_path(os.path.join(path, filename))
                posts.append(post)
    return posts


def write_posts(env, output_path, posts):
    for post in posts:
        template = env.get_template(post.layout+'.html')
        html = template.render(post=post)
        path = output_path
        if post.layout == 'post':
            for fold in post.date.split('-'):
                path = path + os.sep + fold
                if not os.path.exists(path):
                    os.mkdir(path)

        with open(os.path.join(path, post.alias + '.html'),
                  'w', encoding='utf8') as f:
            f.write(html)


def write_pages(env, output_path, pages):
    output_path = os.path.join(output_path, 'page')
    if not os.path.exists(output_path):
            os.mkdir(output_path)
    for page in pages:
        template = env.get_template('page.html')
        html = template.render(page=page)

        path = output_path + os.sep + str(page.page)
        if not os.path.exists(path):
            os.mkdir(path)

        with open(os.path.join(path, 'index.html'),
                  'w', encoding='utf8') as f:
            f.write(html)
    

def generate_structure(path):
    template_path = os.path.join(path, TEMPLATES)
    static_path = os.path.join(path, STATIC)
    posts_path = os.path.join(path, SOURCE)
    output_path = os.path.join(path, DESTINATION)

    if not os.path.exists(template_path):
        os.mkdir(template_path)
        generate_templates(template_path)
    if not os.path.exists(static_path):
        os.mkdir(static_path)
        generate_static(static_path)
    if not os.path.exists(posts_path):
        os.mkdir(posts_path)
        generate_posts(posts_path)


def generate_templates(path):
    with open(os.path.join(path, 'page.html'), 'wb') as fh:
        fh.write(templates_page)
    with open(os.path.join(path, 'base.html'), 'wb') as fh:
        fh.write(templates_base)
    with open(os.path.join(path, 'index.html'), 'wb') as fh:
        fh.write(templates_index)
    with open(os.path.join(path, 'post.html'), 'wb') as fh:
        fh.write(templates_post)
    with open(os.path.join(path, 'about.html'), 'wb') as fh:
        fh.write(templates_about)

def generate_static(path):
    with open(os.path.join(path, 'blog.css'), 'wb') as fh:
        fh.write(static_blog)


def generate_posts(path):
    with open(os.path.join(path, '2015-05-01-about.md'), 'wb') as fh:
        fh.write(posts_about)
    with open(os.path.join(path, '2015-05-01-index.md'), 'wb') as fh:
        fh.write(posts_index)
    with open(os.path.join(path, '2015-05-01-introducing-lychee.md'), 'wb') as fh:
        fh.write(posts_introducing)


def clearn_build(path):
    for name in os.listdir(path):
        if not name in NOT_CLEARN:
            if os.path.isfile(os.path.join(path, name)):
                os.remove(os.path.join(path, name))
            else:
                shutil.rmtree(os.path.join(path, name))
    

def build(path):
    template_path = os.path.join(path, TEMPLATES)
    static_path = os.path.join(path, STATIC)
    posts_path = os.path.join(path, SOURCE)
    output_path = os.path.join(path, DESTINATION)

    clearn_build(path)
   
    posts = get_posts(posts_path)

    site = Site()
    site.posts = [post for post in posts if post.layout == 'post']
    
    per_page = 10
    total_posts = len(site.posts)
    total_pages = ceil(total_posts / per_page)
    page_num = 1
    for i in range(0, total_posts, per_page):
        end = i+per_page
        if end >= total_posts:
            end = total_posts

        previous_page = page_num-1
        if previous_page < 1:
            previous_page = None

        next_page = page_num + 1
        if next_page > total_pages:
            next_page = None

        page = Paginator(per_page, site.posts[i:end], total_posts, total_pages,
            page_num, previous_page, '/page/'+str(page_num-1), 
            next_page, '/page/'+str(page_num+1))
        page_num += 1
        site.pages.append(page)


    env = Environment(loader=FileSystemLoader(template_path))
    env.globals['site'] = site

    write_posts(env, output_path, posts)
    write_pages(env, output_path, site.pages)

if __name__ == '__main__':
    main()
