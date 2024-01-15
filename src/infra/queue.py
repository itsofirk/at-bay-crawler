from multiprocessing import Queue

queue = None


def init_queue():
    global queue
    queue = Queue()
    return queue
