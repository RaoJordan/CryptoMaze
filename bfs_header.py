class Queue:
    def __init__(self, size_q):
        self.size_queue = size_q
        self.array = [[0, 0] for _ in range(2 * self.size_queue)]
        self.eid = [0] * self.size_queue
        self.front = -1
        self.rear = -1


    def push(self, eid, count):
        self.front += 1
        self.array[self.front] = [eid, count]

    def pop(self):
        if not self.empty():
            self.rear += 1
            return self.array[self.rear]
        else:
            return None

    def empty(self):
        return self.front == self.rear


def freeup(q):
    # Memory deallocation is automatically handled in Python
    pass
