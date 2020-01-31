
# importing the required module 
import matplotlib as mt
  
# x axis values 
x = [1,2,3] 
# corresponding y axis values 
y = [2,4,1] 
  
# plotting the points  
mt.pyplot.plot(x, y) 
  
# naming the x axis 
mt.pyplot.xlabel('x - axis') 
# naming the y axis 
mt.pyplot.ylabel('y - axis') 
  
# giving a title to my graph 
mt.pyplot.title('My first graph!') 
  
# function to show the plot 
mt.pyplot.show() 
