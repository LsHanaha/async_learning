import socket


def corutine(f):
    def inner(*args, **kwargs):
        g = f(*args, **kwargs)
        g.send(None)
        return g
    return inner


def subgen():
    while True:
        x = 'Ready to accept message'
        message = yield x
        print('Subgen recieved: ', message)


@corutine
def average():
    count = 0
    summ = 0
    avg = None
    while True:
        try:
            x = yield avg
        except StopIteration:
            print('Done')
            break
        else:
            count += 1
            summ += x
            avg = round(summ / count, 2)
    return avg