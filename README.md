# Gomoku Report	

###### Lida Zhao  11611803

###### *School of Computer Science and Engineering*

###### *Southern University of Science and Technology*

###### *Email: 11611803@mail.sustc.edu.cn*

### 1. Abstraction

​	This project is about to implement a *Gomoku* AI program. In this report, I will first give a brief introduction of *Gomoku*. Then I will mention the software that I use. The Algorithm and Methodology will follow right behind. To be more specific, I mainly use **Min-Max**, I also tried some **Single-point evaluation** method. Not as good as the **Min-max**.  Next, I will introduce the Architecture of my program and more details of the algorithm and functional functions. Last but not least,  all the design and analysis and so on will be included in the **Performance and Analysis** part. 

### 2. Preliminaries

​	 *Gomoku* is an ancient Chinese game, and its rule can be concluded in a single sentence: Any 5 of your chess pieces linked in a line, you win. Nevertheless, simple rule always conceals great tricks or strategies. While playing, players must consider a lot, not only his chess pieces but also the rival's chess pieces. Great players always think several steps ahead. This part I will introduce the software and the basic algorithm.

##### 2.1. Software

​	The whole program is written in Python by Pycharm. The library included contains *numpy*, *random*, *copy*.

##### 2.2. Algorithm

​	In this program, I first choose **Min-Max** to implement the *Gomoku*. **Min-Max** is a good algorithm for finding the best next step. In each layer, I put whether my chess or the other chess on the board and at the deepest layer, I judge the whole situation. Give each chess that has already existed a score, and sum them up according to there color. Suppose I am the computer, and my rival is human. Then the whole situation score should be the sum of computers. So, I can judge whether this situation is good or bad for me.
$$
situation = \sum chess_{computer} -\sum chess_{human}
$$


### 3. Methodology

​	The *Gomoku* is a simple game, but not an easy game. A lot of detail should be noticed.  In this part, I will show the details of representation, architecture, and algorithm in my program.

##### 3.1. Representation

​	The program contains several  important data that should be maintained through the whole process: chess board, chessboard_size, color, time_out, candidate_list, score  there types are shown below

+ chess board *numpy array* :a numpy 2 dimension array
+ color
  + COLOR_BLACK *int*: Refers to the first going player 
  + COLOR_WHITE *int*: Refers to the second going player
  + COLOR_NONE *int*: No chess
+ time_out *int*: Time limitation
+ candidate_list *list*: When time out or method finished, the program will extract the last position of the list.
+ score  *int*: This is the score board of the patterns

##### 3.2. Architecture

​	Here list all the function that I used in this program and there usage.

- hasNeighbor
  - To verify whether a point on the board has neighbor.
  - Parameters:
    - x, y *int* :Denote the coordinate 
    - neighborNum *int* : The threshold value of neighbor number
    - distance *int* : Has neighbor within the distance
    - chessboard *numpy array*
- findPattern
  - Choose a certain point as beginning, stretching in four direction to find the pattern that this point is in. From the begin point it will first go in one direction, if met the same color, count plus one; if met the blank, jump the blank to see whether there is a same color chess right behind the blank. If so, count plus one and record the blank place by *gap*, else, end the stretch; Also, if met the other color chess, stop the stretch in this direction. Once one direction is finished, go ahead on the counter direction and continue the count. After that, change another direction.
  - Parameters
    - chessboard *numpy array*
    - x, y *int* : Denote the coordinate 
    - role *int* : Denote which player's pattern is now processing
- makeScore
  - Once the pattern is found, the program will call this function to give each pattern a score. 
  - Parameters
    - count *int* :The number of same-color-chess
    - barrier *int* :To denote whether there is a counter chess at either end of the line
    - gap *int* : Denote the position of the blank
- evaluation
  - Used to sum all the computer's chess pieces' score and then minus the sum of the human's chess's' score
  - Parameters
    - chessboard *numpy array*
    - comp_color *int* : The color of computer
- revers_role
  - Revers the role
  - Parameter
    - role *int* : Denote the role now
- is_win
  - Judge whether a player is win after placing a chess piece.
  - Parameter
    - x, y *int* : Denote the coordinate 
    - chessboard *numpy array* 
    - role *int*: Denote the role now
- minmax
  - inside the *minmax*  are *max_value* and *min_value*. This is the bootstrap of the whole algorithm
  - Parameter
    - chessboard *numpy array* 
- max_value
  - Parameter
    - x, y *int* : Denote the coordinate 
    - alpha, beta *int* : To implement alpha-beta pruning
    - depth *int* : The max depth it goes
    - role *int*: Denote the role now
- min_value
  - Parameter
    - x, y *int* : Denote the coordinate 
    - alpha, beta *int* : To implement alpha-beta pruning
    - depth: *int* The max depth it goes
    - role *int*: Denote the role now

##### 3.3. Detail of Algorithm

​	This part will show the detail of the algorithm.

- hasNeighbor: use loop and several boolean function 

  ``` pseudocode
  input: x, y, neighborNum, distance, chessboard
  output:
  	if #no_chess in distance around (x,y) < neighborNum
  		return false
  	else return true
  ```

