import os
import argparse
import shutil
import sys
from math import ceil
from jinja2 import Environment, FileSystemLoader
from .post import Post
from .paginator import Paginator


EXT = ['markdown', 'mkdown', 'mkdn', 'mkd', 'md']


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
    

def clearn_build(path):
    if os.path.exists(os.path.join(path, 'index.html')):
        os.remove(os.path.join(path, 'index.html'))
    if os.path.exists(os.path.join(path, '_site')):
        shutil.rmtree(os.path.join(path, '_site'))

    os.mkdir(os.path.join(path, '_site'))

def copy_static(static_path, path):
    if os.path.exists(static_path):
        shutil.copytree(static_path, os.path.join(path,'_site/static'))  

def copy_assert(assert_path, path):
    if os.path.exists(assert_path):
        shutil.copytree(assert_path, os.path.join(path,'_site/assert'))  

def build(path):
    template_path = os.path.join(path, '_templates')
    static_path = os.path.join(path, '_static')
    assert_path = os.path.join(path, '_assert')
    posts_path = os.path.join(path, '_posts')
    output_path = os.path.join(path, '_site')

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
    
    copy_static(static_path, path)
    copy_assert(assert_path, path)

if __name__ == '__main__':
    main()
