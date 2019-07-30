# window
WIDTH, HEIGHT = 900, 600

# simulated Planet
PLANETS = 20

#Density of planets (m/v)

DENSITY=0.001

# the gravity coefficient

G=1.e4
# Range Katta
import time
import numpy as np
import random
import pygame
import copy
from collections import defaultdict
# Global list of PLANETS
planet_list=[]


t_step=1.0

#Define position and velocity of an object
class State:
    def __init__(self,x,y,vx,vy):
        self.px=x;self.py=y;self.vx=vx;self.vy=vy

class Derivative:
    """Class representing velocity and acceleration."""
    def __init__(self, dx, dy, dvx, dvy):
        self._vx, self._vy, self._ax, self._ay = dx, dy, dvx, dvy

class Planet:
    def __init__(self):
        if PLANETS == 1:
            self._state= State(150,300,0,2)
        else:
            self._state= State(
                float(random.randint(0, WIDTH)),
                float(random.randint(0, HEIGHT)),
                float(random.randint(0, 300)/100.)-1.5,
                float(random.randint(0, 300)/100.)-1.5)
        self._r = 1.5
        self.setMassFromRadius()

    def setMassFromRadius(self):
            """From _r, set _m: The volume is (4/3)*Pi*(r^3)..."""
            self.m = DENSITY*4.*np.pi*(self._r**3.)/3.
    def acceleration(self,State):
        fxy=np.array([0.0,0.0])
        for Planet in planet_list:
            if Planet==self:
                continue
            sx=Planet._state.px-State.px
            sy=Planet._state.py-State.py
            r2=np.sqrt(sx**2+sy**2)
            F=G*self.m*Planet.m/r2**2
            #PRINT("force",F)
            fxy+=F*np.array([sx/r2,sy/r2])
            #PRINT("mass",self.m)
        a=fxy
        #PRINT(a)
        return a

    def nextDerivative(self, initialState, derivative, dt):
        """Part of Runge-Kutta method."""
        state = State(0., 0., 0., 0.)
        state.px = initialState.px + derivative._vx*dt
        state.py = initialState.py + derivative._vy*dt
        #PRINT("dy*dt",derivative._vy*dt)
        #PRINT("x,y", state.px,state.py)
        state.vx = initialState.vx + derivative._ax*dt
        state.vy = initialState.vy + derivative._ay*dt
        ax, ay = self.acceleration(state)
        return Derivative(state.vx, state.vy, ax, ay)

    def initialDerivative(self,state):
        ax,ay= self.acceleration(state)
        return Derivative(state.vx,state.vy,ax,ay)

    def update(self):
        #PRINT("1"*10)
        a = self.initialDerivative(self._state)
        b = self.nextDerivative(self._state, a, t_step*0.5)
        c = self.nextDerivative(self._state, b, t_step*0.5)
        d = self.nextDerivative(self._state, c, t_step)
        """#k_v_1=self.acceleration(self._state)    # euler method - slope of velocity
        k_r_1=np.array([self._state.vx,self._state.vy]) # euler method - position
        #PRINT("2"*10)

        temp_state=State(self._state.px+(k_r_1*t_step/2)[0],self._state.py+(k_r_1*t_step/2)[1],self._state.vx,self._state.vy)
        #PRINT(temp_state.py)
        #temp_state.px+=(k_r_1*t_step/2)[0]
        #temp_state.py+=(k_r_1*t_step/2)[1]
        #PRINT("k_r_1*t_step/2[1]",(k_r_1*t_step/2)[1])
        #PRINT("px,py",temp_state.px,temp_state.py)
        k_v_2=self.acceleration(temp_state) # accleration at midpoint, if particle followed euler
        k_r_2=np.array([self._state.vx,self._state.vy])+k_v_1*t_step/2 # velocity if followed euler on velocity
        #PRINT("3"*10)

        temp_state=State(self._state.px+(k_r_2*t_step/2)[0],self._state.py+(k_r_2*t_step/2)[1],self._state.vx,self._state.vy)
        #PRINT(temp_state.py)
        #temp_state.px+=(k_r_2*t_step/2)[0]
        #temp_state.py+=(k_r_2*t_step/2)[1]
        #PRINT("k_r_2*t_step/2[1]",(k_r_2*t_step/2)[1])
        k_v_3=self.acceleration(temp_state) # midpoint again, if particle had moved with k_r_2
        k_r_3=np.array([self._state.vx,self._state.vy])+k_v_2*t_step/2
        #PRINT("4"*10)

        temp_state=State(self._state.px+(k_r_3*t_step/2)[0],self._state.py+(k_r_3*t_step/2)[1],self._state.vx,self._state.vy)
        #temp_state.px+=(k_r_3*t_step)[0]
        #temp_state.py+=(k_r_3*t_step)[1]
        k_v_4=self.acceleration(temp_state)
        k_r_4=np.array([self._state.vx,self._state.vy])+k_v_3*t_step

        #PRINT("acceleration step: ", t_step/6*(k_v_1+ 2*k_v_2+2*k_v_3+k_v_4))
        #PRINT("velocity step: ",t_step/6*(k_r_1+ 2*k_r_2+2*k_r_3+k_r_4))
        self._state.vx, self._state.vy = np.array([self._state.vx,self._state.vy]) + t_step/6*(k_v_1+ 2*k_v_2+2*k_v_3+k_v_4)
        self._state.px = self._state.px+t_step/6*(k_r_1+ 2*k_r_2+2*k_r_3+k_r_4)[0]
        self._state.py = self._state.py+t_step/6*(k_r_1+ 2*k_r_2+2*k_r_3+k_r_4)[1]
        """
        dxdt = 1.0/6.0 * (a._vx + 2.0*(b._vx + c._vx) + d._vx)
        dydt = 1.0/6.0 * (a._vy + 2.0*(b._vy + c._vy) + d._vy)
        dvxdt = 1.0/6.0 * (a._ax + 2.0*(b._ax + c._ax) + d._ax)
        dvydt = 1.0/6.0 * (a._ay + 2.0*(b._ay + c._ay) + d._ay)
        self._state.px += dxdt*t_step
        self._state.py += dydt*t_step
        self._state.vx += dvxdt*t_step
        self._state.vy += dvydt*t_step

