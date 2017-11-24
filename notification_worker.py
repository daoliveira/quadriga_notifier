import threading
import time
from datetime import datetime
from config import config
from quadriga import QuadrigaClient
from db import Data
import sms_client

daemon_config = config["daemon"]
qClient = QuadrigaClient()
data = Data()
active = False


def worker():
    while active:
        with open("notification_worker", "w") as file:
            file.write("{:%Y-%m-%d %H:%M:%S}".format(datetime.now()))

        cache = {} # avoid to call quadriga multiple times for the same book

        # Getting pending notifications
        notifications = data.select_untriggered()
        for notification in notifications:
            n_id = notification["id"]
            book = notification["book"]
            comp = notification["comp"]
            notification_value = notification["value"]

            ticker = cache.setdefault(book, qClient.get_summary(book))

            last = float(ticker["last"])
            satisfy = False
            if comp == '<=':
                satisfy = last <= notification_value
            elif comp == '>=':
                satisfy = last >= notification_value
            elif comp == '<':
                satisfy = last < notification_value
            elif comp == '>':
                satisfy = last > notification_value
            elif comp == '==':
                satisfy = last == notification_value
            else: # != or <>
                satisfy = last != notification_value

            if satisfy:
                when = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())
                pair = [x.upper() for x in book.split("_")]

                # msg ex: 1BTC = 10243.67CAD on 2017-11-21 21:13:17, triggered by btc_cad<=10250
                msg = f"1{pair[0]} = {str(last)}{pair[1]} on {when}, triggered by {book}{comp}{str(notification_value)}"
                sid = sms_client.send_message(msg)

                # update notification in the db
                notif = {"id": n_id, "triggered": when, "sid": sid}
                data.update(notif)

        time.sleep(daemon_config["wait_minutes"]*60)


def start():
    global active
    active = True
    d = threading.Thread(name='notification_worker', target=worker, daemon=True)
    d.start()


def stop():
    global active
    active = False
