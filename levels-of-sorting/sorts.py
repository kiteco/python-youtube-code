# GENERAL UTILITY FUNCTIONS FOR ALL
def scale(xs):
    for i in range(len(xs)):
        yield xs + ['', [i]]
    yield xs + ['', []]

def buffer(xs):
    for i in range(20):
        yield xs + ['', []]

# SORTING ALGORITHMS
def bubble_sort(xs):  # https://en.wikipedia.org/wiki/Bubble_sort
    yield from buffer(xs)
    length = len(xs)
    while True:
        swapped = False
        yield xs + ['', [0]]
        for i in range(1, length):
            if xs[i - 1] > xs[i]:
                xs[i - 1], xs[i] = xs[i], xs[i - 1]
                swapped = True
            yield xs + ['', [i - 1, i]]
        length -= 1
        if not swapped:
            break
    yield xs + ['', []]
    #yield from scale(xs)


def selection_sort(xs):  # https://en.wikipedia.org/wiki/Selection_sort
    yield from buffer(xs)
    for i in range(len(xs)):
        min_idx = i
        for j in range(i + 1, len(xs)):
            if xs[j] < xs[min_idx]:
                yield xs + ['', [j, min_idx]]
                min_idx = j
            else:
                yield xs + ['', [j, min_idx]]
        if min_idx != i:
            xs[min_idx], xs[i] = xs[i], xs[min_idx]            
            yield xs + ['', [i]]
    yield xs + ['', []]
    # yield from scale(xs)


def insertion_sort(xs):  # https://en.wikipedia.org/wiki/Insertion_sort
    yield from buffer(xs)
    i = 1
    while i < len(xs):
        x = xs[i]
        j = i - 1
        yield xs + ['', [i, j]]
        while j >= 0 and xs[j] > x:
            xs[j + 1] = xs[j]
            xs[j] = x
            yield xs + ['', [j, j + 1]]
            j -= 1
        xs[j + 1] = x
        i += 1
    yield xs + ['', []]
    #yield from scale(xs)


def bin_ins_sort(xs):  # https://en.wikipedia.org/wiki/Insertion_sort
    def binary_search(xs, target_i, start, end):
        if start >= end:
            if start > end or xs[start] > xs[target_i]:
                yield xs + [[start, target_i]]
                return start
            else:
                yield xs + [[start + 1, target_i]]
                return start + 1
            yield xs + [[start, end]]

        mid = (start + end) // 2

        yield xs + [[mid, target_i]]
        if xs[mid] < xs[target_i]:
            result = yield from binary_search(xs, target_i, mid + 1, end)
            return result
        elif xs[mid] > xs[target_i]:
            result = yield from binary_search(xs, target_i, start, mid - 1)
            return result
        else:
            return mid

    for i in range(1, len(xs)):
        swap = yield from binary_search(xs, i, 0, i - 1)
        yield xs + [[i, swap]]
        xs = xs[:swap] + [xs[i]] + xs[swap:i] + xs[i + 1:]
        yield xs + [[swap]]
        yield xs + [[]]
    yield xs + [[]]

        

def shellsort(xs):  # https://en.wikipedia.org/wiki/Shellsort
    # Marcin Ciura's gap sequence (https://oeis.org/A102549)
    gaps = [gap for gap in [701, 301, 132, 57, 23, 10, 4, 1] if gap < len(xs)]

    for gap in gaps:
        for i in range(gap, len(xs)):
            current = xs[i]
            j = i
            while j >= gap and xs[j - gap] > current:
                xs[j] = xs[j - gap]
                j -= gap
                yield xs + [[i, j, j - gap]]
            yield xs + [[i, j, j - gap]]
            xs[j] = current 
            yield xs + [[i, j]]
    yield xs + [[]]


