#!./venv/bin/python

import sys
import pprint

import db_table

col = sys.argv[1].split(",")
val = sys.argv[2].split(",")

searchParms = {}

for i in range(len(val)):
    searchParms[col[i]] = val[i]

# Init the db connections
session_table = db_table.db_table("sessions")
subsession_table = db_table.db_table("subsessions")
speaker_table = db_table.db_table("speakers")

# Find each session_id for the searched on column
results = []
if "speaker" in col:
    # If we are searching for the speaker, use the speaker table instead of session.
    speakers = speaker_table.select(None, searchParms)
    for i in range(len(speakers)):
        session = session_table.select(None, {"session_id": speakers[i]['session_id']})[0]
        results.append(session)
else:
    results = session_table.select(None, searchParms)


# For each session id, check to see if it has any subsessions
for i in range(len(results)):
    result = results[i]
    session_id = result['session_id']

    subsessions = subsession_table.select(None, {"parent_id": session_id})
    subsessions_list = []
    for row in subsessions:
        subsessions_list.append(row['child_id'])

    if len(subsessions_list) != 0:
        newResults = session_table.select(None, None, subsessions_list)

    print("Parent Session:")
    pprint.pprint (result)
    if len(subsessions_list) != 0:
        print("\nChild sessions")
        pprint.pprint(newResults)

    print("=========================================")




