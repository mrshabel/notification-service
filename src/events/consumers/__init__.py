from .main import start_main_consumer

# from concurrent.futures import ThreadPoolExecutor
# from multiprocessing import cpu_count
# from . import main as main_consumer
# from threading import Lock

# lock = Lock()


# def start_consumers():
#     """
#     Spin up a threadpool to execute all consumers in the application
#     """
#     # max_workers = cpu_count() if cpu_count else 2
#     with ThreadPoolExecutor(max_workers=2) as executor:
#         with lock:
#             # protect shared resources
#             # submit consumers
#             executor.submit(main_consumer.consume_main_queue).result()
