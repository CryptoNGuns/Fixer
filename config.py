import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ERpFAm6JOVMRjcXW6vd4'
