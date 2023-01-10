import json

def get_messages():
    with open("result.json", encoding="utf-8") as file:

        group_data = json.loads(file.read())
        group_messages = group_data["messages"]
        group_messages = [message for message in group_messages if message["type"] == "message"]

        return group_messages

def get_members(group_messages):
    members = {}
    for message in group_messages:
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

def get_member_stats(member_id, group_messages):

    member_messages = [message for message in group_messages if message["from_id"] == member_id]
    messages_count = len(member_messages)
    forwards_count = len([message for message in member_messages if "forwarded_from" in message.keys()])
    stickers_count = len([message for message in member_messages if "sticker_emoji" in message.keys()])
    replies_count = len([message for message in member_messages if "reply_to_message_id" in message.keys()])
    photos_count = len([message for message in member_messages if "photo" in message.keys()])
    files_count = len([message for message in member_messages if "file" in message.keys()])

    stats = {
        "messages_count":messages_count,
        "forwards_count":forwards_count,
        "stickers_count":stickers_count,
        "replies_count":replies_count,
        "photos_count":photos_count,
        "files_count":files_count
    }

    return stats

def get_group_stats(group_members, group_messages):
    group_stats = {}
    for member_id in group_members:
        member_stats = get_member_stats(member_id, group_messages)
        group_stats[member_id] = member_stats
    
    return group_stats

def main():
    group_messages = get_messages()
    group_members = get_members(group_messages)

    for member in group_members:
        if " " in group_members[member]:
            group_members[member] = group_members[member][:group_members[member].find(" ")]
        elif "-" in group_members[member]:
            group_members[member] = group_members[member][:group_members[member].find("-")]

    group_stats = get_group_stats(group_members, group_messages)
    group_members_sorted = sorted(group_stats, key = lambda member_id: group_stats[member_id]["messages_count"], reverse=True)
    
    longest_name = max(group_members.values(), key = lambda member: len(member))

    for member_id in group_members_sorted:
        member_name = group_members[member_id]
        messages_count = group_stats[member_id]["messages_count"]
        forwards_count = group_stats[member_id]["forwards_count"]
        stickers_count = group_stats[member_id]["stickers_count"]
        replies_count = group_stats[member_id]["replies_count"]
        photos_count = group_stats[member_id]["photos_count"]
        files_count = group_stats[member_id]["files_count"]

        spaces = " "*(len(longest_name)-len(member_name))
        print(f"{member_name}:{spaces} {messages_count} messages ({replies_count} replies, {forwards_count} forwarded)")

main()