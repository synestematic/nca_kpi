# render shortcut handles template loading, context creation, template rendering and HttpResponse return 
from django.shortcuts import render 
from django.http import Http404
from django.http import HttpResponse
from django.utils import timezone
from kpi.models import Stats_ops, Stats_bc
from datetime import date, timedelta , time, datetime
import decimal
import MySQLdb, datetime

def calculate_last_thirty_days(selected_stats):
    thirty_days_objects = selected_stats.objects.using('portale_nca_kpi_mysql').order_by('-date').exclude( date__lt= date.today() - timedelta(days=31) ).filter()
    thirty_days_object = selected_stats()
    for day in thirty_days_objects:
        thirty_days_object.last_date = day.date
        thirty_days_object.incoming_calls += day.incoming_calls
        thirty_days_object.unanswered_calls += day.unanswered_calls
        thirty_days_object.abandoned_soon_calls += day.abandoned_soon_calls
        thirty_days_object.satisfied_calls += day.satisfied_calls
        thirty_days_object.answered_calls += day.answered_calls
        thirty_days_object.fast_calls += day.fast_calls
        thirty_days_object.total_connection_time += day.total_connection_time
        thirty_days_object.total_wait_time += day.total_wait_time

    try:
        thirty_days_object.average_connection_time = round( thirty_days_object.total_connection_time / thirty_days_object.answered_calls , 1)
        thirty_days_object.average_wait_time = round( thirty_days_object.total_wait_time / thirty_days_object.answered_calls , 1)
        thirty_days_object.answered_as_percentage = round((thirty_days_object.answered_calls / thirty_days_object.incoming_calls) * 100 , 1)
        thirty_days_object.fast_as_percentage = round((thirty_days_object.fast_calls / thirty_days_object.answered_calls) * 100, 1)
    except ZeroDivisionError:
        thirty_days_object.average_connection_time = 0.0
        thirty_days_object.average_wait_time = 0.0
        thirty_days_object.answered_as_percentage = 0.0
        thirty_days_object.fast_as_percentage = 0.0

    return thirty_days_object

def calculate_last_five_days(selected_stats):
    five_days_objects = selected_stats.objects.using('portale_nca_kpi_mysql').order_by('date').exclude(date__lt= date.today() - timedelta(days=6) ).filter()
    for day in five_days_objects:
        try:
            day.answered_as_percentage = round((day.answered_calls / day.incoming_calls) * 100 , 1)
            day.fast_as_percentage = round((day.fast_calls / day.answered_calls) * 100, 1)
        except ZeroDivisionError:
            day.answered_as_percentage = 0.0
            day.fast_as_percentage = 0.0            
    return five_days_objects

def calculate_day(selected_stats, day):
    try:
        day_object = selected_stats.objects.using('portale_nca_kpi_mysql').filter().get(date=day)
        day_object.answered_as_percentage = round((day_object.answered_calls / day_object.incoming_calls) * 100 , 1)
        day_object.fast_as_percentage = round((day_object.fast_calls / day_object.answered_calls) * 100, 1)
    except selected_stats.DoesNotExist:
        day_object = selected_stats()
        day_object.date = str(day)
        day_object.answered_as_percentage = 0.0
        day_object.fast_as_percentage = 0.0
        # raise Http404('Whatever Dude...')
    except ZeroDivisionError:
        day_object.answered_as_percentage = 0.0
        day_object.fast_as_percentage = 0.0
    return day_object

# views are functions that take http requests and return http responses
def aftersales(request):
    ops_thirty_days_object = calculate_last_thirty_days(Stats_ops)
    ops_five_days_objects = calculate_last_five_days(Stats_ops)
    ops_today_object = calculate_day(Stats_ops, date.today())
    return render(request, 'kpi/aftersales.html', {
        'title' : 'Aftersales',
        'ivr_avg_duration' : 15,
        'thirty_days': ops_thirty_days_object,
        'five_days': ops_five_days_objects,
        'day': ops_today_object,
        'fast_lower_th': 30.0,
        'fast_upper_th': 60.0,
        'ans_lower_th': 70.0,
        'ans_upper_th': 80.0,
    })

def bookingcenter(request):
    bc_thirty_days_object = calculate_last_thirty_days(Stats_bc)
    bc_five_days_objects = calculate_last_five_days(Stats_bc)
    bc_today_object = calculate_day(Stats_bc, date.today())
    return render(request, 'kpi/bookingcenter.html', {
        'title' : 'Booking Center',
        'ivr_avg_duration' : 80,
        'thirty_days': bc_thirty_days_object,
        'five_days': bc_five_days_objects,
        'day': bc_today_object,
        'fast_lower_th': 30.0,
        'fast_upper_th': 40.0,
        'ans_lower_th': 70.0,
        'ans_upper_th': 80.0,
    })

def day_detail(request, day):
    ops_day_object = calculate_day(Stats_ops, day)
    return render(request, 'kpi/day.html', {
    'title' : 'Aftersales',
    'ivr_avg_duration' : 15,
    'day': ops_day_object,
    'fast_lower_th': 30.0,
    'fast_upper_th': 60.0,
    'ans_lower_th': 70.0,
    'ans_upper_th': 80.0,
    })

