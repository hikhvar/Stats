#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
HUMAN_READABLE_FORMAT = "%d.%m.%Y"

def to_timestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6 


def to_human_readable(date):
    date = datetime.fromtimestamp(date)
    return date.strftime(HUMAN_READABLE_FORMAT)

def from_human_readable(datestring):
    """ 
        return the timestamp from human readable string.
    """
    date = datetime.strptime(datestring, HUMAN_READABLE_FORMAT)
    return to_timestamp(date)