def selection_sort(l, orientation):
    l1 = l[1:]
    if orientation == 'ascending':
        for i in range (len(l1)):
            idx_min = i
            for j in range (i+1, len(l1)):
                if l1[j] < l1[idx_min]:
                    idx_min = j
            l1[i], l1[idx_min] = l1[idx_min], l1[i]
    elif orientation == 'descending':
        for i in range (len(l1)):
            idx_min = i
            for j in range (i+1, len(l1)):
                if l1[j] > l1[idx_min]:
                    idx_min = j
            l1[i], l1[idx_min] = l1[idx_min], l1[i]
    l1.insert(0,l[0])
    return l1

def bubble_sort(l, orientation):
    l1 = l[1:]
    if orientation == 'ascending':
        for i in range (len(l1)):
            for j in range (len(l1)-i-1):
                if l1[j+1] < l1[j]:
                    l1[j], l1[j+1] = l1[j+1], l1[j]
    elif orientation == 'descending':
        for i in range (len(l1)):
            for j in range (len(l1)-i-1):
                if l1[j+1] > l1[j]:
                    l1[j], l1[j+1] = l1[j+1], l1[j]
    l1.insert(0,l[0])
    return l1

def insertion_sort(l, orientation):
    l1 = l[1:]
    if orientation == 'ascending':
        for i in range (1, len(l1)):
            key = l1[i]
            j = i-1
            while j >= 0 and key < l1[j]:
                l1[j+1] = l1[j]
                j -= 1
            l1[j+1] = key

def merge_sort(l, orientation):
    l1 = l[1:]
    if orientation == 'ascending':
        if len(l1) > 1:
            mid = len(l1)//2
            left = l1[:mid]
            right = l1[mid:]
            merge_sort(left, orientation)
            merge_sort(right, orientation)

            i = j = k = 0

            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    l1[k] = left[i]
                    i += 1
                else:
                    l1[k] = right[j]
                    j += 1
                k += 1
            
            while i < len(left):
                l1[k] = left[i]
                i += 1
                k += 1
            
            while j < len(right):
                l1[k] = right[j]
                j += 1
                k += 1
        l1.insert(0,l[0])
        return l1
    elif orientation == 'descending':
        if len(l1) > 1:
            mid = len(l1)//2
            left = l1[:mid]
            right = l1[mid:]
            merge_sort(left, orientation)
            merge_sort(right, orientation)

            i = j = k = 0

            while i < len(left) and j < len(right):
                if left[i] > right[j]:
                    l1[k] = left[i]
                    i += 1
                else:
                    l1[k] = right[j]
                    j += 1
                k += 1
            
            while i < len(left):
                l1[k] = left[i]
                i += 1
                k += 1
            
            while j < len(right):
                l1[k] = right[j]
                j += 1
                k += 1
        l1.insert(0,l[0])
        return l1
