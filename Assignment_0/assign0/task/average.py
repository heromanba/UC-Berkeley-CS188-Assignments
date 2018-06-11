
"""
Run python autograder.py 
"""

def average(priceList):
    "Return the average price of a set of fruit"
    "*** YOUR CODE HERE ***"
    #use set to store unique and remove redundant element
    priceSet = set(priceList)
    sum = 0
    #in case sum/0 happens 
    if len(priceSet) > 0:
        #calculate sum of all elements in priceSet
        for i in priceSet:
            sum = sum + i
        print("The average of Price is: ", sum/len(priceSet))
    else:
        print("The priceList is empty")
    return sum/len(priceSet)
