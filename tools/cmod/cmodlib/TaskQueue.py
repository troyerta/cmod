import time
import multiprocessing

# from tasks import get_word_counts


PROCESSES = multiprocessing.cpu_count() - 1
# NUMBER_OF_TASKS = 10


def process_tasks( task_queue, function ):
    while not task_queue.empty():
        book = task_queue.get()
        function(book)
    return True


def add_tasks(task_queue, module_list):
    for module in module_list:
        task_queue.put( module )
    return task_queue


def run( function, module_list ):
    empty_task_queue = multiprocessing.Queue()
    full_task_queue = add_tasks( empty_task_queue, module_list )
    processes = []
    print(f'Running with {PROCESSES} processes!')
    start = time.time()
    for n in range(PROCESSES):
        p = multiprocessing.Process(
            target=process_tasks, args=( full_task_queue, function ) )
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print(f'Time taken = {time.time() - start:.10f}')
