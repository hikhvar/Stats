# -*- coding: utf-8 -*-
import datetime
import time

NAMES = ["Mia", "Emma", "Hannah", "Sofia", "Anna", "Lea", "Ben", "Luca", "Paul", "Jonas", "Finn", "Luis"]
SURNAMES = ["Taake", "Tadlock", "Tappe", "Tappemeyer", "Tappendiek", "Tappmeyer", "Tarner", "Tarras", "Taeulker"]

import random
import itertools

def populate_model(model, seed=293286, user=15, entries=10000, deletes=100, days=100):
    """
        populate the model with 'user' users and 'entries' total entries.
        After creating these, 'deletes' many saetze are deleted individual.
        The results are spread over 'days' many different days.
    """
    start = time.time()
    random.seed(seed)
    users = random.sample(list(itertools.product(NAMES, SURNAMES)), user)
    dates = random.sample(list(itertools.product(range(2012, 2015), range(1,13),range(1,28))), days)
    dates = map(lambda x: datetime.datetime(x[0], x[1], x[2]), dates)
    for name, surname in users:
        model.add_schuetze(name, surname)
    for i in xrange(entries):
        ringe = 40 + random.random()*14.5
        schuetze = " ".join(users[random.randint(0, len(users)-1)])
        date = dates[random.randint(0, len(dates)-1)]
        model.add_satz(schuetze, ringe, date)
    dels = random.sample(model.get_all_satz_entries(), deletes)
    for satz in dels:
        model.delete_satz([satz.uuid])
    end = time.time()
    return end - start



