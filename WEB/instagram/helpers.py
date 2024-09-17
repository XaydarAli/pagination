from django.db import models


class Pagination():
    @staticmethod
    def page_pagination(queryset: list, page_size: int, page: int):
        """
        queryset: data
        page_size: har bitta sahifada nechtadanligi
        page: sahifa tartibi
        """
        return queryset[page_size * (page - 1):page_size * page]
