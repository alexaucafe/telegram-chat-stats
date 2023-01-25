from chat import Chat

def main():

    group = Chat()
    group_stats = group.get_group_stats()

    text = txt(group_stats)
    print(text)

    with open("result.txt", "w", encoding = "utf-8") as file:
        file.write(text)
        file.close()

def txt(group_stats, first_names = True):

    text_lines: list = []

    if first_names == True:
        longest_name_member = max(group_stats["members"], key = lambda member: len(member["first_name"]))
        longest_name_len = len(longest_name_member["first_name"])
    else:
        longest_name_member = max(group_stats["members"], key = lambda member: len(member["name"]))
        longest_name_len = len(longest_name_member["name"])

    spaces = " "*(longest_name_len + 2)
    text_lines.append("{}{}\n".format(spaces, group_stats["name"]))

    for member in group_stats["members"]:
        if first_names == True:
            name = member["first_name"]
        else:
            name = member["name"]
        messages_count = member["messages_count"]
        forwards_count = member["forwards_count"]
        replies_count = member["replies_count"]

        spaces = " "*(longest_name_len - len(name))
        text_lines.append(f"{name}:{spaces} {messages_count} messages ({replies_count} replies, {forwards_count} forwarded)")
    
    spaces = " "*(longest_name_len + 2)
    text_lines.append(f"\n{spaces}309:Дата-отдел")

    return "\n".join(text_lines)

main()