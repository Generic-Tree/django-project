import multiprocessing

from .env import env


bind = f"{env('HOST')}:{env('PORT')}"

workers = env('WORKERS') or multiprocessing.cpu_count() * 2
threads = env('THREADS') or 1

reload = env("RELOAD")

if env('DEBUG'):
    loginfo = 'debug'
