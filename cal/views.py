import json
from datetime import datetime, timedelta, date

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from .forms import EventForm


def index(request):
    return HttpResponse('hello')


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        if is_overlapping(form.instance.room_number, form.instance.start_time, form.instance.end_time):
            # There is a overlap. Show an error.
            messages.error(request, 'Conflicting timing. Please select another time.')
            return render(request, 'cal/event.html', {'form': form})
        else:
            form.save()
            return HttpResponseRedirect(reverse('cal:data_is_here'))
    return render(request, 'cal/event.html', {'form': form})


def event_del(request, event_id):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
        instance.delete()
    return HttpResponseRedirect(reverse('cal:data_is_here'))


def is_overlapping(room_number, start_time, end_time):  # start_time 1 PM, End-time = 2PM
    events = Event.objects.filter(room_number=room_number)  # Get all the registered events.
    for event in events:
        print('event_room_number', event.room_number)
        print('event_start_time', event.start_time)
        print('event_end_time', event.end_time)
        # Loop through registered events to find out overlap.
        if event.start_time >= end_time:
            # If current event starts after user requested start time, then there is no overlap.
            print('First valid', str(event))
            continue
        elif event.end_time <= start_time:
            # If current event ends before user requested time, then there is no overlap.
            print('second valid', str(event))
            continue
        else:
            # There is a possibility for overlapping.
            print('Overlapping Event=', str(event))
            return True
    return False


def data_is_here(request):
    data = Event.objects.all()
    events = []
    for e in data:
        events.append({
            'id': e.my_id,
            'title': e.title,
            'start': e.start_time.strftime('%Y-%m-%dT%H:%M'),
            'end': e.end_time.strftime('%Y-%m-%dT%H:%M')
        })
    return render(request, 'cal/calendar.html', {'data': events})
