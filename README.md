# Simple-Evolution-Simulation

This is a very simple simulation that simulates the process of natural selection.
In this simulation there are multiple creatures (1000). Each creature has a brain, which represent a sequence of actions (400 actions). Those actions are random acceleration vectors, which make the creature moves and accelerate in different directions.
The initial population is totaly random, with random sequances of acceleration for each creature.
The simulation idea is that when each generation finishs the simulation (each creature reaches a wall or a border of screen), a new generation is created.
The creation of the new generation depends on the  performance of the previous generation.
Each creature from the new generation is created using one of the previous generation, with some random changes applied.
The Best creature goes on in the next generation.
The better the creature does, the more chances it gets to have children in the next generation.
The performance is measured purely using the distance to the target (the red dot), the closer the better.
The Best creature from the previous generation is colored bule.

with time there should be creatures who learned to reach the final goal.

Many improvements can be done on this simulation, one of which is to take the time needed to reach the final position into account when calculating the performance.
Another improvement is to try to make the movement as smooth as possible, by taking the changes of acceleration vector into account when calculation the performance.

The purpose of this simulation is to deonstrate the idea of natural selection and evolution.


To run the simulation just run the Run_Simulation.py file.
