import os
import shutil
from jinja2 import Environment, FileSystemLoader
from .post import Post


TEMPLATES = 'templates'
STATIC = 'static'
SOURCE = 'posts'
ASSERT = 'assert'
DESTINATION = ''

EXT = ['markdown', 'mkdown', 'mkdn', 'mkd', 'md']
NOT_CLEARN = [TEMPLATES, STATIC, SOURCE, ASSERT, 'CNAME', '.git']


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
        else:
            with open(os.path.join(path, post.layout+'.html'),
                      'w', encoding='utf8') as f:
                f.write(html)


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
    site.pages = [page for page in posts if page.layout != 'post']

    env = Environment(loader=FileSystemLoader(template_path))
    env.globals['site'] = site

    write_posts(env, output_path, posts)


if __name__ == '__main__':
    main()
