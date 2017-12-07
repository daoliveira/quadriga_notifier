import threading
import time
from datetime import datetime
from config import config
from quadriga import QuadrigaClient
from db import Data
import sms_client
import logging as log

log.basicConfig(filename="notification_worker.log", level=log.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                )

daemon_config = config["daemon"]
qClient = QuadrigaClient()
data = Data()


def worker():
    while True:

        cache = {} # avoid to call quadriga multiple times for the same book

        # Getting pending notifications
        log.info("Querying DB for pending notifications")
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
                msg = "1%s = %s%s on %s, triggered by %s%s%s" % (pair[0], last, pair[1], when, book, comp, notification_value)
                log.info("Sending SMS message: %s", msg)
                sid = sms_client.send_message(msg)

                # update notification in the db
                notif = {"id": n_id, "triggered": when, "sid": sid}
                data.update(notif)
        else:
            log.info("No pending notifications this time")

        time.sleep(daemon_config["wait_minutes"]*60)


def start():
    worker()
    #d = threading.Thread(name='notification_worker', target=worker, daemon=True)
    #d.start()


if __name__ == '__main__':
    start()
