def buffer(xs):
    for i in range(20):
        yield xs + ['', []]

def scale(xs):
    for i in range(len(xs)):
        yield xs + [[i]]
    yield xs + [[]]

def timsort(xs):  
    yield from buffer(xs)

    # https://en.wikipedia.org/wiki/Timsort
    # https://github.com/python/cpython/blob/master/Objects/listsort.txt

    def binary_search(xs, target_i, start, end, dispatch):
        yield xs + [dispatch, [start, end]]
        if start >= end:
            if start > end or xs[start] > xs[target_i]:
                yield xs + [dispatch, [start, target_i]]
                return start
            else:
                yield xs + [dispatch, [start + 1]]
                return start + 1
            

        mid = (start + end) // 2
        yield xs + [dispatch, [mid, target_i]]
        if xs[mid] < xs[target_i]:
            if mid == len(xs) - 1:
                return len(xs)
            result = yield from binary_search(xs, target_i, mid + 1, end, dispatch)
            return result
        elif xs[mid] > xs[target_i]:
            result = yield from binary_search(xs, target_i, start, mid - 1, dispatch)
            return result
        else:
            return mid
        
    def bin_ins_sort(xs, lo, hi, start):  # insertion sort routine
        for i in range(start, hi):
            swap = yield from binary_search(xs, i, lo, i - 1, 'Building run')
            yield xs + ['Building run', [i, swap]]
            xs = xs[:swap] + [xs[i]] + xs[swap:i] + xs[i + 1:]
        #yield xs + [[]]
        return xs

    if len(xs) <= 32:
        yield from bin_ins_sort(xs, 0, len(xs), 0)
        return
    
    def find_minrun():
        length = len(xs)
        bits =  length.bit_length() - 5
        minrun = length >> bits
        mask = (1 << bits) - 1
        if (length & mask):
            minrun += 1
        return minrun

    def count_run(xs, start):  # finds length of next run, swaps if decreasing
        if start >= len(xs):
            yield xs + ['Building run', []]
            return 0
        elif start == len(xs) - 1:
            yield xs + ['Building run', [len(xs) - 1]]
            return 1

        curr = start
        if xs[curr + 1] < xs[curr]:
            yield xs + ['Building run', [curr, curr + 1]]
            curr += 1
            while curr < len(xs) - 1 and xs[curr + 1] < xs[curr]:
                yield xs + ['Building run', [curr, curr + 1]]
                curr += 1
            i = start
            j = curr
            while i < j:
                xs[i], xs[j] = xs[j], xs[i]
                yield xs + ['Building run', [i, j]]
                i += 1 
                j -= 1
            return curr - start + 1
        else:
            curr += 1
            while curr < len(xs) - 1 and xs[curr + 1] >= xs[curr]:
                yield xs + ['Building run', [curr, curr + 1]]
                curr += 1
            return curr - start + 1

    def merge_collapse(xs, s):  # keeps track of stack invariants; merges while invariants broken
        while True:
            if len(s) >= 3:
                a = s[-3]
                b = s[-2]
                c = s[-1]
                if a[1] <= b[1] + c[1] or b[1] <= c[1]:
                    if a[1] <= b[1] + c[1]:
                        if a[1] > c[1]:
                            start = min(b[0], c[0])
                            yield from merge(xs, b, c)
                            s.pop()
                            s.pop()
                            s.append((start, b[1] + c[1]))
                        else:
                            start = min(a[0], b[0])
                            yield from merge(xs, a, b)
                            s.pop(-3)
                            s.pop(-2)
                            s.append((start, a[1] + b[1]))
                    else:
                        start = min(b[0], c[0])
                        yield from merge(xs, b, c)
                        s.pop()
                        s.pop()
                        s.append((start, b[1] + c[1]))
                    continue
                else:
                    break

            if len(s) == 2:
                b = s[-2]
                c = s[-1]
                if b[1] <= c[1]:
                    start = min(b[0], c[0])
                    yield from merge(xs, b, c)
                    s.pop()
                    s.pop()
                    s.append((start, b[1] + c[1]))
            break

    MIN_GALLOP = 7
    gallop_threshold = 7

    def gallop(xs, target_i, start, end):
        nonlocal MIN_GALLOP
        nonlocal gallop_threshold
        k = 1
        idx = start
        while idx < end and xs[idx] < xs[target_i]:
            yield xs + ['Galloping!', [idx, target_i]]
            idx = start + 2 ** k - 1
            k += 1
        result = yield from binary_search(xs, target_i, 
                                          start + (idx - start + 1) // (2 ** (k - 1)),  min(idx, end),
                                          'Galloping!')
        if result - start >= MIN_GALLOP:
            gallop_threshold -= 1
        else:
            gallop_threshold += 1
        return result


    def merge(xs, small_tup, big_tup):  # merge runs from stack together
        nonlocal MIN_GALLOP
        nonlocal gallop_threshold
        if big_tup[1] < small_tup[1]:
            small_tup, big_tup = big_tup, small_tup

        sm_start = small_tup[0]
        sm_end = small_tup[1] + sm_start
        bg_start = big_tup[0]
        bg_end = big_tup[1] + bg_start

        small = xs[sm_start:sm_end]
        big = xs[bg_start:bg_end]

        fbins = yield from binary_search(xs, bg_start, sm_start, sm_end - 1, 'Merging runs')
        fbins -= sm_start
        lsinb = yield from binary_search(xs, sm_end - 1, bg_start, bg_end - 1, 'Merging runs')
        lsinb -= bg_start
        temp = small[fbins:].copy()
        i = 0
        j = 0
        idx = fbins
        consec_sm = 0
        consec_bg = 0
        while i < len(temp) and j <= min(lsinb, len(big) - 1):
            if consec_bg >= gallop_threshold:
                nxtsinb = yield from gallop(xs, sm_start + fbins + i, bg_start + j, bg_end)
                copy = nxtsinb - (bg_start + j)
                space = max(0, len(small) - idx)
                if space > 0:
                    if copy > space:
                        small[idx:] = big[j:j + space]
                        big[0:copy - space] = big[j + space:j + copy]
                    else:
                        small[idx:idx + copy] = big[j:j + copy]
                else:
                    big[idx - len(small):idx - len(small) + copy] = big[j:j + copy]
                idx += copy
                j += copy
                consec_bg = 0
                continue
            if consec_sm >= gallop_threshold:
                nxtbins = yield from gallop(xs, bg_start + j, sm_start + fbins + i, sm_end)
                copy = nxtbins - (sm_start + fbins + i)
                space = max(0, len(small) - idx)
                if space > 0:
                    if copy > space:
                        small[idx:] = temp[i:i + space]
                        big[0:copy - space] = temp[i + space:i + copy]
                    else:
                        small[idx:idx + copy] = temp[i:i + copy]
                else:
                    big[idx - len(small):idx - len(small) + copy] = temp[i:i + copy]
                idx += copy
                i += copy
                consec_sm = 0
                continue
            yield xs + ['Merging runs', [bg_start + j, sm_start + fbins + i]]
            if big[j] < temp[i]:
                consec_bg += 1
                consec_sm = 0
                if idx >= len(small):
                    big[idx - len(small)] = big[j]
                else:
                    small[idx] = big[j]
                j += 1
            else: # if temp[i] <= big[j]; i believe this is how timsort maintains stability?
                consec_bg = 0
                consec_sm += 1
                if idx >= len(small):
                    big[idx - len(small)] = temp[i]
                else:
                    small[idx] = temp[i]
                i += 1
            idx += 1
        if i < len(temp):
            big[-(len(temp) - i):] = temp[i:]
        xs_idx = min(small_tup[0], big_tup[0])
        for val in small + big:
            xs[xs_idx] = val
            yield xs + ['Merging runs', [xs_idx]]
            xs_idx += 1

    minrun = find_minrun()
    stack = list()
    # here we go
    idx = 0
    while idx < len(xs):
        len_run = yield from count_run(xs, idx)
        if len_run < minrun:
            xs = yield from bin_ins_sort(xs, idx, min(idx + minrun, len(xs)), idx + len_run)
            len_run = min(minrun, len(xs) - idx)
        stack.append((idx, len_run))
        idx += len_run
        yield from merge_collapse(xs, stack)
    while len(stack) > 1:
        a = stack.pop()
        b = stack.pop()
        start = min(a[0], b[0])
        yield from merge(xs, a, b)
        stack.append((start, a[1] + b[1]))
    yield xs + ['', []]