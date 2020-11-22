from client import Client
import time

c1 = Client("Augustine")
c2 = Client("Nick")

c1.send_message("hello")
time.sleep(2)
c2.send_message("hello 2")
time.sleep(2)
c1.send_message("whats up?")
time.sleep(2)
c2.send_message("boring")
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()