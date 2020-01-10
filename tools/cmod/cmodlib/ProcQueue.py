from multiprocessing import Lock, Process, Queue, current_process, cpu_count
import time
import queue # imported for using queue.Empty exception

def do_job(tasks_to_accomplish, tasks_that_are_done, function):
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
        except queue.Empty:

            break
        else:
            '''
                if no exception has been raised, add the task completion
                message to task_that_are_done queue
            '''
            # print(task)
            # time.sleep(.2)
            function( task )
            tasks_that_are_done.put(task.name + ' was tested by ' + current_process().name)
            time.sleep(.2)
    return True


def multi_proc( function, module_list ):
    number_of_task = 50
    # number_of_processes = cpu_count() - 1
    number_of_processes = 7
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    processes = []

    # for i in range(number_of_task):
        # tasks_to_accomplish.put("Task no " + str(i))

    [tasks_to_accomplish.put( module ) for module in module_list]

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=do_job, args=(tasks_to_accomplish, tasks_that_are_done, function))
        processes.append(p)
        p.start()

    # print the output
    tasks_ackd = 0
    while tasks_to_accomplish.qsize() > 0 or tasks_ackd < len(module_list):
    # for i in range(number_of_task):
        print(tasks_that_are_done.get( True, timeout=5.0 ))
        tasks_ackd += 1

    [p.join() for p in processes]
