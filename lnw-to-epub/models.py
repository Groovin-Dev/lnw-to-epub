class Update:
    def __init__(self, title, latest, last_update, rank):
        self.title = title
        self.latest = latest
        self.last_update = last_update
        self.rank = rank

    def get_info(self):
        return { 
            "title": self.title,
            "latest": self.latest,
            "updated_at": self.last_update,
            "rank": self.rank
        }


class Novel:
    def __init__(self, title, author, rank, rating, chapters, views, bookmarked, status, categories, last_update):
        self.title = title
        self.author= author
        self.rank = rank
        self.rating = rating
        self.chapters = chapters
        self.views = views
        self.bookmarked = bookmarked
        self.status = status
        self.categories = categories
        self.last_update = last_update

    def get_info(self):
        return {
            "title": self.title,
            "author": self.author,
            "rank": self.rank,
            "rating": self.rating,
            "chapters": self.chapters,
            "views": self.views,
            "bookmarked": self.bookmarked,
            "status": self.status,
            "categories": self.categories,
            "last_update": self.last_update
        }
