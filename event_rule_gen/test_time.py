import shedule_table as st
from shedule_event import datetime_to_cron, put_rule, attach_event_rule
import json


with open("./tst.json","r") as t:
    sd = json.loads(t.read())
    s = st.get_shedule(sd["shedule_table"])
    print(st.shedule(s))


# local testing

# from exam_shedule import generate_cloud_watch_rules
# generate_cloud_watch_rules(sd, handler='')
