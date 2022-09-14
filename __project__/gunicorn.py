import multiprocessing

from .env import env


bind = f"{env('HOST')}:{env('PORT')}"

workers = env('WORKERS') or 1
threads = env('THREADS') or 1

reload = env("RELOAD")

accesslog = '-'
if env('DEBUG'):
    loginfo = 'debug'
