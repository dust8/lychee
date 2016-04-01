import os
from yaml import load
from markdown import markdown


class Post:

    def __init__(self):
        self.title = ''
        self.date = ''
        self.layout = 'post'
        self.content = ''
        self.permalink = ''
        self.link = ''

    def from_path(self, path):
        try:
            basename = os.path.split(path)[1]
            root, ext = os.path.splitext(basename)
            self.slug = root[11:]
            self.date = root[:10]
            self.url = '/' + '/'.join(self.date.split('-')) + \
                '/' + self.slug + '.html'

            with open(path, 'r', encoding='utf8') as fh:
                data = fh.read()
                start = data.find('---')
                if start != 0:
                    raise Exception('''The front matter must be the first thing in the file
                        and must take the form of valid YAML set between triple-dashed lines''')

                end = data.find('---', start + 3)
                if end == -1:
                    raise Exception('''The front matter must be the first thing in the file
                        and must take the form of valid YAML set between triple-dashed lines''')

                tfm = load(data[start + 3:end])

                self.__dict__.update(tfm)
                self.content = markdown(data[end + 3:])
        except:
            print('post from_path error:{}'.format(path))