def main():
    pygame.init()

    #create screen
    win=pygame.display.set_mode((WIDTH,HEIGHT))


    keysPressed = defaultdict(bool)

    def ScanKeyboard():
        while True:
            # Update the keysPressed state:
            evt = pygame.event.poll()
            if evt.type == pygame.NOEVENT:
                break
            elif evt.type in [pygame.KEYDOWN, pygame.KEYUP]:
                keysPressed[evt.key] = evt.type == pygame.KEYDOWN

    global planet_list, PLANETS

    for i in range(PLANETS):
        planet_list.append(Planet())

    sun=Planet()
    sun._state=State(WIDTH/2,HEIGHT/2,0,0)
    sun.m*=1000
    planet_list.append(sun)
    bClearScreen = True
    t=0
    zoom = 1.0
    pygame.display.set_caption('Gravity simulation (SPACE: show orbits, '
                           'keypad +/- : zoom in/out)')
    i=0
    while i<10000:
        pygame.event.get()
        # update full screen
        pygame.display.flip()
        if bClearScreen:  # Show orbits or not?
            win.fill((0, 0, 0))
        # lock sufrace
        win.lock()
        for p in planet_list:
            if p is sun:
                continue  # for planets that have not been merged, draw a
                # circle based on their radius, but take zoom factor into account
            #draws a nice circle
            pygame.draw.circle(win, (255, 255, 255),
                    (int(p._state.px),
                     int(HEIGHT-p._state.py)),
                     int(2*zoom), 0)
        win.unlock()

        for p in planet_list:
            if p is sun:
                continue
            # Calculate the contributions of all the others to its acceleration
            # (via the gravity force) and update its position and velocity
            p.update()
            #PRINT(i, p._state.px,p._state.py)


        #unlock surface
        win.unlock()
        i+=1
        time.sleep(0)
if __name__ == "__main__":
        main()
