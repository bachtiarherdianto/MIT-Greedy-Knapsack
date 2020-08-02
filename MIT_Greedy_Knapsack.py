# class Food(object):
#     def __init__(self, n, v, w):
#         self.single_name = n
#         self.single_value = v
#         self.calories = w
#     def GetValue(self):
#         return self.single_value
#     def GetCost(self):
#         return self.calories
#     def Density(self):
#         return self.GetValue() / self.GetCost()
#     def __str__(self):
#         return str(self.single_name)+ ': (' +str(self.single_value)+ ', ' +str(self.calories)+ ')'
#
# def BuildMenu(GroupName, GroupValue, calories):
#     ''' names, values, calories lists of same length. name a list of strings, values and calories lists
#         of numbers return list of Foods'''
#     menu = []
#     for i in range(len(GroupValue)):
#         menu.append(Food(GroupName[i], GroupValue[i], calories[i]))
#     return menu
#
# def Main(items, maxCost, keyFunction):
#     ''' Assumes items a list, maxCost >= 0, keyFunction maps elements of items to numbers'''
#     itemsCopy = sorted(items, key=keyFunction, reverse=True)
#     result = []
#     totalValue, totalCost = 0.0, 0.0
#     for i in range(len(itemsCopy)):
#         if (totalCost + itemsCopy[i].GetCost()) <= maxCost:
#             result.append(itemsCopy[i])
#             totalCost += itemsCopy[i].GetCost()
#             totalValue += itemsCopy[i].GetValue()
#     return (result, totalValue)
#
# def Helper(items, constraint, keyFunction):
#     taken, val = Main(items, constraint, keyFunction)
#     print('Total value of items taken is ', val, '\nFood: (values, calories)')
#     for single_item in taken:
#         print(single_item)
#
# def Greedy(SingleFood, maxUnits):
#     print('Use Greedy by value to allocate', maxUnits, 'calories')
#     Helper(SingleFood, maxUnits, Food.GetValue)
#     print('\nUse Greedy by cost to allocate', maxUnits, 'calories')
#     Helper(SingleFood, maxUnits, lambda x: 1 / Food.GetCost(x))
#     print('\nUse Greedy by density to allocate', maxUnits, 'calories')
#     Helper(SingleFood, maxUnits, Food.Density)
#
# def maxVal (toConsider, avail):
#     ''' Assumes toConsider a list of items, avail a weigh
#         Returns a tuple of the total value of a solution to
#         the 0/1 knapsack problem and the items of that solution'''
#     if toConsider == [] or avail == 0:
#         result = (0, ())
#     elif toConsider[0].GetCost() > avail:
#         result = maxVal(toConsider[1:], avail)
#     else:
#         nextItem = toConsider[0]
#         withVal, withToTake = maxVal(toConsider[1:],
#                                      avail - nextItem.GetCost())
#         withVal += nextItem.GetValue()
#         withoutVal, withoutTake = maxVal(toConsider[1:], avail)
#         if withVal > withoutVal:
#             result = (withVal, withToTake + (nextItem,))
#         else:
#             result = (withoutVal, withoutTake)
#     return result
#
# def FastMaxVal(toConsider, avail, memo= {}):
#     """ Assumes toConsider a list of subjects, avail a weight
#         memo supplied by recursive calls
#         Returns a tuple of the total value of a solution to
#         the 0/1 knapsack problem and the subjects of that solution"""
#     if (len(toConsider), avail) in memo:
#         result = memo[len(toConsider), avail]
#     elif toConsider == [] or avail == 0:
#         result = (0, ())
#     elif toConsider[0].GetCost() > avail:           # Explore right branch only
#         result = FastMaxVal(toConsider[1:], avail, memo)
#     else:
#         NextItem = toConsider[0]                    # Explore left branch
#         withVal, withToTake = FastMaxVal(toConsider[1:], avail-NextItem.GetCost(), memo)
#         withVal += NextItem.GetValue()              # Explore right baranch
#         withoutVal, withoutToTake = FastMaxVal(toConsider[1:], avail, memo)
#         if withVal > withoutVal:
#             result = (withVal, withToTake + (NextItem,))
#         else:
#             result = (withoutVal, withoutToTake)
#     memo[(len(toConsider), avail)] = result
#     return result
#
# def TestMaxVal (foods, maxUnits, algorithm, printItems= True):
#     print('Menu contains', len(foods), 'items')
#     print('Use search tree to allocate', maxUnits, 'calories')
#     val, taken = algorithm(foods, maxUnits)
#     if printItems:
#         print('Total value of items taken=', val)
#         for item in taken:
#             print('  ', item)
#
# # '''Test Greedy Algorithm
# #    to optimize Knapsack's Problem'''
# # names, values, calories = ['I0', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7'], \
# #                           [89  , 90  , 95  , 100 , 90  , 79  , 50  , 10  ], \
# #                           [123 , 154 , 258 , 354 , 365 , 150 , 95  , 195 ]
# #
# # # print(Food(names, values, calories)) # to check Food object
# # GroupFoods = BuildMenu(names, values, calories)
# # Greedy(GroupFoods, 600)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import random

def BuildLargeMenu(numItems, maxVal, maxCost):
    items = []
    for i in range(numItems):
        items.append(Food(str(i),
                          random.randint(1, maxVal),
                          random.randint(1, maxCost)))
    return items  # to return large list of food

for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50):
    items = BuildLargeMenu (numItems, 90, 250)
    print('Test with function maxVal')  # to compare between maxFal and FastMaxVal
    TestMaxVal(items, 750, maxVal, True)
    print('Test with function FastMaxVal') # using principle of Dynamic programming
    TestMaxVal(items, 750, FastMaxVal, True)
