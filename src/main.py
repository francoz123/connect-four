from  functions import horizontals, right_diagonals, left_diagonals
a = [[1,0,0,1,0,0,0],
     [1,0,0,0,1,0,0],
     [1,0,1,1,0,0,1],
     [1,0,0,1,0,0,1],
     [0,1,1,0,0,0,0],
     [1,0,0,0,0,1,0]
    ]
for row in range(len(a)):
    print(row, a[row])
#print(horizontals(a, 1))
#print('right',right_diagonals(a, 1))
print('left',left_diagonals(a, 1))
