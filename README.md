# Introducing Lychee

`Lychee` is a new static blog generator, written in `Python3`.    

No more databases.     
Write your blog by `Markdown` formats that contains a `YAML` front matter block.    


## Quick-start guide    


        ~ $ pip install lychee
        ~ $ lychee -new my-blog
        ~ $ lychee -build my-blog
        ~ $ lychee -serve my-blog
        => Now browse to http://localhost:4000

   
## Installation    
Your need to install [python3](https://www.python.org/).


## Directory structure    

        my-blog
        ├── templates
        |   ├── base.html
        |   ├── index.html
        |   ├── about.html
        |   ├── page.html
        |   └── post.html
        ├── posts
        |   ├── 2015-05-01-about.md
        |   └── 2015-05-02-intrudcing-lychee.md
        ├── static
        |   └── blog.css
        └── assert    


## Front Matter
MarkDown file that contains a YAML front matter block.    

        ---
        title: Blogging Like a Hacker
        ---
or    

        ---
        layout: about
        title: Blogging Like a Hacker
        ---

if your file not contain layout, the default layout is post.   