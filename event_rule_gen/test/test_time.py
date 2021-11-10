import sys

sys.path.append("../")

import shedule_table as st
from shedule_event import datetime_to_cron, put_rule, attach_event_rule
import json
from scale_shedule import generate_rules


with open("./test.json", "r") as t:
    e = json.loads(t.read())


def multi_sevice_shedule_rule(event, handler):
    for every in event:
        # local testing
        generate_rules(every)


multi_sevice_shedule_rule(e, "")
