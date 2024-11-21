from datetime import datetime

from dateutil import parser


class Event:

    def __init__(self, jobj:any):
        self.event_type:str = None
        self.author:str = None
        self.event_date:datetime = None
        self.label:str = None
        self.comment:str = None

        if jobj is not None:
            self.from_json(jobj)

    def from_json(self, jobj:any):
        self.event_type = jobj.get('event_type')
        self.author = jobj.get('author')
        try:
            self.event_date = parser.parse(jobj.get('event_date'))
        except: 
            pass
        self.label = jobj.get('label')
        self.comment = jobj.get('comment')