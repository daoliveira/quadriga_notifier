from quadriga import QuadrigaClient
from db import Data
import re
import notification_worker

data = Data()


def start():
    notification_worker.start()
    print("Notification service enabled")


def stop():
    notification_worker.stop()
    print("Notification service disabled")


def status():
    if notification_worker.active:
        with open("notification_worker") as file:
            last_run = file.readline()
            print(f"Notification service enabled. Last run: {last_run}")
    else:
        print("Notification service disabled")


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
    for notification in notifications:
        print("%s      %s %s %s      %s" % notification[:5])


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
        print(f"Usage: > notify [{'|'.join(QuadrigaClient.order_books)}] [<|>|<=|>=|==|<>|!=] [value]")
        print("Example: > notify btc_cad <= 8540.25")
    elif tokens[1] == "list":
        print("Lists pending notifications. Usage: > list")
    elif tokens[1] == "remove":
        print("Removes pending notification. Usage: > remove [id]")
        print("Example: > remove 5")
    elif tokens[1] == "start":
        print("Starts notification service. Usage: > start")
    elif tokens[1] == "stop":
        print("Stops notification service. Usage: > stop")
    elif tokens[1] == "status":
        print("Show notification service status. Usage: > status")
    elif tokens[1] == "quit" or tokens[1] == "exit":
        print("Exits QuadrigaCX Notifications and stops notification service")
    else:
        print(default_msg)


def main():
    print("QuadrigaCX Notifications. Type 'help' to learn about available commands.")
    print("Type 'start' to start notification service. ")
    while True:
        command = input("> ").strip()
        if command == "quit" or command == "exit":
            break
        elif command == "start":
            start()
        elif command == "stop":
            stop()
        elif command == "status":
            status()
        elif command[:6] == "notify":
            add_notification(command)
        elif command == "list":
            list_notifications()
        elif command[:6] == "remove":
            remove_notification(command)
        elif command[:4] == "help":
            help(command)
        else:
            print("Available commands: help|notify|list|remove|start|stop|status|quit|exit")


if __name__ == '__main__':
    main()
