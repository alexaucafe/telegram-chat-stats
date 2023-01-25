from chat import Chat

def main():

    group = Chat()
    group_stats = group.get_group_stats()

    print(txt(group_stats))

def txt(group_stats, first_names = True):

    text_lines: list = []

    longest_first_name = max(group_stats["members"], key = lambda member: len(member["first_name"]))
    longest_name_len = len(longest_first_name["first_name"])

    spaces = " "*(longest_name_len + 2)
    text_lines.append("{}{}\n".format(spaces, group_stats["name"]))

    for member in group_stats["members"]:
        first_name = member["first_name"]
        messages_count = member["messages_count"]
        forwards_count = member["forwards_count"]
        replies_count = member["replies_count"]

        spaces = " "*(longest_name_len - len(first_name))
        text_lines.append(f"{first_name}:{spaces} {messages_count} messages ({replies_count} replies, {forwards_count} forwarded)")
    
    spaces = " "*(longest_name_len + 2)
    text_lines.append(f"\n{spaces}309:Дата-отдел")

    return "\n".join(text_lines)

main()