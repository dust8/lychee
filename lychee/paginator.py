class Paginator:
    def __init__(self, per_page, posts, total_posts, total_pages, page, 
        previous_page, previous_page_path, next_page, next_page_path):
        self.per_page = per_page
        self.posts = posts
        self.total_posts = total_posts
        self.total_pages = total_pages
        self.page = page
        self.previous_page = previous_page
        self.previous_page_path = previous_page_path
        self.next_page = next_page
        self.next_page_path = next_page_path