from multiprocessing.pool import Pool

from joblib import Parallel, delayed
import multiprocessing
import time

# what are your inputs, and what operation do you want to
# perform on each input. For example...
inputs = range(9999999)


def processInput(i):
    return i * i


num_cores = multiprocessing.cpu_count()
start_time = time.time()
pool = Pool(num_cores)
results = pool.map(processInput, inputs)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
# results = [processInput(i) for i in inputs]
results = []
for i in inputs:
    results.append(processInput(i))
print("--- %s seconds ---" % (time.time() - start_time))

#print(results)