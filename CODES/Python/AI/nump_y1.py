import numpy as np

arr = np.arange(1, 13)  
print("Original array:", arr) 

reshaped_arr = arr.reshape(3,4) 
print("Reshaped to 3x4:\n", reshaped_arr) 
print("First row:", reshaped_arr[0]) 
print("Second column:", reshaped_arr[:,1]) 