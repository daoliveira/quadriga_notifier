from sqlite3 import connect, Row
from datetime import datetime


class Data(object):
    def __init__(self):
        self.conn = connect("db")
        self.conn.execute("create table if not exists notification (" +
                          "id integer primary key autoincrement, book text, comp text, " +
                          "value numeric, created integer, triggered integer, sid text)")
        self.conn.commit()
        self.conn.close()

    def insert(self, book, comp, value):
        self.conn = connect("db")
        self.conn.execute("insert into notification (" +
                          "book, comp, value, created) values(?, ?, ?, ?)",
                          (book, comp, value, "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())))
        self.conn.commit()
        self.conn.close()

    def select_untriggered(self):
        self.conn = connect("db")
        self.conn.row_factory = Row  # return dict instead of tuples
        curr = self.conn.execute("select * from notification where triggered is null")
        notifications = curr.fetchall()
        self.conn.close()
        return notifications

    def select_all(self):
        self.conn = connect("db")
        self.conn.row_factory = Row  # return dict instead of tuples
        curr = self.conn.execute("select * from notification")
        notifications = curr.fetchall()
        self.conn.close()
        return notifications

    def update(self, notification):
        if not notification["id"]:
            raise ValueError
        fields=[]
        for key,value in notification.items():
            if key == "id":
                continue
            fields.append(str(key)+"='"+str(value)+"'")

        sql = "update notification set " + ", ".join(fields) + " where id=" + str(notification["id"])
        self.conn = connect("db")
        self.conn.execute(sql)
        self.conn.commit()
        self.conn.close()

    def delete(self, notification_id):
        self.conn = connect("db")
        self.conn.execute(f"delete from notification where id={str(notification_id)}")
        self.conn.commit()
        self.conn.close()

