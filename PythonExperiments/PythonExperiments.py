
class ModArrayMapper:

    def __init__(self, array, mod, rem):
        self.array = array
        self.mod = mod
        self.rem = rem         

    def __iter__(self):
        for i in range(len(self.array)):
            if i % self.mod == self.rem:
                yield self.array[i]

class ArrayMerger:
    def __init__(self, array_list):
        self.array_list = array_list
        self.length = max(map(len, self.array_list))

    def __iter__(self):
        item_index = 0
        for i in range(self.length):
            for array in self.array_list:
                if len(array) > item_index:
                    yield array[item_index]
            item_index += 1


arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(arr)

mapper_even = ModArrayMapper(arr, 2, 0)
mapper_odd = ModArrayMapper(arr, 2, 1)

even = sorted(mapper_even)
odd = sorted(mapper_odd, reverse=True)

print(even)
print(odd)

merger = ArrayMerger([even, odd])
print(list(merger))