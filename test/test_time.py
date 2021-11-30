import sys
import json
sys.path.append("../")

from event_rule_gen.scale_shedule import generate_rules


with open("./test.json", "r") as t:
    e = json.loads(t.read())


def multi_sevice_shedule_rule(event, handler):
    for every in event:
        # local testing
        generate_rules(every)


multi_sevice_shedule_rule(e, "")
