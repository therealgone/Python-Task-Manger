import psutil
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("1000x1000")

        self.label_cpu = ttk.Label(root, text="CPU Usage: 0%")
        self.label_cpu.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.label_ram = ttk.Label(root, text="RAM Usage: 0%")
        self.label_ram.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.label_network = ttk.Label(root, text="Network Usage: 0 bytes")
        self.label_network.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.label_disk = ttk.Label(root, text="Disk Usage: 0%")
        self.label_disk.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.fig, (self.cpu_ax, self.ram_ax, self.disk_ax) = plt.subplots(3, 1, figsize=(8, 6))

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=1, rowspan=4, padx=10, pady=10)

        self.cpu_usage_data = []
        self.ram_usage_data = []
        self.disk_usage_data = []

        self.update_labels_and_graphs()

    def update_labels_and_graphs(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        disk_usage = psutil.disk_usage('/').percent

        self.label_cpu.config(text=f"CPU Usage: {cpu_usage:.2f}%")
        self.label_ram.config(text=f"RAM Usage: {ram_usage:.2f}%")
        self.label_network.config(text=f"Network Usage: {network_usage} bytes")
        self.label_disk.config(text=f"Disk Usage: {disk_usage:.2f}%")

        self.cpu_usage_data.append(cpu_usage)
        self.ram_usage_data.append(ram_usage)
        self.disk_usage_data.append(disk_usage)

        self.plot_graphs()

        self.root.after(100, self.update_labels_and_graphs)  # Update every 1000 milliseconds (1 second)

    def plot_graphs(self):
        self.cpu_ax.clear()
        self.ram_ax.clear()
        self.disk_ax.clear()

        self.cpu_ax.plot(self.cpu_usage_data, label='CPU Usage')
        self.ram_ax.plot(self.ram_usage_data, label='RAM Usage')
        
        # Disk usage bar graph out of 100
        self.disk_ax.bar(['Disk'], [self.disk_usage_data[-1]], color='blue', width=0.5)
        self.disk_ax.set_ylim(0, 100)  # Set y-axis limit to 100 for disk usage

        # Add 5-line gap between titles
        self.cpu_ax.text(0.5, 1.2, '', transform=self.cpu_ax.transAxes)
        self.ram_ax.text(0.5, 1.2, '', transform=self.ram_ax.transAxes)
        self.disk_ax.text(0.5, 1.2, '', transform=self.disk_ax.transAxes)

        self.cpu_ax.set_title('CPU Usage Over Time')
        self.ram_ax.set_title('RAM Usage Over Time')
        self.disk_ax.set_title('Disk Usage')

        self.cpu_ax.legend()
        self.ram_ax.legend()

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitor(root)
    root.mainloop()
