# quadriga_notifier
QuadrigaCX notifications for cryptocurrency price events

```
$ python quadriga_notifier.py
QuadrigaCX Notifications. Type 'help' to learn about available commands.
Type 'start' to start notification service. 
> help
Type 'help [notify|list|remove|start|stop|status|help|quit|exit]'

> help notify
Creates a notification.
Usage: > notify [btc_cad|bch_cad|ltc_cad|eth_btc|eth_cad|btc_usd] [<|>|<=|>=|==|<>|!=] [value]
Example: > notify btc_cad <= 8540.25

> help list
Lists pending notifications. Usage: > list

> help remove
Removes pending notification. Usage: > remove [id]
Example: > remove 5

> help start
Starts notification service. Usage: > start

> help stop
Stops notification service. Usage: > stop

> help status
Show notification service status. Usage: > status

> help quit
Exits QuadrigaCX Notifications and stops notification service

> notify btc_cad <= 10200.45

> notify eth_cad <= 400

> notify ltc_cad >= 95

> notify bch_cad > 1500

> list
ID     Trigger            Created
==     =======            =======
1      btc_cad <= 10200.45      2017-11-23 20:35:57
2      eth_cad <= 400      2017-11-23 20:36:05
3      ltc_cad >= 95      2017-11-23 20:36:15
4      bch_cad > 1500      2017-11-23 20:36:25

> remove 4

> list
ID     Trigger            Created
==     =======            =======
1      btc_cad <= 10200.45      2017-11-23 20:35:57
2      eth_cad <= 400      2017-11-23 20:36:05
3      ltc_cad >= 95      2017-11-23 20:36:15

> start
Notification service enabled

> status
Notification service enabled. Last run: 2017-11-23 20:36:53

> stop
Notification service disabled

> status
Notification service disabled

> exit
Process finished with exit code 0
```

config.yaml example:

```
#twilio account (for sms message)
twilio:
    account_sid: xxxxxxxxxxxxxxxxxxxxxxxx
    auth_token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    to: +14151234567
    from: +14157654321

#notification daemon
daemon:
    wait_minutes: 1
```
