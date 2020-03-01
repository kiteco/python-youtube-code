a_list = [4, 1, 5, 3, 2]

def selectionsort(unsorted_list):
  print(unsorted_list)
  for i in range(len(unsorted_list)):
    smallest_index = i
    for j in range(i + 1, len(unsorted_list)):
      if unsorted_list[j] < unsorted_list[smallest_index]:
        smallest_index = j
    unsorted_list[smallest_index], unsorted_list[i] = unsorted_list[i], unsorted_list[smallest_index]
  print(unsorted_list)


selectionsort(a_list)