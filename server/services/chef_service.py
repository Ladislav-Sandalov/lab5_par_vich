import threading
import time
import random
from server.datas.warehouse import warehouse, recipes
from server.datas.employees import chefs
from server.services.waiter_service import ready_queue

order_queue = []
lock = threading.Lock()

def process_orders():
    while True:
        with lock:
            for chef in chefs:
                if chef["status"] == "free" and order_queue:
                    order = order_queue.pop(0)
                    chef["status"] = "busy"
                    chef["current_order"] = order
                    threading.Thread(target=prepare_order, args=(chef, order)).start()
        time.sleep(1)

def prepare_order(chef, order):
    recipe = recipes.get(order["recipe_name"])
    if not recipe:
        chef["status"] = "free"
        chef["current_order"] = None
        return

    with lock:
        for ingredient, amount in recipe.items():
            if warehouse[ingredient] < amount * order["quantity"]:
                chef["status"] = "free"
                chef["current_order"] = None
                return
        for ingredient, amount in recipe.items():
            warehouse[ingredient] -= amount * order["quantity"]

    # Add noise to preparation time
    base_time = (10 if order["recipe_name"] == "fries" else 15) * order["quantity"]
    noise = random.uniform(-0.1, 0.1)
    time.sleep(base_time * (1 + noise))

    with lock:
        chef["status"] = "free"
        chef["current_order"] = None
        ready_queue.append(order)