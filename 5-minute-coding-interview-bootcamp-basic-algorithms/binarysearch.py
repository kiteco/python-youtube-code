a_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def binarysearch(list, value, left_edge, right_edge): 
  if left_edge <= right_edge:
    middle = left_edge + (right_edge - 1) // 2
    if list[middle] == value:
      return middle
    elif list[middle] < value:
      return binarysearch(list, value, middle + 1, right_edge)
    else:
      return binarysearch(list, value, left_edge, middle - 1)
    
  return -1

print(binarysearch(a_list, 5, 0, len(a_list)))