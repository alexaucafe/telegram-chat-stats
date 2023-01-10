import json

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
        group_messages = [message for message in group_messages if message["type"] == "message"]

        return group_messages

    def get_members(self):
        members = {}
        for message in self.group_messages:
            if message["type"] == "service": continue

            member_id = message["from_id"]
            member_name = message["from"]
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

        member_messages = [message for message in self.group_messages if message["from_id"] == member_id]
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

    def get_group_stats(self):

        group_stats = {
            "name": self.group_data["name"],
            "messages_count": len(self.group_messages),
            "members": []
        }

        for member_id in self.group_members:
            member_stats = self.get_member_stats(member_id)
            group_stats["members"].append(member_stats)
        
        return group_stats

def main():

    group = Chat()
    group_stats = group.get_group_stats()
    group_members_sorted = sorted(group_stats["members"], key = lambda member: member["messages_count"], reverse=True)

    longest_first_name = max(group_members_sorted, key = lambda member: len(member["first_name"]))
    longest_name_len = len(longest_first_name["first_name"])

    spaces = " "*(longest_name_len + 2)
    print("{}{}\n".format(spaces, group_stats["name"]))

    for member in group_members_sorted:
        first_name = member["first_name"]
        messages_count = member["messages_count"]
        forwards_count = member["forwards_count"]
        replies_count = member["replies_count"]

        spaces = " "*(longest_name_len - len(first_name))
        print(f"{first_name}:{spaces} {messages_count} messages ({replies_count} replies, {forwards_count} forwarded)")
    
    spaces = " "*(longest_name_len + 2)
    print(f"\n{spaces}309:Дата-отдел")

main()