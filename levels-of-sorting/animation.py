import random
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sorts import *
from introsort import *
from timsort import *
from sound import *

matplotlib.rcParams['toolbar'] = 'None'
matplotlib.use('TkAgg')

def generate_numbers(n, seed=True):
    if seed:
        random.seed(0)
    numbers = list(range(1, n + 1))
    random.shuffle(numbers)
    return numbers


def animate(algorithm, n, interval=1, seed=True, *args, **kwargs):

    # C_MAJOR = ('c', 'd', 'e', 'f', 'g', 'a', 'b')
    CHROMATIC_C = ('c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b')

    xs = generate_numbers(n)
    title = algorithm.__name__.replace('_', ' ').title()
    generator = algorithm(xs, **kwargs)

    fig, ax = plt.subplots(figsize=(25, 16))
    fig.suptitle(title, y=0.94, color='white', fontsize=48)
    fig.text(x=0.5, y=0.84, s=get_desc(algorithm), color='white', fontsize=28, ha='center')
    bars = ax.bar(range(len(xs)), xs, align='edge', color='#01b8c6')
    text = fig.text(0.075, 0.84, '', color='white', fontsize=28, ha='left')
    ax.axis('off')
    ax.set_position(matplotlib.transforms.Bbox([[0.075,0.1],[0.925,0.82]]))
    fig.patch.set_facecolor('#151231')

    runtime = get_runtime(algorithm)
    comparisons = 0
    frame_num = 0
    sounds = list()

    def update_fig(xs, rects, runtime):

        nonlocal comparisons
        nonlocal frame_num

        if len(xs[-1]) == 2:
            comparisons += 1

        next_sound_chunk = 0

        for i, tup in enumerate(zip(rects, xs)):
            rect, val = tup
            rect.set_height(val)
            
            if i in xs[-1]:
                rect.set_color('#f79ce7')
                octave = 2 + (val - 1) // len(CHROMATIC_C)
                note = CHROMATIC_C[(val - 1) % len(CHROMATIC_C)]
                next_sound_chunk += plucknote1(Note(note, octave), 0.4)

            else:
                rect.set_color('#01b8c6')
        
        sounds.append(next_sound_chunk)

        if frame_num > 20:
            text.set_text(runtime + f'{comparisons} comparisons\n{xs[-2]}')
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
            stream.write(sounds[frame_num - 1].astype(numpy.float32).tostring())
            stream.close()
            p.terminate()
        else :
            text.set_text(runtime + f'{comparisons} comparisons\n')

        frame_num += 1


    anim = animation.FuncAnimation(fig, func=update_fig, fargs=(bars, runtime),
        frames=generator, interval=interval, repeat=False, cache_frame_data=False)

    manager = plt.get_current_fig_manager()
    manager.window.wm_geometry("+0+0")

    plt.show()


def get_desc(algorithm):
    name = algorithm.__name__
    result = ''
    if name == 'bubble_sort':
        result += 'swaps adjacent out-of-order elements'
    elif name == 'selection_sort':
        result += 'finds next smallest element'
    elif name == 'insertion_sort':
        result += 'inserts next element into place'
    elif name == 'merge_sort':
        result += 'divides list and merges pieces'
    elif name == 'quicksort':
        result += 'swaps elements around a pivot'
    elif name == 'heapsort':
        result += 'Selection sort with a heap'
    elif name == 'introsort':
        result += 'hybrid Insertion/Quicksort/Heapsort'
    elif name == 'timsort':
        result += 'hybrid Insertion/Merge sort'
    return result

def get_runtime(algorithm):
    name = algorithm.__name__
    result = ''
    if name == 'bubble_sort':
        #result += 'Bubble sort swaps adjacent out-of-order elements\n\n'
        result += 'Runtime: $\mathregular{O(n^2)}$\n'
    elif name == 'selection_sort':
        #result += 'Selection sort finds and puts the next smallest element into place\n\n'
        result += 'Runtime: $\mathregular{O(n^2)}$\n'
    elif name == 'insertion_sort':
        #result += 'Insertion sort inserts the next element into place\n\n'
        result += 'Runtime: $\mathregular{O(n^2)}$\n'
    elif name == 'merge_sort':
        #result += 'Mergesort divides the list and merges the pieces\n\n'
        result += 'Runtime: O(nlogn)\n'
    elif name == 'quicksort':
        #result += 'Quicksort recursively swaps elements around a pivot\n\n'
        result += 'Expected Runtime: O(nlogn)\n'
    elif name == 'heapsort':
        #result += 'Heapsort is Selection sort using a heap\n\n'
        result += 'Runtime: O(nlogn)\n'
    elif name == 'introsort':
        #result += 'Introsort is a hybrid of Insertion sort, Quicksort, and Heapsort\n\n'
        result += 'Runtime: O(nlogn)\n'
    elif name == 'timsort':
        #result += 'Timsort is a hybrid of Insertion sort and Merge sort\n\n'
        result += 'Runtime: O(nlogn)\n'
    return result