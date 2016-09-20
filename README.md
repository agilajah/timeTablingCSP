# timeTablingCSP

IF3170 Artificial Intelligence Course Project.

Create Course Timetabling Application using CSP's Algorithms :
  1. Hill Climbing Algorithm
  2. Simulated Annealing
  3. Genetic Algorithm
  
Identifying Problem Component :
  1. Variables
		The variables of this problem is 
			s(h,j), the position of values that will be assigned
			where h is the day representations (1 = Monday, 2 = Tuesday, and so on)
  2. Domains
		a. MK -> key by Course_Id & Course_No
		b. R -> key by Room_Name & MK
  3. Constraints
		a. h >= 1 && h <= 5
		b. j >= 7 && j <= 17
		c. MK1#h,j != MK2#h,j
		d. R.MK1 != R.MK2


By Febi Agil Ifdillah(13514010), Harry Alvin Waidan Kefas, Naufal Malik Rabbani, Anwar Ramadha

Teknik Informatika ITB 2014
