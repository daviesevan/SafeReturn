"""
This file holds helper functions for models to use
"""
import time
import random

def unique_ids():
    return int(time.time() * 100000) + random.randint(0, 999999)