---
title: Introducing Lychee
---
`Lychee` is a new static blog generator, written in `Python3`.    

No more databases.     
Write your blog by `Markdown` formats that contains a `YAML` front matter block.    


## Quick-start guide    


        ~ $ pip install lychee
        ~ $ lychee new blog
        ~ $ cd blog
        ~/blog $ lychee serve
        => Now browse to http://localhost:4000


## Installation    
Your need to install [python3](https://www.python.org/).


## Directory structure    

        blog
        ├── posts
        │   ├── 2016-04-01-about.md
        │   ├── 2016-04-01-archive.md
        │   ├── 2016-04-01-index.md
        │   └── 2016-04-01-introducing-lychee.md
        ├── static
        │   ├── normalize.css
        │   └── style.css
        └── themes
            └── default
                ├── about.html
                ├── archive.html
                ├── base.html
                ├── index.html
                └── post.html


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
