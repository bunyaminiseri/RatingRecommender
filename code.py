#!/usr/bin/python

def main():
	result = open("result.txt","w+")
	source  = open('train_all_txt.txt', 'r')
	source2  = open('output.txt', 'r')
	result_matrix = open("result_matrix.txt","w+")

	row = 943 #amount of users
	column = 1682 # amount of items

	avg_array = [0] * column #create array for keeping average of rating for each item


	matrix = [0] * row #rating matrix to make calculations
	for i in range(row):
	    matrix[i] = [0] * column

	matrix2 = [0] * row #rating matrix
	for i in range(row):
	    matrix2[i] = [0] * column

	matrix3 = [0] * row #rating matrix
	for i in range(row):
	    matrix3[i] = [0] * column     

	w_matrix = [0] * column #item weight matrix size = 1682x1682. The matrix keeps between pair of items to make item-to-item search
	for i in range(column):
	    w_matrix[i] = [0] * column

	lines = source.readlines()
	for line in lines: #read data from training data and put them into rating matrix
		line = line.replace('\n','')
		mylist = line.split(" ")
		matrix[int(mylist[0])-1][int(mylist[1])-1] = int(mylist[2])
		matrix3[int(mylist[0])-1][int(mylist[1])-1] = int(mylist[2])

	lines2 = source2.readlines()
	for line in lines2: #read data from training data and put them into rating matrix
		line = line.replace('\n','')
		mylist = line.split(" ")
		matrix2[int(mylist[0])-1][int(mylist[1])-1] = float(mylist[2])

	for j in range (column): #calculating and filling average array for item ratings
		avg_count = 0
		for i in range (row):
			avg_array[j] += matrix[i][j]
			if (matrix[i][j]!=0):
				avg_count += 1

		if (avg_count==0):
			avg_count=1

		avg_array[j] = avg_array[j] / avg_count

	print(len(avg_array))


	for i in range(column): #finding weights between pair of items
		for j in range (column):
			if (i!=j and w_matrix[i][j]==0): #items will not have weight with themselves so it calculates only if i!=j and weight(i,j)=0
				avg_i = 0
				avg_j = 0
				count_i = 0
				count_j = 0
				weight = 0
				a = 0 #upper part of division in 
				b = 0 #lower left part of division
				c = 0 #lower right part of division
				user_list = []
				for k in range (row):
					if(matrix[k][i]!=0):
						avg_i += matrix[k][i]
						count_i += 1
					if(matrix[k][j]!=0):
						avg_j += matrix[k][j]
						count_j += 1
					if (matrix[k][i]!=0 and matrix[k][j]!=0): #if the user has rating for both items i and j, add them to the list
						user_list.append(k)
				if(count_i==0):
					count_i += 1
				if(count_j==0):
					count_j += 1
				avg_i = avg_i / count_i
				avg_j = avg_j / count_j
				for m in range(len(user_list)):
					a += (matrix[user_list[m]][i] - avg_i) * (matrix[user_list[m]][j] - avg_j)
					b += (matrix[user_list[m]][i] - avg_i) * (matrix[user_list[m]][i] - avg_i)
					c += (matrix[user_list[m]][j] - avg_j) * (matrix[user_list[m]][j] - avg_j)
					if (b == 0):
						b += 1
					if (c == 0):
						c +=1
					weight = a / ((b*c) ** (0.5))
					#print (weight)
					w_matrix[i][j] = weight
					w_matrix[j][i] = weight
					#weight_array[i] += weight
					#weight_array_absolute[i] += abs(weight)

	#making predictions for zero values in dataset
	for i in range (row):
		for j in range (column):
			a = 0 #upper part of division
			b = 0 #lower part of division
			if(matrix[i][j]==0):
				for k in range (column):
					a += w_matrix[j][k] * matrix[i][k]
					b += abs(w_matrix[j][k])
				if(b==0):
					b=1
				matrix[i][j] = avg_array[j] + (a / b)
				if(matrix[i][j]<1):
					matrix[i][j] = 1
				if(matrix[i][j]>5):
					matrix[i][j] = 5

	for i in range (row):
		for j in range (column):
			if(matrix3[i][j]==0):
				matrix[i][j] = (matrix[i][j] + matrix2[i][j]) / 2

	#print out the result output and result matrix to check
	for i in range(1, row+1):
	     	for j in range(1, column+1):
	     		result.write("%d %d %.2f\n" % (i,j,matrix [i-1][j-1]))
	     		result_matrix.write("%.2f" % (matrix[i-1][j-1]))
	     		result_matrix.write(" ")
		result_matrix.write("\n")

	result.close()
	result_matrix.close()
	source.close()


main()