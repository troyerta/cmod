import time
import multiprocessing

PROCESSES = multiprocessing.cpu_count() - 1

# Try adding enum of module and total num modules as args, then
# Assume the function passes back the complete string that needs
# to be printed. Add it to a another queue here, and the master
# process will consume the output for printing serially
def process_tasks( task_queue, function ):
    while not task_queue.empty():
        module = task_queue.get()
        function( module )
    return True

def run( function, module_list ):
    task_queue = multiprocessing.Queue()

    [task_queue.put( module ) for module in module_list]

    processes = []
    print(f'Running with {PROCESSES} processes!')
    start = time.time()
    for n in range(PROCESSES):
        p = multiprocessing.Process(
            target=process_tasks, args=( task_queue, function ) )
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print(f'Time taken = {time.time() - start:.10f}')