- findPattern: use loop and several boolean function. It is more likely to put the chess around the existing chesses

  ```pseudocode
  input:chessboard, x, y, role
  output:
  	for direction1 in four directions
  		for points in direction1
  			if next points == blank
  				if the first time meet a blank 
                  	and chess behind nextpoints == role
                  	gap <- gap position
                  	count<- count + 1
              if next points == role
              	count<- count + 1
              if next points == counter role or out_of_bound
              	barrier <- barrier + 1
          for points in direction1_opposite
          	if next points == blank
  				if the first time meet a blank 
                  	and chess behind nextpoints == role
                  	gap <- gap position
                  	count<- count + 1
              if next points == role
              	count<- count + 1
              if next points == counter role or out_of_bound
              	barrier <- barrier + 1
         call function(makeScore)
      return score of (x,y)
  ```

- makeScore: a bounch of if else condition, contains all the situations that may occor. Will  show the code here

  ```python
      def makeScore(self, count, barrier, gap, good_barrier):
          # 没有空隙00000
          if gap <= 0:
              if count >= 5: 		 return score['FIVE']
              if barrier == 0:
                  if count == 4:   return score['FOUR']
                  elif count == 3: return score['THREE']
                  elif count == 2: return score['TWO']
                  elif count == 1: return score['ONE']
              elif barrier == 1:
                  if count == 4:   return score['DEAD_FOUR']
                  elif count == 3: return score['DEAD_THREE']
                  elif count == 2: return score['DEAD_TWO']
                  elif count == 1: return score['DEAD_ONE']
              elif barrier == 2:   return score['DEAD']
              else: 				 return 0
          # 空隙在第一个位置或者倒数第一个0_0000
          elif gap == 1 or gap == count - 1:
              if count >= 6: 		 return score['FIVE']
              if barrier == 0:
                  if count == 5:   return score['FOUR']
                  elif count == 4: return score['JUMP_FOUR']
                  elif count == 3: return score['JUMP_THREE']
                  elif count == 2: return score['JUMP_TWO']
              elif barrier == 1:
                  if count == 5:
                      if good_barrier:
                          		 return score['DEAD_FOUR']
                      else:  		 return score['FOUR']
                  elif count == 4:
                      if good_barrier:
                             		 return score['DEAD_JUMP_FOUR']
                      else:  	 	 return score['THREE']
                  elif count == 3:
                      if good_barrier:
                             		 return score['DEAD_JUMP_THREE']
                      else:  		 return score['TWO']
                  elif count == 2:
                      	   		 return score['DEAD_JUMP_TWO']
              elif barrier == 2:
                  if count == 5:   return score['DEAD_FOUR']
                  elif count == 4: return score['DEAD_FOUR']
                  else: 			 return score['DEAD']
              else: 	    		 return 0
          # 空隙在第二个位置或者倒数第二个00_0000
          elif gap == 2 or gap == count - 2:
              if count >= 7: 		 return score['FIVE']
              if barrier == 0:
                  if count == 6:   return score['FOUR']
                  elif count == 5: return score['JUMP_FOUR']
                  elif count == 4: return score['JUMP_THREE']
              elif barrier == 1:
                  if count == 6:
                      if good_barrier: 
                          	     return score['DEAD_FOUR']
                      else: 		 return score['FOUR']
                  elif count == 5:
                      if good_barrier: 
                          		 return score['DEAD_FOUR']
                      else: 		 return score['JUMP_FOUR']
                  elif count == 4: return score['DEAD_JUMP_FOUR2']
              elif barrier == 2:
                  if count == 6:   return score['DEAD_FOUR']
                  elif count == 5: return score['DEAD_JUMP_FOUR']
                  elif count == 4: return score['DEAD_JUMP_FOUR']
              else:
                  				 return 0
          elif gap == 3 or gap == count - 3:
              if count >= 8: 		 return score['FIVE']
              if barrier == 0:
                  if count == 7:   return score['FOUR']
                  if count == 6:   return score['JUMP_FOUR']
              elif barrier == 1:
                  if count == 7:
                      if good_barrier:  
                          		 return score['JUMP_FOUR']
                      else:  		 return score['FOUR']
                  elif count == 6: return score['JUMP_FOUR']
              elif barrier == 2:
                  if count == 7: 	 return score['DEAD_FOUR']
                  elif count == 6: return score['DEAD_FOUR']
                  else:  			 return score['DEAD']
              else: return 0
          elif gap == 4 or gap == count - 4:
              if count >= 9: 		 return score['FIVE']
              if barrier == 0:
                  if count == 8:	 return score['FOUR']
              if barrier == 1:
                  if count == 8: 	 return score['FOUR']
              if barrier == 2:
                  if count == 8:   return score['DEAD_FOUR']
              else: 				 return 0
          else:					 return 0
  ```

- evaluation: sum

  ```pseudocode
  output:
  	for all points in board	
  		if points == comp_color
  			comp <- comp + findPattern(points)
  		if points == hum_color
  			hum <- hum + findPattern(points)
  	situation = comp - hum
  	return situation
  ```