def merge_sort(xs):  # https://en.wikipedia.org/wiki/Merge_sort
    yield from buffer(xs)
    def merge(xs, start, mid, end):
        merged = list()
        left = start
        right = mid

        while left < mid and right < end:
            if xs[left] < xs[right]:
                merged.append(xs[left])
                yield xs + ['Merging', [left, right]]
                left += 1
            else:
                merged.append(xs[right])
                yield xs + ['Merging', [left, right]]
                right += 1

        while left < mid:
            merged.append(xs[left])
            yield xs + ['Merging', [left]]
            left += 1
            

        while right < end:
            merged.append(xs[right])
            yield xs + ['Merging', [right]]
            right += 1
            
        for i, val in enumerate(merged):
            xs[start + i] = val
            yield xs + ['Merging', [start + i]]
        
    def mergesort_runner(xs, start, end):       
        if end - start <= 1:
            if end - start == 1:
                yield xs + ['Dividing', [start]]
            return

        mid = start + (end - start) // 2
        yield from mergesort_runner(xs, start, mid)
        yield from mergesort_runner(xs, mid, end)
        yield from merge(xs, start, mid, end)

    yield from mergesort_runner(xs, 0, len(xs))
    yield xs + ['', []]
    #yield from scale(xs)


def quicksort(xs):  # https://en.wikipedia.org/wiki/Quicksort
    yield from buffer(xs)
    # Hoare partition scheme
    def partition(xs, lo, hi):
        pivot_idx = (lo + hi) // 2
        pivot = xs[pivot_idx]
        i = lo - 1
        j = hi + 1
        while True:
            i += 1
            while xs[i] < pivot:
                yield xs + ['', [i, pivot_idx]]
                i += 1
            j -= 1
            while xs[j] > pivot:
                yield xs + ['', [j, pivot_idx]]
                j -= 1
            if i >= j:
                return j
            yield xs + ['', [i, j]]
            xs[i], xs[j] = xs[j], xs[i]
            #yield xs + [[i, j]]
        
    def quicksort_runner(xs, lo, hi):
        if lo < hi:
            p = yield from partition(xs, lo, hi)
            yield from quicksort_runner(xs, lo, p)
            yield from quicksort_runner(xs, p + 1, hi)

    yield from quicksort_runner(xs, 0, len(xs) - 1)
    yield xs + ['', []]
    #yield from scale(xs)


def heapsort(xs):  # https://en.wikipedia.org/wiki/Heapsort
    yield from buffer(xs)
    def max_heapify(xs, i, end):
        
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i

        if left < end and xs[left] > xs[largest]:
            largest = left
        yield xs + ['Building heap', [left, largest]]

        if right < end and xs[right] > xs[largest]:
            largest = right
        yield xs + ['Building heap', [right, largest]]

        if largest != i:
            xs[i], xs[largest] = xs[largest], xs[i]
            yield xs + ['Building heap', [i, largest]]
            yield from max_heapify(xs, largest, end)
        yield xs + ['Building heap', [i, largest]]

    def build_heap(xs):
        for i in range(len(xs) // 2, -1, -1):
            yield from max_heapify(xs, i, len(xs))

    def sift_down(xs, start, end):
        root = start
        while root * 2 + 1 <= end:
            child = root * 2 + 1
            swap = root

            if xs[swap] < xs[child]:
                yield xs + ['Heapify', [swap, child]]
                swap = child
            else:
                yield xs + ['Heapify', [swap, child]]
            
            if child + 1 <= end and xs[swap] < xs[child + 1]:
                yield xs + ['Heapify', [swap, child + 1]]
                swap = child + 1
            else:
                yield xs + ['Heapify', [swap, child + 1]]

            if swap == root:
                return
            else:
                xs[root], xs[swap] = xs[swap], xs[root]
                yield xs + ['Heapify', [swap, root]]
                root = swap

    def heapsort_runner(xs):
        yield from build_heap(xs)
        end = len(xs) - 1

        while end > 0:
            xs[end], xs[0] = xs[0], xs[end]
            yield xs + ['', [0, end]]
            end -= 1
            yield from sift_down(xs, 0, end)

    yield from heapsort_runner(xs)
    yield xs + ['', []]
    #yield from scale(xs)
