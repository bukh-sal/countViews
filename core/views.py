from django.shortcuts import render
from .models import Request, RequestSummary
from django.db import models
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth

from django.http import JsonResponse

import time
import datetime
import random
from datetime import timedelta

def index(request):
    start_time = time.time()
    context = {}

    Request.objects.create(
        method=request.method,
        datetime=datetime.datetime.now()
        )

    context['requests_count'] = Request.objects.all().count()

    context['time_taken'] = time.time() - start_time
    
    return render(request, 'core/index.html', context)


def create_random_request(request, number_of_requests):
    start_time = time.time()
    context = {}

    # start datetime 1 year ago
    start_date = datetime.datetime.now() - datetime.timedelta(days=365*5)
    # end datetime now
    end_date = datetime.datetime.now()

    for i in range(number_of_requests):
        # random datetime between start and end
        random_date = start_date + (end_date - start_date) * random.randint(0, 100) / 100
        # add timezone info
        random_date = random_date.replace(tzinfo=datetime.timezone.utc)
        # random method
        random_method = random.choice(['GET', 'POST', 'PUT', 'DELETE'])
        # create request
        Request.objects.create(method=random_method, datetime=random_date)

    context['requests_count'] = Request.objects.all().count()


    context['time_taken'] = time.time() - start_time


    return render(request, 'core/index.html', context)


def summary(request):
    start_time = time.time()
    context = {}

    # get the number of requests per month for the last 12 months (sqlite doesn't support date_trunc)
    #context['requests_per_month'] = Request.objects.raw('SELECT id, method, datetime, COUNT(*) AS requests_count, strftime("%Y-%m", datetime) AS month FROM core_request GROUP BY month ORDER BY month DESC LIMIT 12')

    # do the same but with django ORM
    #context['requests_per_month'] = Request.objects.annotate(month=TruncMonth('datetime')).values('month').annotate(requests_count=Count('id')).order_by('-month')[:12]
    
    #last_12_months = Request.objects.annotate(month=TruncMonth('datetime')).values('month').annotate(requests_count=Count('id')).order_by('-month')[:12]
    # use date instead of datetime
    last_12_months = Request.objects.annotate(month=TruncMonth('date')).values('month').annotate(requests_count=Count('id')).order_by('-month')

    context['requests_per_month'] = last_12_months
    #context['requests_per_month'] = (Request.objects.values('datetime__month').annotate(dcount=Count('id')))

    #context['requests_per_month'] = Request.objects.annotate(month=TruncMonth('datetime')).values('month').annotate(count=Count('id')).order_by('-month')[:12]

    # total number of requests per month
    #context['requests_per_month'] = Request.objects.annotate(month=TruncMonth('datetime')).values('month').annotate(count=Count('id')).order_by('month')

    time_taken = time.time() - start_time
    # convert time taken to six decimal places
    context['time_taken'] = "{:.6f}".format(time_taken)

    return render(request, 'core/summary.html', context)


def summary_json(request):
    data = {}
    #request_count = Request.objects.annotate(month=TruncMonth('date')).values('month').annotate(requests_count=Count('id')).order_by('-month')
    #data['requests_per_month'] = list(request_count)
    
    summary = cached_summary()
    data['requests_per_month'] = list(summary.values('date', 'count'))


    #data['requests_per_month'] = list(query_request_count())

    return JsonResponse(data)



def query_request_count():
    request_count = Request.objects.annotate(month=TruncMonth('date')).values('month').annotate(requests_count=Count('id')).order_by('-month')

    return request_count


def cached_summary():
    # get the count of Request objects, and compare it to the count of RequestSummary objects
    # if they are the same, return the RequestSummary objects
    # if they are different, delete all RequestSummary objects, and create new ones
    # then return the RequestSummary objects
    total_requests = Request.objects.all().count()

    # sum of 'count' field in RequestSummary
    total_count_of_summary = RequestSummary.objects.aggregate(Sum('count'))['count__sum']

    if total_requests == total_count_of_summary:
        return RequestSummary.objects.all()

    else:
        RequestSummary.objects.all().delete()

        request_count = Request.objects.annotate(month=TruncMonth('date')).values('month').annotate(requests_count=Count('id')).order_by('-month')

        for month in request_count:
            RequestSummary.objects.create(
                date = month['month'],
                count = month['requests_count']
            )

        return RequestSummary.objects.all()


def last_x(request, number_of_items):
    context = {}

    context['requests'] = Request.objects.all()[:number_of_items]

    return render(request, 'core/last_x.html', context)