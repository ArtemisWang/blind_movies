import pickle
import numpy as np
with open('data/acc_bow3.pkl', 'rb') as f:
    model = pickle.load(f)
    data_bow = model['acc_list']
    # print(data_bow)

with open('data/acc_cnn3.pkl', 'rb') as f:
    model = pickle.load(f)
    data_cnn = model['acc_list']
    # print(data_cnn)

with open('data/acc_grnn3.pkl', 'rb') as f:
    model = pickle.load(f)
    data_grnn = model['acc_list']

x, y, z = [], [], []
for i, data_i in enumerate(data_cnn):
    x.append(np.argmax(data_bow[i]))
    y.append(np.argmax(data_cnn[i]))
    z.append(np.argmax(data_grnn[i]))


# x = [6, 6, 1, 0, 6, 0, 0, 1, 8, 5, 0, 3, 3, 4, 1, 6, 2, 10, 11, 7, 8, 2, 8, 12, 10, 1, 14]
# y = [20, 12, 3, 4, 2, 5, 6, 7, 8, 9, 11, 10, 10, 11, 13, 12, 4, 13, 16, 15, 15, 23, 15, 19, 20, 1, 23]
# z = [2, 1, 3, 4, 2, 5, 6, 7, 8, 18, 11, 10, 10, 13, 14, 12, 4, 14, 14, 14, 15, 23, 14, 1, 21, 22, 23]


def anyIdentical(list0, list1, list2):  ## 首先将三个列表中两个及以上相同的值作为最终的结果，将列表中其他的值置为-1
    rank = []
    if len(list0) == len(list1) == len(list2):
        for i in range(len(list1)):
            if list0[i] == list1[i] or list0[i] == list2[i]:
                rank.append(list0[i])
            elif list1[i] == list2[i]:
                rank.append(list1[i])
            else:
                rank.append(-1)
    else:
        print("列表范围不对应")
    return rank


rank = anyIdentical(x, y, z)
# print(len(rank))
# print(rank)
# [-1, -1, 3, 4, 2, 5, 6, 7, 8, -1, 11, 10, 10, 11, -1, 12, 4, 13, -1, 14, 15, 23, 15, 19, 21, -1, 23]

# while i < len(rank)-1:
#     if rank[i] == -1:
#         rank[i] = 0
#     if i == 0:
#         rank[i] = int((sum(rank[0:4])) / 4)
#     if i >= 1:
#         if rank[i] >= rank[i-1] and rank[i-1] <= rank[i+1]:
#             if rank[i] > rank[i+1]:
#                 rank[i] = int((rank[i - 1] + rank[i + 1]) / 2)
#             else:
#                 pass
#         else:
#             if rank[i] == 0:
#                 rank[i] = int((rank[i - 1] + rank[i + 1]) / 2)
#
#     i += 1


def modifiedRank(rank):  ## 修正列表，将列表中为-1的值改成一个符合要求的值，预测值，该值大于等于前后两个值的平均值
    i = 0
    while i < len(rank) - 1:
        if rank[i] == -1:
            rank[i] = 0
        if i == 0 and rank[i] == 0:
            rank[i] = int((sum(rank[0:4])) / 4)
        if i >= 1:
            if rank[i - 1] <= rank[i + 1]:
                if rank[i] >= rank[i - 1] and rank[i] <= rank[i + 1]:
                    pass
                else:
                    rank[i] = int((rank[i - 1] + rank[i + 1]) / 2)
            else:
                if rank[i] >= rank[i - 1]:
                    pass
                else:
                    rank[i] = rank[i - 1]
        i += 1
    return rank


modi_rank = modifiedRank(rank)
# print(len(modi_rank))
# print(modi_rank)
# [1, 2, 3, 4, 4, 5, 6, 7, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 15, 15, 15, 19, 21, 22, 23]

def continueRank(rank): ## 处理列表中的重复的值，例如[15,15,15,15,19]改写成为[]15,16,17,18,19]
    j = 0
    i_list = [] ## 存储重复值的索引值
    for i in range(len(rank)-1):
        if i in i_list:
            break
        while rank[i] == rank[i+1]:
            i_list.append(i)
            j += 1
            i += 1
        if j >= 2:
            if rank[i+1]-rank[i] < j:  ## 重复的值的数量大于前后两个值之间的差值，还需要保留一些重复的值
                j = rank[i+1]-rank[i]
            while rank[i+1]-rank[i] >= j and j > 0:
                rank[i-j+1] = rank[i-j]+1
                j -= 1
            # print(i, j)  ## 几个连续值的最后一个数的索引值i，测试中为22，对应三个连续的15的最后一个15的索引值
        # print(rank)
        j = 0
    return rank

rank_rank = continueRank(rank)
# print(len(rank_rank))
# print(rank_rank)
# [1, 2, 3, 4, 4, 5, 6, 7, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 15, 16, 17, 19, 21, 22, 23]