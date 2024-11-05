import threading
import random
import time
from queue import Queue


class Table:
    def __init__(self, number, guest=None):
        self.number = number
        self.guest = guest


class Guest(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        num_second = random.randint(3, 10)
        time.sleep(num_second)


class Cafe:
    def __init__(self, queue, *tables):
        self.queue = queue
        self.tables = tables
        self.queue = Queue()

    def guest_arrival(self, *guests):
        if len(guests) == len(tables):
            for guest, table in guests, tables:
                table.guest = guest
                print(f'{guest.name} сел(-а) за стол номер {table.number})')
                guest.start()
        elif len(guests) < len(tables):
            for i in range(len(guests)):
                tables[i].guest = guests[i]
                print(f'{guests[i].name} сел(-а) за стол номер {tables[i].number}')
                guests[i].start()
        else:
            guests = list(guests)
            for j in range(len(tables)):
                tables[j].guest = guests[j]
                print(f'{guests[j].name} сел(-а) за стол номер {tables[j].number}')
                guests[j].start()
            for k in range(len(tables), len(guests)):
                self.queue.put(guests[k])
                print(f"{guests[k].name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() and [tables[i].guest is None for i in range(len(tables))]:
            for i in range(len(tables)):
                guest = tables[i].guest
                if tables[i].guest is None and not self.queue.empty():
                    guest = self.queue.get()
                    tables[i].guest = guest
                    guest.start()
                    print(f"{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {tables[i].number}")
                elif not tables[i].guest is None and tables[i].guest.is_alive() is False:
                    guest = tables[i].guest
                    tables[i].guest = None
                    print(f"{guest.name} покушал(-а) и ушёл(ушла)")
                    print(f'Стол номер {tables[i].number} свободен')


tables = [Table(number) for number in range(1, 6)]
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()
