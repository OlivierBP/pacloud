#! /usr/bin/python

import datetime
import random

nb = random.randint(1, 1000)
timeToReach = datetime.datetime.now() + datetime.timedelta(minutes=10)

while timeToReach > datetime.datetime.now():
    print("Working on: " + str(nb))

print("Done")




