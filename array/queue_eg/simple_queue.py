class SimpleQueue(object):
    def __init__(self, cap):
        self.capacity = cap
        self.current_index = 0
        self.queue = []
