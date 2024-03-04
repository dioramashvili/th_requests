import json
import queue

import requests
import threading

base_url = 'https://dummyjson.com/products'


def send_request_and_store_data(url, result_queue):
    response = requests.get(url)
    data = response.json()

    result_queue.put(data)


result_queue = queue.Queue()
file_lock = threading.Lock()
threads = []

for i in range(1, 101):
    url = f"{base_url}/{i}"
    thread = threading.Thread(target=send_request_and_store_data, args=(url, result_queue))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

all_data = []
while not result_queue.empty():
    all_data.append(result_queue.get())

with file_lock:
    with open("data.json", "w") as json_file:
        json.dump(all_data, json_file, indent=2)
