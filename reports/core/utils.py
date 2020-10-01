import random
from datetime import date, timedelta
# from .models import Entity
from django.core.paginator import Paginator


FMT = '%Y-%m-%d'

def week_ranges(number):
    year = date.today().isocalendar()[0]
    dt0 = date(day=1, month=1, year=year)
    dt0 = dt0 - timedelta(days=dt0.isoweekday())
    return ((dt0 + timedelta(days=(number-1) * 7+1)).strftime(FMT), (dt0 + timedelta(days=number*7)).strftime(FMT))


def prepare_pagination(context, items):
    # items = context.get(items)
    per_page = context.get('per_page', 10)
    paginator = Paginator(items, per_page)
    page_number = context.get('page_number', 1)
    page = paginator.page(page_number)
    is_paginated = page.has_other_pages()
    prev_url = '?page={}&per_page={}'.format(page.previous_page_number(), per_page) if page.has_previous() else ''
    next_url = '?page={}&per_page={}'.format(page.next_page_number(), per_page) if page.has_next() else ''
    context['page_object'] = page
    context['is_paginated'] = is_paginated
    context['prev_url'] = prev_url
    context['next_url'] = next_url
    context['entities'] = paginator.get_page(page_number)
    context['paginator'] = paginator
    return context


def create_some_entities(cls):
    n = 50
    user_ids = [1, 2, 3, 4, 5]
    for i in range(n):
        uid = random.choice(user_ids)
        dt = date(day=random.randint(1,28), month=random.randint(1,12), year=2020)
        entity = cls(user_id=uid,
                        date=dt,
                        duration=random.randint(5, 45),
                        distance=random.randint(100, 350))
        entity.save()
        print('saved new: ', entity.id)


if __name__=='__main__':
    create_some_entities()