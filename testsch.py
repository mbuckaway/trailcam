import sched, time
s = sched.scheduler(time.time, time.sleep)
def print_time(a='default'):
    s.enter(10, 1, print_time)
    print("From print_time", time.time(), a)

def print_some_times():
    print(time.time())
    s.enter(10, 1, print_time)
    s.run()
    print(time.time())

print_some_times()