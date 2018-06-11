"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """    
    "*** YOUR CODE HERE ***"   
    #initialize cost list which will contain each cost of every fruitshop 
    cost = []        
    #the number of fruitshops
    n = len(fruitShops)
    for i in range(n):            
        #calculate how much will this order cost in each fruitshop
        each_cost = fruitShops[i].getPriceOfOrder(orderList)
        cost.append(each_cost)          
                
    #find the least cost of all the fruitshops    
    minimum_cost = min(cost)
              
    #know which this fruitshop is
    best_shop_index = cost.index(minimum_cost) 
                  
    #return the name of this fruitshop
    return fruitShops[best_shop_index]
    
def shopArbitrage(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        maximum profit in amount
    """
    "*** YOUR CODE HERE ***"
              
    #the number of the kinds of fruit in the orderlist
    m = len(orderList)         
    #the number of fruitshops 
    n = len(fruitShops)          
    #initialize maximum profit with 0
    maximum_profit = 0
    for i in range(m):           
        #warning: if this list is outside first for loop this will be wrong
        cost = []
        for j in range(n):           
            #extract every single kind of fruit in the orderlist
            same_fruit_order = [orderList[i]]          
            #calculate how much this kind of furit will cost in each fruitshop
            cost_element = fruitShops[j].getPriceOfOrder(same_fruit_order) 
            cost.append(cost_element)
                  
        #the maximum profit is the difference between the highest and lowest cost
        maximum_profit = max(cost) - min(cost) + maximum_profit 
    return maximum_profit

def shopMinimum(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        Minimun cost of buying the fruits in orderList
    """
    "*** YOUR CODE HERE ***"
    #the number of the kinds of fruit in the orderlist
    m = len(orderList)
    #the number of fruitshops
    n = len(fruitShops) 
    #initialize the minimum cost with 0
    minimum_cost = 0
    for i in range(m):
        cost = []           
        #if this list is outside first for loop this will be wrong
        for j in range(n):
            #convert the ith element of orderList to list, because the input of getPriceOfOrder must be a list
            same_fruit_order = [orderList[i]]
            #calculate how much this kind of furit will cost in each fruitshop
            cost_element = fruitShops[j].getPriceOfOrder(same_fruit_order)
            cost.append(cost_element)
        #sum every minimum cost of all kinds of fruit together  
        minimum_cost = min(cost) + minimum_cost
    return minimum_cost


if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
  orders = [('apples',3.0)]
  print("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())
