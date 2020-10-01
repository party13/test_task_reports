import json
import operator
from datetime import datetime, timedelta, date
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Entity
from django.forms import Form
from .utils import *
from django.views.generic import View
from django.http import HttpResponse
from .forms import CreateEntityForm
# from django.core.exceptions import PermissionDenied


class HomePage(View):
    def get(self, request):
        if request.user.is_authenticated:
            # redirect to main view
            return redirect('my_entities')
        else:
            # render the greetings template
            template = 'greetings.html'
            return render(request, template, context={})


class MyEntities(View):
    def get(self, request):
        # nice list of entities to display must be here
        user = request.user
        if user.is_authenticated:
            template = 'entities_list.html'
            context = dict()

            entities = Entity.objects.filter(user_id=user.id)
            dt_from = request.GET.get('dt_from')
            dt_to = request.GET.get('dt_to')

            if dt_from and dt_to:
                try:
                    dt_from = datetime.strptime(dt_from, FMT)
                    dt_to = datetime.strptime(dt_to, FMT)
                    if dt_from <= dt_to:
                        dt1 = date(year=dt_from.year, month=dt_from.month, day=dt_from.day)
                        dt2 = date(year=dt_to.year, month = dt_to.month, day=dt_to.day)
                        entities = [e for e in entities if dt1 <= e.date <= dt2]
                        context['dt_from'] = dt_from.strftime('%d %b')
                        context['dt_to'] = dt_to.strftime('%d %b')
                except Exception as e:
                    print('not valid date, {}'.format(str(e)))
                    pass

            # sort by
            sort_attr = request.GET.get('sort', 'date')
            print(sort_attr)
            if sort_attr not in ['date', 'duration', 'distance', 'speed']:
                sort_attr = 'date'
            entities = sorted(entities, key=operator.attrgetter(sort_attr))

            context['sort_' + sort_attr] = True
            form = CreateEntityForm()
            context['user_name'] = user.username
            context['form'] = form
            context['count'] = len(entities)
            # context['entities'] = entities
            context['today'] = date.today().strftime(FMT)      # "%Y-%m-%d"
            context['page_number'] = int(request.GET.get('page', 1))
            context['per_page'] = int(request.GET.get('per_page', 10))
            context = prepare_pagination(context, items=entities)
            return render(request, template, context=context)
        else:
            # raise PermissionDenied
            return redirect('login_url')


class CreateEntity(View):
    def post(self, request):
        try:
            form = CreateEntityForm(request.POST)
            if form.is_valid():
                user_id = form.data.get('user_id')
                date = form.data.get('date')
                duration = form.data.get('duration')
                distance = form.data.get('distance')
                entity = Entity(user_id=user_id, date=date,distance=distance, duration=duration)
                entity.save()
                print(entity.id)
                return HttpResponse(json.dumps({'result': True, 'details': ''}))
            else:
                # render the form with errors
                return HttpResponse(json.dumps({'result': False, 'details': str(form.errors)}))
        except Exception as e:
            return HttpResponse(json.dumps({'result': False, 'details': str(e)}))


class MyStatistics(View):
    template = 'statistics.html'

    def get(self, request):
        # rendering statistics will be here
        user = request.user
        context = dict()
        if not user.is_authenticated:
            # raise PermissionDenied
            return redirect('login_url')

        entities = Entity.objects.filter(user_id=user.id)
        today = date.today()
        current_week = today.isocalendar()[1]
        weeks = list()
        for week_number in range(1, current_week):
            week_entities = [e for e in entities if e.week_number == week_number]
            if week_entities:
                count = len(week_entities)
                distance = sum([e.distance for e in week_entities])
                duration = sum([e.duration for e in week_entities])
                speed = distance / duration
            else:
                count = distance = duration = speed = 0
            week_start, week_end = week_ranges(week_number)
            weeks.append({'week_number': week_number,
                          'count': count,
                          'distance': distance,
                          'duration': duration,
                          'week_start': week_start,
                          'week_end': week_end,
                          'speed': round(speed, 3)})
            context['weeks'] = weeks
        return render(request, MyStatistics.template, context=context)

    def post(self, request):
        # apply filtering for statistics will be here
        return render(request, MyStatistics.template, context={})

def view_info(request):
    return render(request, 'task_info.html')

def delete_entity(request):
    if Form(request.POST).is_valid():
        user = request.user
        eid = request.POST.get('entity_id')
        entity = Entity.objects.get(id__iexact=eid)
        if entity and entity.user_id == user.id:
            entity.delete()
    return redirect('my_entities')


def greetings(request):
    template = 'greetings.html'
    # user = request.user
    return render(request, template)


def ajax_response(request):
    data = {'html': '<>render smth' , 'success': True}
    return HttpResponse(json.dumps(data), content_type='application/json')
