# There are two orientations of the sorting algorithm : Ascending and Descending
# The orientation of sorting is based on user's input
def selection_sort(l, orientation):
    if orientation == 'ascending':
        for i in range (len(l)):
            idx_min = i
            for j in range (i+1, len(l)):
                if l[j] < l[idx_min]:
                    idx_min = j
            l[i], l[idx_min] = l[idx_min], l[i]
    elif orientation == 'descending':
        for i in range (len(l)):
            idx_min = i
            for j in range (i+1, len(l)):
                if l[j] > l[idx_min]:
                    idx_min = j
            l[i], l[idx_min] = l[idx_min], l[i]
    return l

def bubble_sort(l, orientation):
    if orientation == 'ascending':
        for i in range (len(l)):
            for j in range (len(l)-i-1):
                if l[j+1] < l[j]:
                    l[j], l[j+1] = l[j+1], l[j]
    elif orientation == 'descending':
        for i in range (len(l)):
            for j in range (len(l)-i-1):
                if l[j+1] > l[j]:
                    l[j], l[j+1] = l[j+1], l[j]
    return l

def merge_sort(l, orientation):
    if orientation == 'ascending':
        if len(l) > 1:
            mid = len(l)//2
            left = l[:mid]
            right = l[mid:]
            merge_sort(left, orientation)
            merge_sort(right, orientation)

            i = j = k = 0

            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    l[k] = left[i]
                    i += 1
                else:
                    l[k] = right[j]
                    j += 1
                k += 1
            
            while i < len(left):
                l[k] = left[i]
                i += 1
                k += 1
            
            while j < len(right):
                l[k] = right[j]
                j += 1
                k += 1
        return l
    elif orientation == 'descending':
        if len(l) > 1:
            mid = len(l)//2
            left = l[:mid]
            right = l[mid:]
            merge_sort(left, orientation)
            merge_sort(right, orientation)

            i = j = k = 0

            while i < len(left) and j < len(right):
                if left[i] > right[j]:
                    l[k] = left[i]
                    i += 1
                else:
                    l[k] = right[j]
                    j += 1
                k += 1
            
            while i < len(left):
                l[k] = left[i]
                i += 1
                k += 1
            
            while j < len(right):
                l[k] = right[j]
                j += 1
                k += 1
        return l