- revers_role: simply using if else to reverse

  ```pseudocode
  input: role
  output:
  	if role == comp_color
  		return hum_color		
  	else
  		return comp_color	
  ```

- is_win: use loop to find the **five-in-line** pattern

  ```pseudocode
  input (x,y) 
  output:
  	for four directions of (x,y)
  		if in this direction 5 chess lined
  		return true
  	return false
  ```

- minmax: 

  ```pseudocode
  bestScore = float('-inf')
  beta = float('inf')
  bestAction = None
  going_list = set()
  
  for all empyt points in chessboard
  		if empyt points hasNeighbor
  			going_list.add(points)
  if going_list is empty:
  	bestAction <- (center, center)
  	return
  for empty_point in going_list:
  	score = min_value(next_x,next_y,alpha,beta,depth-1, role)   
  	if score > bestScore:
  		bestScore <- score
  		bestAction <- empty_point
  return bestAction
  ```



  - max_value: use recursion to find the steps

    ```pseudocode
    input: x, y, alpha, beta, depth, role
    output:
    	chessboard[x][y] <- role
    	if is_win(x,y,role)
           chessboard[x][y] <- COLOR_NONE
           return inf, x, y
        if depth <= 0:
           evaluate the situation
    		return situation    
    	
    	v = inf
    	for all the new points around (x,y)
    		add to the going_list
    		v <- min(v,max_value(next_x,next_y,alpha,beta,depth-1, reverse(role))     
            beta <- min(beta, v)
    		if beta <= alpha:
            	chessboard[x][y] <- COLOR_NONE
                return v, x, y
             chessboard[x][y] <- COLOR_NONE
       return v, x, y
    ```

  - min_value: use recursion to find the steps

    ```pseudocode
    input: x, y, alpha, beta, depth, role
    output:
    	chessboard[x][y] <- role
    	if is_win(x,y,role)
           chessboard[x][y] <- COLOR_NONE
           return -inf, x, y
        if depth <= 0:
           evaluate the situation
    		return situation    
    	
    	v = -inf
    	for all the new points around (x,y)
    		add to the going_list
    		v <- min(v,max_value(next_x,next_y,alpha,beta,depth-1, reverse(role))   
            alpha <- max(alpha, v)
    		if beta <= alpha:
            	chessboard[x][y] <- COLOR_NONE
                return v, x, y
             chessboard[x][y] <- COLOR_NONE
       return v, x, y
    ```

### 4. Performance and Analysis

​	This part will be the performance report and analysis of the program

##### 4.1. Test data

​	The test data is from the Sakai. I also got a program made by a classmate that can play Gomoku with human or another program locally. This helps a lot, I even put the former version of the code and the latter version to play against to see if there is any improvement.

##### 4.2. Performance

​	In this program, my depth is only 2. The time complexity is around *O(n^4)*, however, it is already very time-consuming. 

##### 4.3. Analysis

​	I have simplified the going_list. Before modification, the list would scan the whole board to find the blank points, but now it only scans the board once and if any new points are added, I only update the points around it. There are also some optimizations that I didn't do. Actually, I should pre-verify each blank point and arrange them which will make alpha-beta pruning more effective. Sometimes my min-max can not even defeat the program with single point validation. I listed all the patterns and try to give all patterns a score, but it still cannot defeat them which make me kind of confused. I think maybe my score function is not good enough, and the validation of each situation is not effective enough.

##### 4.4. Additional works

​	The version I presented is only a small part of my whole work, actually, I have written 7 versions of it and cost more than 40 hours in total. Those 4 of the versions are for exploring a better score function, one is about single point valuation(because I heard my classmates use this method), 2 is trying to add a cache in it.

### 5.conclusion

​	I have read a lot about the right algorithm before really get down to it. I spend a lot of time on understanding the JS code in a blog. Trying hard to extract the algorithm from the source code. However, it is not easy, the code has a lot of unrelated function that I may not yet use, and it will distress me. After finally finish my code, I found that a lot of classmate do not use a relatively "complicated algorithm" like min-max at the very beginning, what's more, they even performs better than me which makes me very annoyed. Thus, in later time, I always think there is something wrong with my algorithm and try to transfer to another one. I did try. But the result is also not so good. This cost me a lot of time-- writing useless code. Although I learned more, but time is gone after all. I should stick on a algorithm and keep going on improving it but not change to another one.

### 6. Acknowledgements 

​	I really appreciate Shuxin Wang, Zhiyuan Wang that we communicate a lot about how to work out this problem and how to improve the algorithm. Thanks for there thoughts. Also, I appreciate all the work paid by our teaching assistant Yao Zhao. Thanks for all the effective algorithm that you introduced. Thank for all the student assistant, you make such a great online combat platform. It is really a great job. Thanks to the unknown blog writer called *lihongxun945*, your blog solved most of my confuse and gave me new thoughts. Last but not least, I would thank Jie Ji, who always keep accompany with me and encourage me whenever I am in a dilemma.

### 7. References

Github contributors,[online].https://github.com/lihongxun945/myblog/issues/11,[Accessed: 10-10-2018]

CSDN contributors,[online].https://blog.csdn.net/u013351484/article/details/51417641

[Accessed:13-10-2018]

