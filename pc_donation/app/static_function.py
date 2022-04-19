import flask


class PageSet:
    def __init__(self,  page, per_page, last_item):
        self.item_start = int(page * per_page - per_page)
        self.item_end = int(page * per_page)
        self.last_page = int(last_item / per_page) + (last_item % per_page > 0)
        page_list_start = page - 5
        page_list = []
        for i in range(0, 11):
            page_list.append(page_list_start)
            if page_list_start < 1:
                page_list.remove(page_list_start)
            if page_list_start > self.last_page:
                page_list.remove(page_list_start)
            page_list_start += 1
        self.page_list = page_list




    
        