def log_stats(request):
    date_string = str(datetime.date.today())
    day_stats = get_day_stats( date_string )
    try:
        if day_stats['incoming_calls_amount'] > 0:
            stats = Stats_ops()
            stats.date = date_string
            stats.department = 'ops'
            
            stats.incoming_calls = day_stats['incoming_calls_amount']
            stats.unanswered_calls = day_stats['unanswered_calls_amount']
            stats.answered_calls = day_stats['answered_calls_amount']
            stats.fast_calls = day_stats['fast_calls_amount']

            stats.total_connection_time = day_stats['total_connection_time']
            stats.total_wait_time = day_stats['total_wait_time']
            stats.average_connection_time = day_stats['average_connection_time']
            stats.average_wait_time = day_stats['average_wait_time']
            stats.ivr_average_duration = 15
            stats.abandoned_soon_calls = day_stats['abandoned_soon_calls_amount']
            stats.satisfied_calls = day_stats['satisfied_calls_amount']
            stats.save(using='portale_nca_kpi_mysql')
            print('Stats logged...')

        return HttpResponse( str(datetime.datetime.utcnow().replace(tzinfo=timezone.utc)) )
    except NameError as e:
        return HttpResponse('There was a NameError: {}'.format(e))
    except:
        raise Http404()


def get_day_stats(date_string):
    date_string = '\''+date_string+'\'' # '2017-03-01'

    import MySQLdb
    nca_db = MySQLdb.connect(host="10.4.4.205", user="django", db="nca")
    nca_cur = nca_db.cursor()

    nca_cur.execute(
        r"SELECT id FROM chiamate_as WHERE tipo_connessione LIKE '%inbound%' AND data_chiamata = " + date_string
    )
    incoming_calls_amount = nca_cur.rowcount
     
    ###############################################################
    # log unanswered_calls without taking into account people who abandon the queu too soon and peapole who leave after listening to extension2 information and hangup
    nca_cur.execute(
        r"SELECT id FROM chiamate_as WHERE tipo_connessione LIKE '%inbound%' AND data_chiamata = " + date_string + " AND tempo_connesso = 0 AND tempo_squillo < 15"
    )
    abandoned_soon_calls_amount = nca_cur.rowcount

    nca_cur.execute(
        r"SELECT id FROM chiamate_as WHERE tipo_connessione LIKE '%inbound%' AND data_chiamata = " + date_string + " AND tempo_connesso = 0 AND tempo_squillo >= 15 AND tempo_squillo < 30 AND estensione = 2"
    )
    satisfied_calls_amount = nca_cur.rowcount

    nca_cur.execute(
        r"SELECT id FROM chiamate_as WHERE tipo_connessione LIKE '%inbound%' AND data_chiamata = " + date_string + " AND tempo_connesso = 0"
    )
    # unanswered_calls_amount = nca_cur.rowcount
    unanswered_calls_amount = nca_cur.rowcount - ( satisfied_calls_amount + abandoned_soon_calls_amount )
    ################################################################

    nca_cur.execute(
        r"SELECT id FROM chiamate_as WHERE tipo_connessione LIKE '%inbound%' AND data_chiamata = " + date_string + " AND tempo_connesso > 0"
    )
    answered_calls_amount = nca_cur.rowcount

    nca_cur.execute(
        r"SELECT id FROM chiamate_as WHERE tipo_connessione LIKE '%inbound%' AND data_chiamata = " + date_string + " AND tempo_connesso > 0 AND tempo_squillo < 35"
    )
    fast_calls_amount = nca_cur.rowcount

    if answered_calls_amount > 0:
        ############# AVERAGE CONNECTED TIME #############
        nca_cur.execute(
            r"SELECT tempo_connesso FROM chiamate_as WHERE tipo_connessione LIKE '%inbound%' AND data_chiamata = " + date_string + " AND tempo_connesso > 0"
        )
        total_connection_time = sum( int( row[0] ) for row in nca_cur.fetchall() )

        average_connection_time = ( total_connection_time / answered_calls_amount )
        average_connection_time = round(average_connection_time,1)

        ############ AVERAGE WAIT TIME #############
        nca_cur.execute(
            r"SELECT tempo_squillo FROM chiamate_as WHERE tipo_connessione LIKE '%inbound%' AND data_chiamata = " + date_string + " AND tempo_connesso > 0"
        )
        total_wait_time = 0
        for row in nca_cur.fetchall():
            total_wait_time = total_wait_time + int(row[0])

        average_wait_time = ( total_wait_time / answered_calls_amount )
        average_wait_time = round(average_wait_time,1)

    elif answered_calls_amount == 0:
        average_connection_time = 0.0
        average_wait_time = 0.0
        total_connection_time = 0
        total_wait_time = 0

    return {
        'incoming_calls_amount': incoming_calls_amount,

        'unanswered_calls_amount': unanswered_calls_amount,
        'abandoned_soon_calls_amount': abandoned_soon_calls_amount,
        'satisfied_calls_amount': satisfied_calls_amount,

        'answered_calls_amount': answered_calls_amount,
        'fast_calls_amount': fast_calls_amount,

        'average_connection_time': average_connection_time,
        'average_wait_time': average_wait_time,
        'total_connection_time': total_connection_time,
        'total_wait_time': total_wait_time,

    }

