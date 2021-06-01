import time

class Sorter:
    @staticmethod
    def selection(data, pivot, order):
        pivot = int(pivot)
        extreme = lambda array, order : min(array) if order == "ASC" else max(array)

        start = time.time_ns()
        keys = []
        for d in data:
            keys.append(d[pivot])
        
        n = len(data)
        for i in range(1, n - 1):
            extreme_value = extreme(keys[i:], order)
            j = keys.index(extreme_value, i, n - 1)
            data[i], data[j] = data[j], data[i]
            keys[i], keys[j] = keys[j], keys[i]

        end = time.time_ns()
        exec_time = (end - start)
        
        return (data, exec_time)

    @staticmethod
    def merger(data, left, mid, right, comparator, pivot):
        result = []
        for isi in data:
            result.append(isi)
            
        p = left
        q = mid + 1
        r = left
        while(p <= mid) and (q <= right):
            if(comparator(data[p], data[q], pivot)):
                result[r] = data[p]
                p += 1
            else:
                result[r] = data[q]
                q += 1

            r += 1

        while(p <= mid):
            result[r] = data[p]
            p += 1
            r += 1

        while(q <= right):
            result[r] = data[q]
            q += 1
            r += 1

        return result

    @staticmethod
    def merge(data, pivot, order):
        pivot = int(pivot)
        compare = lambda a, b, pivot : (a[pivot] < b[pivot] if order == "ASC" else a[pivot] >= b[pivot])
        start = time.time_ns()
        data = Sorter.merge(data, 1, len(data) - 1, compare)
        end = time.time_ns()

        exec_time = (end - start)
        return (data, exec_time)

    @staticmethod
    def merge(data, left, right, comparator, pivot):
        if(left < right):
            mid = (left + right) // 2
            data = Sorter.merge(data, left, mid, comparator, pivot)
            data = Sorter.merge(data, mid + 1, right, comparator, pivot)
            data = Sorter.merger(data, left, mid, right, comparator, pivot)
        return data

    @staticmethod
    def bubble(data, pivot, order):
        pivot = int(pivot)
        compare = lambda a, b, pivot: (a[pivot] < b[pivot] if order == "ASC" else a[pivot] >= b[pivot])
        start = time.time_ns()
        n = len(data)
        for i in range(1, n):
            for j in range(1, n - i):
                if compare(data[j - 1], data[j], pivot):
                    continue
                (data[j - 1], data[j]) = (data[j], data[j - 1])

        end = time.time_ns()

        exec_time = (end - start)
        
        return (data, exec_time)