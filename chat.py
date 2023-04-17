import json
from numpy import arange
from numpy import datetime64
from numpy import timedelta64

class Chat:

    def __init__(self, filename = "result.json") -> None:
        self.filename = filename
        self.group_data = self.get_group_data()
        self.group_messages = self.get_messages()
        self.group_members = self.get_members()

    def get_group_data(self):
        with open(self.filename, encoding="utf-8") as file:
            group_data = json.loads(file.read())
            file.close()
        return group_data

    def get_messages(self):

        group_messages = self.group_data["messages"]
        # group_messages = [message for message in group_messages if message["type"] == "message"]

        return group_messages

    def get_members(self):
        members = {}
        for message in self.group_messages:
            if message["type"] == "service":
                member_id = message["actor_id"]
                member_name = message["actor"]
            elif message["type"] == "message":
                member_id = message["from_id"]
                member_name = message["from"]
            else:
                continue

            if member_id not in members:
                members[member_id] = member_name
            elif members[member_id] != member_name:
                members[member_id] = member_name
            else:
                continue

        return members
    
    def get_first_name(self, member_id):
        member_name = self.group_members[member_id]
        if " " in member_name:
            first_name = member_name[:member_name.find(" ")]
        elif "-" in member_name:
            first_name = member_name[:member_name.find("-")]
        else:
            first_name = member_name
        return first_name

    def get_member_stats(self, member_id):

        member_messages = [message for message in self.group_messages if message.get("from_id", message.get("actor_id")) == member_id]
        messages_count = len(member_messages)
        forwards_count = len([message for message in member_messages if "forwarded_from" in message.keys()])
        replies_count = len([message for message in member_messages if "reply_to_message_id" in message.keys()])

        member_stats = {
            "name": self.group_members[member_id],
            "first_name": self.get_first_name(member_id),
            "user_id": member_id,
            "messages_count":messages_count,
            "forwards_count":forwards_count,
            "replies_count":replies_count,
        }

        return member_stats
    
    def get_days(self, active_days_count: int = 5):

        start_date = self.group_messages[0]["date"]
        end_date = self.group_messages[-1]["date"]
        dates = arange(datetime64(start_date, "D"),
                       datetime64(end_date, "D"),
                       timedelta64(1, "D"))

        days = {"name":self.group_data["name"],
                "active_days":[],
                "days":[]}

        for date in dates:
            date_messages = [m for m in self.group_messages if str(date) in m["date"]]
            days["days"].append({"date":date, "messages_count": len(date_messages)})

        active_days = sorted(days["days"],
                             key = lambda day: day["messages_count"],
                             reverse = True)
        days["active_days"] = active_days[:active_days_count]

        return days

    def get_group_stats(self, sort = True, reverse = False):

        group_stats = {
            "name": self.group_data["name"],
            "messages_count": len(self.group_messages),
            "members": []
        }

        for member_id in self.group_members:
            member_stats = self.get_member_stats(member_id)
            group_stats["members"].append(member_stats)
        
        if sort == True:
            group_members_sorted = sorted(group_stats["members"],
                                          key = lambda member: member["messages_count"],
                                          reverse = not reverse)
            group_stats["members"] = group_members_sorted
        
        group_stats["days"] = self.get_days() # Active days count may be specified
        
        return group_stats