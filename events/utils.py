
def event_key(event):
    try:
        return event['start']['dateTime']
    except KeyError:
        return event['start']['date']
