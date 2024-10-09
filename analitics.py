import psutil
import time
import threading

class Memory:
    def __init__(self, interval=0.1):
        self.interval = interval
        self.memory_readings = []
        self.monitoring = False
        self.monitor_thread = None

    def _monitor_memory(self):
        process = psutil.Process()
        while self.monitoring:
            mem_info = process.memory_info()
            self.memory_readings.append(mem_info.rss)  # RSS (Resident Set Size)
            time.sleep(self.interval)

    def start(self):
        self.memory_readings = []
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_memory)
        self.monitor_thread.start()

    def stop(self):
        self.monitoring = False
        if self.monitor_thread is not None:
            self.monitor_thread.join()
        self.monitor_thread = None

    def get_results(self):
        if not self.memory_readings:
            return {"average_memory": 0, "max_memory": 0}

        avg_memory = sum(self.memory_readings) / len(self.memory_readings)
        max_memory = max(self.memory_readings)
        return {"average_memory": avg_memory / (1024 ** 2),  # Convert to MB
                "max_memory": max_memory / (1024 ** 2)}      # Convert to MB

#
# # Example usage:
# def myfunc():
#     # Some heavy computation or memory allocation
#     big_list = [x for x in range(10**7)]  # Simulate memory usage
#     time.sleep(2)
#     del big_list  # Release memory
#     time.sleep(1)
#
# # Initialize the analytics class
# analytics = SomeAnalytics()
#
# # Start monitoring
# analytics.start()
# myfunc()
# # Stop monitoring
# analytics.stop()
#
# # Get results
# results = analytics.get_results()
# print(f"Average memory usage: {results['average_memory']:.2f} MB")
# print(f"Maximum memory usage: {results['max_memory']:.2f} MB")
