# timeTablingCSP

IF3170 Artificial Intelligence Course Project.

Create Course Timetabling Application using CSP's Algorithms :
  1. Hill Climbing Algorithm
  2. Simulated Annealing
  3. Genetic Algorithm
  
Identifying Problem Component :
  1. Variables
		The variables of this problem is 
			\t\t\t s(h,j), the position of values that will be assigned
			\t\t\t where h is the day representations (1 = Monday, 2 = Tuesday, and so on)
  2. Domains
		\t\t a. MK -> key by Course_Id & Course_No <br>
		\t\t b. R -> key by Room_Name & MK <br>
  3. Constraints
		\t\t a. h >= 1 && h <= 5 <br>
		\t\t b. j >= 7 && j <= 17 <br>
		\t\t c. MK1#h,j != MK2#h,j <br>
		\t\t d. R.MK1 != R.MK2 <br>
		\t\t e. MK.R == '-' -> MK.R = random(R) <br>


By Febi Agil Ifdillah(13514010), Harry Alvin Waidan Kefas, Naufal Malik Rabbani, Anwar Ramadha

Teknik Informatika ITB 2014
