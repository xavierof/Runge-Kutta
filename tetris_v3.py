
import numpy as np
import random as rand
import time as clock
import clear_screen_v3
import queue
import threading

# Boundaries of grid and cascading blocks
width=12 # width of game
height=12 # height of screen
length=3 # square length/height

# keyboard input
horizontal_moves=["a","d"]
rotation_moves=["w","s"]


## SCORE



# Shape formats
shapes={'I': np.array([[[0,1,0],[0,1,0],[0,1,0]] , [[0,0,0],[1,1,1],[0,0,0]]]),
        'S': np.array([[[0,0,0],[0,1,1],[1,1,0]] , [[0,0,0],[1,1,0],[0,1,1]]])}


# This function will exit loop if the top rows become occupied
def check(screen):
    for i in range(0,3):
        if True in ((screen[i,]-1)>0):
            return(False)
    return(True)

#Queue user input
def read_kbd_input(inputQueue):
    #print('Ready for keyboard input:')
    while (True):
        # Receive keyboard input from user.
        input_str = input()

        # Enqueue this input string.
        # Note: Lock not required here since we are only calling a single Queue method, not a sequence of them
        # which would otherwise need to be treated as one atomic operation.
        inputQueue.put(input_str)

# Begin block class
class block:
    def __init__(self,x,shape,rotation):
        self.x=x  ## left most x coordinate (column)
        self.y=0  ## upper most y coordinate (row)
        self.shape= shape ## which shape
        self.rotation= rotation ## orientation of the object
        self.refresh=0 ## value will be 1 if it needs to be reset

    def rotate(self):
        self.rotation= (self.rotation+1) % 2

    def horizontal(self,letter,earth):
        falling_block_sum=produce(self).sum()

        # Check key input and whether or not a move to the right is possible
        if letter== "a" and self.x>0:
            self.x-=1

            # This is the screen if the move were permitted
            sum=produce(self)+earth.rock

            # Check if the move overwrite the earth.rock
            if  True in ((sum-1) > 0):

                # if there is overlap, we cannot allow the horizontal move
                self.x+=1

        #  Check key input and whether or not a move to the left is possible
        if letter == "d" and self.x<width-1:
            self.x+=1
            #This is the screen if the move were permitted
            sum=produce(self)+earth.rock

            # Check if the move overwrite the earth.rock
            if  True in ((sum-1) > 0):

                # if there is overlap, we cannot allow the horizontal move
                self.x-=1

            # We can't move the falling block down partially off the screen
            elif produce(self).sum()<falling_block_sum:

                #falling block would be moved off screen, repeal move
                self.x-=1

    def reset(self):

        self.shape=rand.choice(list(shapes.keys())) #assign block
        self.rotation=rand.randint(0,1) #assign rotation
        self.refresh=0 # revert reset indicator
        self.y=0 # blocks always begin from the top row
        self.x=rand.randint(0,9) # assign column

# end of block class


# maps block object onto a 12x12 np array
def produce(block):
    base=np.zeros([width,height])
    for i in range(length):
        for j in range(length):

            # overlay the block class onto the array - starting from the left moving right, from the top moving down
            # ensure that we don't move outside the base array
            if block.y+i<width and block.x+j<width:
                base[block.y+i,block.x+j]=shapes[block.shape][block.rotation][i,j]

    return base          # (x,y) is TOP LEFT hand corner

# Begin earth class. This class is for the blocks that accumulate at the bottom
# of the screen.
class earth:
    def __init__(self):
        self.rock=np.zeros([width,height])
        self.score=0

    # check if the current cascading block joins to the earth object
    def new_layer(self,block):
        grid=produce(block)
        if grid[width-1,].sum()>=1: # we have hit the very bottom row
            self.rock+=grid
            block.refresh=1 # kill the current falling_block

        # Will falling_block hit earth at the next time step
        else:
            block.y+= 1
            grid_future= produce(block)
            if 2 in (self.rock+grid_future):
                block.y-=1
                self.rock = self.rock + grid
                block.refresh=1
            else:
                block.y-=1

    def row_wipe(self):
        for j in range(height-1,-1,-1):
            if self.rock[j,].sum()==12:
                self.rock[j,]=0
                self.rock[1:j+1,]=self.rock[0:j,]
                self.score+=1
def main():
    t1=0
    period=0.4 # Every 0.4 seconds of system time, the loop will check the screen is in viable state
    inputQueue = queue.Queue() # Queue of user commands
    inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
    inputThread.start()
    falling_block=block(4,'I',1) # First falling block
    base=earth() # Initalise base. This is the object which accumulates to the users peril
    run = True
    while run:
        t=clock.time()

        # Check if the user has entered a command
        if inputQueue.qsize() > 0:

            # Retrieve command
            input_str = inputQueue.get()
            if input_str in horizontal_moves:
                clear_screen_v3.clear() # Refresh screen
                falling_block.horizontal(input_str,base) # Check vadility of move then implement
                print(produce(falling_block)+base.rock)
                print("Score: ",base.score)

            if input_str in rotation_moves:
                clear_screen_v3.clear() # Refresh screen
                falling_block.rotate()  # Check vadility of move then implement
                print(produce(falling_block)+base.rock)
                print("Score: ",base.score)

        if t-t1>=period:
            clear_screen_v3.clear()

            # Check if we need a new falling block
            if falling_block.refresh == 1:

                # Create new falling block
                falling_block.reset()
                # falling_block needs to be refreshed

            current_screen=produce(falling_block)+base.rock
            # have we overlayed a falling_block over occupied cells?
            run=check(current_screen)

            print(current_screen)
            print("Score: ", base.score)
             # Print Current state

            # Update earth object
            base.new_layer(falling_block)
            base.row_wipe()
            # Update descending block
            falling_block.y+=1
            t1=clock.time()
        clock.sleep(0)
if __name__ == "__main__":
    main()
