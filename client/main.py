import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"  # URL сервера


class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management App")
        self.root.geometry("800x600")

        # Основные кнопки
        tk.Button(root, text="View Halls", command=self.view_halls, width=20).pack(pady=5)
        tk.Button(root, text="Reserve Table", command=self.reserve_table, width=20).pack(pady=5)
        tk.Button(root, text="Create Order", command=self.create_order, width=20).pack(pady=5)
        tk.Button(root, text="View Warehouse", command=self.view_warehouse, width=20).pack(pady=5)
        tk.Button(root, text="Order Queue", command=self.view_order_queue, width=20).pack(pady=5)
        tk.Button(root, text="Exit", command=root.quit, width=20).pack(pady=5)

        # Поле информации
        self.info_text = tk.Text(root, width=80, height=30)
        self.info_text.pack(pady=10)

    def view_halls(self):
        """Отображение статуса залов и столиков."""
        try:
            response = requests.get(f"{BASE_URL}/halls")
            response.raise_for_status()
            halls = response.json()
            self.info_text.delete(1.0, tk.END)
            for hall in halls:
                self.info_text.insert(tk.END, f"{hall['name']}:\n")
                for table in hall["tables"]:
                    status = "Reserved" if table["status"] == "reserved" else "Free"
                    self.info_text.insert(tk.END, f"  Table {table['id']}: {status}\n")
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to fetch hall data.")

    def reserve_table(self):
        """Бронирование или снятие брони со столика."""
        def submit_reservation():
            hall_id = int(hall_entry.get())
            table_id = int(table_entry.get())
            action = "reserve" if action_var.get() == "Reserve" else "free"
            try:
                response = requests.post(f"{BASE_URL}/halls/{hall_id}/tables/{table_id}/{action}")
                response.raise_for_status()
                messagebox.showinfo("Success", response.json()["message"])
                reservation_window.destroy()
            except requests.RequestException:
                messagebox.showerror("Error", "Failed to update table status.")

        reservation_window = tk.Toplevel(self.root)
        reservation_window.title("Reserve Table")
        tk.Label(reservation_window, text="Hall ID:").grid(row=0, column=0)
        tk.Label(reservation_window, text="Table ID:").grid(row=1, column=0)
        tk.Label(reservation_window, text="Action:").grid(row=2, column=0)

        hall_entry = tk.Entry(reservation_window)
        hall_entry.grid(row=0, column=1)
        table_entry = tk.Entry(reservation_window)
        table_entry.grid(row=1, column=1)

        action_var = tk.StringVar(value="Reserve")
        tk.OptionMenu(reservation_window, action_var, "Reserve", "Free").grid(row=2, column=1)

        tk.Button(reservation_window, text="Submit", command=submit_reservation).grid(row=3, column=0, columnspan=2)

    def create_order(self):
        """Создание заказа."""
        def submit_order():
            recipe_name = recipe_entry.get()
            quantity = int(quantity_entry.get())
            hall_id = int(hall_entry.get())
            table_id = int(table_entry.get())
            order_data = {
                "recipe_name": recipe_name,
                "quantity": quantity,
                "hall_id": hall_id,
                "table_id": table_id,
            }
            try:
                response = requests.post(f"{BASE_URL}/orders", json=order_data)
                response.raise_for_status()
                messagebox.showinfo("Success", response.json()["status"])
                order_window.destroy()
            except requests.RequestException:
                messagebox.showerror("Error", "Failed to create order.")

        order_window = tk.Toplevel(self.root)
        order_window.title("Create Order")
        tk.Label(order_window, text="Recipe Name:").grid(row=0, column=0)
        tk.Label(order_window, text="Quantity:").grid(row=1, column=0)
        tk.Label(order_window, text="Hall ID:").grid(row=2, column=0)
        tk.Label(order_window, text="Table ID:").grid(row=3, column=0)

        recipe_entry = tk.Entry(order_window)
        recipe_entry.grid(row=0, column=1)
        quantity_entry = tk.Entry(order_window)
        quantity_entry.grid(row=1, column=1)
        hall_entry = tk.Entry(order_window)
        hall_entry.grid(row=2, column=1)
        table_entry = tk.Entry(order_window)
        table_entry.grid(row=3, column=1)

        tk.Button(order_window, text="Submit", command=submit_order).grid(row=4, column=0, columnspan=2)

    def view_warehouse(self):
        """Просмотр склада и выручки."""
        try:
            response = requests.get(f"{BASE_URL}/warehouse")
            response.raise_for_status()
            data = response.json()
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "Warehouse:\n")
            for item, quantity in data["warehouse"].items():
                self.info_text.insert(tk.END, f"  {item}: {quantity}\n")
            self.info_text.insert(tk.END, f"\nRevenue: {data['revenue']} RUB\n")
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to fetch warehouse data.")

    def view_order_queue(self):
        """Просмотр очереди заказов у поваров и официантов."""
        try:
            response = requests.get(f"{BASE_URL}/employees")
            response.raise_for_status()
            data = response.json()
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "Chefs:\n")
            for chef in data["chefs"]:
                status = "Busy" if chef["status"] == "busy" else "Free"
                self.info_text.insert(tk.END, f"  Chef {chef['id']}: {status}\n")
            self.info_text.insert(tk.END, "\nWaiters:\n")
            for waiter in data["waiters"]:
                status = "Busy" if waiter["status"] == "busy" else "Free"
                self.info_text.insert(tk.END, f"  Waiter {waiter['id']}: {status}\n")
        except requests.RequestException:
            messagebox.showerror("Error", "Failed to fetch employee data.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()