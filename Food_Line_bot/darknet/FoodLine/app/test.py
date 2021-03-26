resultvx = "apple、apple、apple、tofu pudding、tofu pudding"
jobs = resultvx.split('、')



set = set(jobs)
dict = {}
for item in set:
    dict.update({item: jobs.count(item)})

print (dict)


import string
# str = 'eat/apple/tangyuan'
# print(str)
# #输出：abcde
#
# list1 = list(str)
# print(list1)
# #输出：['a', 'b', 'c', 'd', 'e']


# resultvx = "apple/apple/apple"
# wordlist = resultvx.split('/')
# print (wordlist[0])
