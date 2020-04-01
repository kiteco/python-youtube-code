import math

def buffer(xs):
    for i in range(20):
        yield xs + [[]]

def scale(xs):
    for i in range(len(xs)):
        yield xs + [[i]]
    yield xs + [[]]

def introsort(xs, insertion_threshold=16):  # https://en.wikipedia.org/wiki/Introsort
    yield from buffer(xs)
    def bin_ins_sort(xs, lo, hi):  # insertion sort routine for introsort
        def binary_search(xs, target, start, end):
            if start >= end:
                if start > end or xs[start] > target:
                    yield xs + ['Running Insertion sort', [start]]
                    return start
                else:
                    yield xs + ['Running Insertion sort', [start + 1]]
                    return start + 1
                yield xs + ['Running Insertion sort', [start, end]]

            mid = (start + end) // 2

            yield xs + ['Running Insertion sort', [mid]]
            if xs[mid] < target:
                result = yield from binary_search(xs, target, mid + 1, end)
                return result
            elif xs[mid] > target:
                result = yield from binary_search(xs, target, start, mid - 1)
                return result
            else:
                return mid

        for i in range(lo, hi):
            swap = yield from binary_search(xs, xs[i], lo, i - 1)
            yield xs + ['Running Insertion sort', [i, swap]]
            xs = xs[:swap] + [xs[i]] + xs[swap:i] + xs[i + 1:]
        #yield xs + [[]]
        return xs

    def partition(xs, lo, hi):  # Hoare partition routine
        pivot_idx = (lo + hi) // 2
        pivot = xs[pivot_idx]
        i = lo - 1
        j = hi + 1
        while True:
            i += 1
            while xs[i] < pivot:
                yield xs + ['Running Quicksort', [i, pivot_idx]]
                i += 1
            else:
                yield  xs + ['Running Quicksort', [i, pivot_idx]]
            j -= 1
            while xs[j] > pivot:
                yield xs + ['Running Quicksort', [j, pivot_idx]]
                j -= 1
            else:
                yield xs + ['Running Quicksort', [j, pivot_idx]]
            if i >= j:
                yield xs + ['Running Quicksort', [i, j]]
                return j
            xs[i], xs[j] = xs[j], xs[i]
            yield xs + ['Running Quicksort', [i, j]]

    def heapsort(xs, lo, hi):  # heapsort routine for introsort
        def max_heapify(xs, i, end):
            
            left = 2 * (i - lo) + 1 + lo
            right = 2 * (i - lo) + 2 + lo
            largest = i

            if left < end and xs[left] > xs[largest]:
                largest = left
            # yield xs + [[left, largest]]

            if right < end and xs[right] > xs[largest]:
                largest = right
            # yield xs + [[right, largest]]

            if largest != i:
                xs[i], xs[largest] = xs[largest], xs[i]
                # yield xs + [[i, largest]]
                yield from max_heapify(xs, largest, end)
            yield xs + ['Running Heapsort', [i]]

        def build_heap(xs, lo, hi):
            for i in range(lo + (hi - lo) // 2 + 1, lo - 1, -1):
                yield from max_heapify(xs, i, hi + 1)            

        def sift_down(xs, start, end):
            root = start
            while start + (root - start) * 2 + 1 <= end:
                child = start + (root - start) * 2 + 1
                swap = root

                if xs[swap] < xs[child]:
                    yield xs + ['Running Heapsort', [swap, child]]
                    swap = child
                else:
                    yield xs + [[swap, child]]
                
                if child + 1 <= end and xs[swap] < xs[child + 1]:
                    yield xs + ['Running Heapsort', [swap, child + 1]]
                    swap = child + 1
                else:
                    yield xs + ['Running Heapsort', [swap, child + 1]]

                if swap == root:
                    return
                else:
                    xs[root], xs[swap] = xs[swap], xs[root]
                    yield xs + ['Running Heapsort', [swap, root]]
                    root = swap

        def heapsort_runner(xs, lo, hi):
            yield from build_heap(xs, lo, hi)
            end = hi

            while end > lo:
                xs[end], xs[lo] = xs[lo], xs[end]
                yield xs + ['Running Heapsort', [lo, end]]
                end -= 1
                yield from sift_down(xs, lo, end)

        yield from heapsort_runner(xs, lo, hi)
        #yield xs + [[]]
        return xs

    def introsort_runner(max_depth, lo, hi):
        nonlocal xs
        if hi - lo <= insertion_threshold:
            xs = yield from bin_ins_sort(xs, lo, hi + 1)
            return       
        elif max_depth <= 0:
            xs = yield from heapsort(xs, lo, hi)
            return
        else:
            p = yield from partition(xs, lo, hi)
            yield from introsort_runner(max_depth - 1, lo, p)
            yield from introsort_runner(max_depth - 1, p + 1, hi)

    max_depth = 2 * math.floor(math.log(len(xs)))
    yield from introsort_runner(max_depth, 0, len(xs) - 1)
    yield xs + ['', []]
    #yield from scale(xs)