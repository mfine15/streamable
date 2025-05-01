from streamable import Stream
import time
import random

def sleep_and_return(x):
    time.sleep(random.random() * 0.00001)
    return x

stream = Stream(range(100000))
result = stream.progress(total=100000).map(sleep_and_return).filter(lambda x: x % 2 == 0)
list(result)
