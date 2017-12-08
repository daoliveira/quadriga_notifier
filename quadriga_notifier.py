from quadriga import QuadrigaClient
from db import Data
import re

data = Data()


def add_notification(command):
    # removing 'notify' and striping spaces
    # 'notify ltc_cad <= 90' becomes 'ltc_cad<=90'
    command = "".join(command[6:].split())
    # preparing regex to extract comparator
    comp_regex = re.compile("(<=|>=|==|<>|!=|<|>)")
    comp_match = comp_regex.search(command)
    if not comp_match:
        print("Use one of the valid comparators: <|>|<=|>=|==|<>|!=")
        return
    comp = comp_match.group()

    tokens = command.split(comp)
    book = tokens[0]
    if book not in QuadrigaClient.order_books:
        print("Use one of the valid order books: " + "|".join(QuadrigaClient.order_books))
        return

    try:
        value = float(tokens[1])
    except ValueError:
        print("Use a real value")
        return

    data.insert(book=book, comp=comp, value=value)


def list_notifications():
    notifications = data.select_untriggered()
    if not len(notifications):
        print("No pending notifications")
        return
    print("ID     Trigger            Created")
    print("==     =======            =======")
    for n in notifications:
        print("%s      %s %s %s      %s" % (n[0], n[1], n[2], n[3], n[4]))


def remove_notification(command):
    tokens = command.split(" ")
    try:
        id = int(tokens[1])
    except ValueError:
        print("Use 'remove [id]'. Example: > remove 1")

    data.delete(id)


def help(command):
    default_msg = "Type 'help [notify|list|remove|start|stop|status|help|quit|exit]'"
    tokens = command.split()

    # only 'help' entered
    if len(tokens) == 1:
        print(default_msg)
        return

    # 'help something' entered
    if tokens[1] == "notify":
        print("Creates a notification.")
        print("Usage: > notify [%s] [<|>|<=|>=|==|<>|!=] [value]" % ("|".join(QuadrigaClient.order_books)))
        print("Example: > notify btc_cad <= 8540.25")
    elif tokens[1] == "list":
        print("Lists pending notifications. Usage: > list")
    elif tokens[1] == "remove":
        print("Removes pending notification. Usage: > remove [id]")
        print("Example: > remove 5")
    elif tokens[1] == "quit" or tokens[1] == "exit":
        print("Exits QuadrigaCX Notifications and stops notification service")
    else:
        print(default_msg)


def main():
    print("QuadrigaCX Notifications. Type 'help' to learn about available commands.")
    while True:
        command = input("> ").strip()
        if command == "quit" or command == "exit":
            break
        elif command[:6] == "notify":
            add_notification(command)
        elif command == "list":
            list_notifications()
        elif command[:6] == "remove":
            remove_notification(command)
        elif command[:4] == "help":
            help(command)
        else:
            print("Available commands: help|notify|list|remove|quit|exit")


if __name__ == '__main__':
    main()
