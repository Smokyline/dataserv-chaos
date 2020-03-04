from django.shortcuts import render_to_response
from chaos import settings
from core import SWARM
import datetime
import os


def render_chaos(request):
    def decode_dt_param(str_dt):
        date, time = str_dt.split('T')
        dt = datetime.datetime.strptime(
            '%s %s' %
            (date, time), '%Y-%m-%d %H:%M:%S')
        return dt

    original_umask = os.umask(0)
    param_name = [
        'swchar',
        'mod',
        'timeFrom',
        'timeTo',
        'delta',
        ]
    param_dict = {}
    for p in param_name:
        param_dict[p] = request.GET[p]
    dt_from, dt_to = decode_dt_param(
        param_dict['timeFrom']), decode_dt_param(
        param_dict['timeTo'])

    swarm = SWARM(char=param_dict['swchar'], dt_from=dt_from, dt_to=dt_to, delta=int(param_dict['delta']))

    print('data prepared...')
    led = swarm.plot_map()
    os.umask(original_umask)

    return render_to_response('image_view.html', {'MEDIA_URL': settings.STATIC_URL, 'IMAGE_NAME': led})


def chaos_form(request):
    return render_to_response('dataserv-chaos-ru.html')
