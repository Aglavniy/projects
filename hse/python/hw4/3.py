a = [[2, 2, 2], 
     [1, 1, 1]]
b = [[4, 5], 
     [3, 5],
     [1,2]]

result = [[sum(x * y for x, y in zip(row_a, col_b)) for col_b in zip(*b)] for row_a in a]

print(result)