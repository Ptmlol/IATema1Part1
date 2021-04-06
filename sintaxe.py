# import numpy as np
#
# to_matrix = np.array([[1, 2, 12, 11],
#                       [8, 5, 6, 12],
#                       [7, 15, 12, 13],
#                       [14, 15, 16, 0]])
# if int(to_matrix[-1][-1]) == 0:
#     for i in range(0, len(to_matrix)):
#         for j in range(0, len(to_matrix)):
#             if not i == j == len(to_matrix) - 1 and not i == j == 0:
#                 if i == 0 and j >= 1:
#                     if int(to_matrix[i][j - 1]) <= int(to_matrix[i][j]):
#                         pass
#                     else:
#                         print("NU")
#                         break
#                 if i >= 1 and j == 0:
#                     if int(to_matrix[i - 1][j]) <= int(to_matrix[i][j]):
#                         pass
#                     else:
#                         print("NU")
#                         break
#                 if i >= 1 and j >= 1:
#                     if int(to_matrix[i - 1][j]) <= int(to_matrix[i][j]) and int(to_matrix[i][j - 1]) <= int(to_matrix[i][j]):
#                         pass
#                     else:
#                         print("NU")
#                         break
#     print("DA")
matrix = [[0 for x in range(3)] for y in range(3)]
for i in range(3):
    for j in range(3):
        matrix[i][j] = 1

print(matrix)