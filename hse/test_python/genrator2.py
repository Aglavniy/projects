
def subsets(lst):

    for i in range(len(lst)):
        
        while len(lst) - len(lst[:i+1]) >= 2:
            for num in lst[i+2:]:
                answer = [*lst[:i+1], num]
                yield answer


        yield lst[:i+1]

    try:
        for subset in subsets(lst[1:]):
            yield subset
    except:
        yield []


lst = [1, 2, 3,4]
k = 0
for subset in subsets(lst):  
    k+=1
    print(subset)
print(k)