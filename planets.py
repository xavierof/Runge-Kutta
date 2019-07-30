#!/usr/bin/env python3

import math
from turtle import *
pi=math.pi
# The gravitational constant G
G = 6.67428e-11

# Assumed scale: 100 pixels = 1AU.
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 250 / AU

class Body(Turtle):
    """Subclass of Turtle representing a gravitationally-acting body.

    Extra attributes:
    mass : mass in kg
    vx, vy: x, y velocities in m/s
    px, py: x, y positions in m
    """



    def attraction(self, other):
        """(Body): (fx, fy)

        Returns the force exerted upon this body by the other body.
        """
        # Report an error if the other object is the same as this one.
        if self is other:
            raise ValueError("Attraction of object %r to itself requested"
                             % self.name)

        # Compute the distance of the other body.
        sx, sy = self.px, self.py
        ox, oy = other.px, other.py
        dx = (ox-sx)
        dy = (oy-sy)
        d = math.sqrt(dx**2 + dy**2)

        # Report an error if the distance is zero; otherwise we'll
        # get a ZeroDivisionError exception further down.
        if d == 0:
            raise ValueError("Collision between objects %r and %r"
                             % (self.name, other.name))

        # Compute the force of attraction
        f = G * self.mass * other.mass / (d**2)

        # Compute the direction of the force.
        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f
        return fx, fy

def update_info(step, bodies):
    """(int, [Body])

    Displays information about the status of the simulation.
    """
    print('Step #{}'.format(step))
    for body in bodies:
        s = '{:<8}  Pos.={:>6.2f} {:>6.2f} Vel.={:>10.3f} {:>10.3f}'.format(
            body.name, body.px/AU, body.py/AU, body.vx, body.vy)
        print(s)
    print()

def loop(bodies):
    """([Body])

    Never returns; loops through the simulation, updating the
    positions of all the provided bodies.
    """
    timestep = 12*60*60 # One day

    for body in bodies:
        body.penup()
        body.hideturtle()

    step = 1
    while True:
        update_info(step, bodies)
        step += 1

        for body in bodies:
            # Add up all of the forces exerted on 'body'.
            total_fx = total_fy = 0.0
            for other in bodies:
                # Don't calculate the body's attraction to itself
                if body is other:
                    continue
                fx, fy = body.attraction(other)
                total_fx += fx
                total_fy += fy

            # Record the total force exerted.
            print("Name :{} force_x {:>10.2f} force_y {:>10.2f} ".format(body.name,total_fx/AU,total_fy/AU))

        # Update velocities based upo ass * timestep
            body.vy += total_fy / body.mass * timestep
            body.vx += total_fx/ body.mass *timestep
            # Update positions
            body.px += body.vx * timestep
            body.py += body.vy * timestep
            body.goto(body.px*SCALE, body.py*SCALE)
            body.dot(3)


def main():


    earth = Body()
    earth.name = 'Earth'
    earth.mass = 1.98892 * 10**30
    earth.px = -1*AU
    earth.py = 0-AU
    earth.vy= 1.5*math.sin(60*pi/180)*10**4
    earth.vx= -1.5*math.cos(60*pi/180)*10**4     # 29.783 km/sec
    earth.pencolor('blue')

    # Venus parameters taken from
    # http://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
    venus = Body()
    venus.name = 'Venus'
    venus.mass = 1.98892 * 10**30
    venus.px = 1*AU
    venus.py = 0-AU
    venus.vy = -1.5*math.sin(60*pi/180)*10**4
    venus.vx = -1.5*math.cos(60*pi/180)*10**4
    venus.pencolor('red')

    hatch = Body()
    hatch.name='hatch'
    hatch.mass= 1.98892 * 10**30
    hatch.px = 0
    hatch.py = math.sqrt(3)*AU -AU
    hatch.vy=0
    hatch.vx=1.5*1*10**4
    hatch.pencolor('green')

    loop([earth, venus, hatch])

if __name__ == '__main__':
    main()
