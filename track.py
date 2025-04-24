import uuid
import random
import string

def new_tracking_id( length=8 ):
    rand_str =''.join(random.choices(chars,  k=length))
    return rand_str


def unique_tracking_id(model , length=8):
    while True:
        tracking_id = new_tracking_id(length)
        if not model.objects.filter(tracking_id=tracking_id).exits():
            return tracking_id



