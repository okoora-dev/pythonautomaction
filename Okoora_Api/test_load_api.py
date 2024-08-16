import time
import multiprocessing
from pytest import mark
from test_load_convertg import test_load_convert

@mark.load_test
def test_loading():
    processes = []

    for x in range(5):
        p = multiprocessing.Process(target=test_load_convert)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
        print(f"{p.name} call API 20 times")


    finish = time.perf_counter()
    print("Finished running after seconds : ",finish)

