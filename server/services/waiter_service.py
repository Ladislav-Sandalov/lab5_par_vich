import threading
import time
from server.datas.employees import waiters
from server.datas.warehouse import prices, revenue

ready_queue = []
lock = threading.Lock()

def deliver_orders():
    global revenue
    while True:
        with lock:
            for waiter in waiters:
                if waiter["status"] == "free" and ready_queue:
                    order = ready_queue.pop(0)
                    waiter["status"] = "busy"
                    waiter["current_order"] = order
                    threading.Thread(target=deliver_order, args=(waiter, order)).start()
        time.sleep(1)

def deliver_order(waiter, order):
    global revenue
    time.sleep(5)
    with lock:
        revenue += prices[order["recipe_name"]] * order["quantity"]
        waiter["status"] = "free"
        waiter["current_order"] = None