from typing import List

class Header:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class HeaderCategories:
    def __init__(self, header: Header, categories: List):
        self.id = header.id
        self.name = header.name
        self.categories = categories