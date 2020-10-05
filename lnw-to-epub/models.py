from dataclasses import dataclass

@dataclass
class Update:
    title: str
    latest: str
    last_update: str
    rank: str

@dataclass
class Novel:
    title: str
    author: str
    rank: str
    rating: str
    chapters: str
    views: str
    bookmarked: str
    status: str
    categories: str
    last_update: str

@dataclass
class Chapter:
    title: str
    link: str
    number: str
    text: str