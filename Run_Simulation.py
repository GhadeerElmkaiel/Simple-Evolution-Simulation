import pygame
import random
import math


# -----------------------------------------------------------------
pygame.init()

winWidth = 1100
winHeight = 800
playWinWidth = 800
playWinHeight = 800
FPS = 100

mutationRate = 0.01
hugeMutationRate = 0.05
gen = 1
maxFitness = 0
minAnglesChange = 10**7
minSteps = 1000
minStepsLimit = 50
oneReachedGoal = False

showAll = True
withWalls = True


clock = pygame.time.Clock()
gameDis = pygame.display.set_mode((winWidth, winHeight))


startPos = [playWinWidth/2, playWinHeight-20]
maxSpeed = 9


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 0)
darkGray = (30, 30, 30)
lightGray = (200, 200, 200)


bestUnitImgSize = 150
bestUnitImgWidthStart = playWinWidth + (winWidth - playWinWidth - bestUnitImgSize)/2
bestUnitImgHeightStart = 520
unitWidth = 10
unitHeight = 15
unit = pygame.image.load("Unit.png")
bestUnit = pygame.image.load("BestUnit.png")
bestUnitBig = pygame.image.load("BestBig.png")


bestUnitsInGens = []

# -----------------------------------------------------------------


def dis(pos1, pos2):
    return (math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2))

# -----------------------------------------------------------------


def get_msg_objects(msg, color, font):
    textSurface = font.render(msg, True, color)
    return textSurface, textSurface.get_rect()

# -----------------------------------------------------------------


def msg_to_screen(msg, pos, color=(0, 0, 0), size = 25):
    font = pygame.font.SysFont(None, size)
    textSurface, textRect = get_msg_objects(msg, color, font)
    textRect.center = pos[0], pos[1]
    gameDis.blit(textSurface, textRect)

# -----------------------------------------------------------------


def msg_to_screen_corner(msg, pos, color=(0, 0, 0), size = 25):
    font = pygame.font.SysFont(None, size)
    textSurface = font.render(msg, True, color)
    gameDis.blit(textSurface, pos)

# -----------------------------------------------------------------


def update_control_ban():
    pygame.draw.rect(gameDis,  (30, 30, 30), [playWinWidth,0,winWidth - playWinWidth, winHeight])
    msg_to_screen_corner("Max Fitness =", [playWinWidth + 10, 10],lightGray, 30)
    if not oneReachedGoal:
        msg_to_screen_corner(str(int(maxFitness)), [playWinWidth + 10, 35], lightGray, 30)
    else:
        msg_to_screen_corner("Max Value", [playWinWidth + 10, 35], lightGray, 30)

    msg_to_screen_corner("Gen : ", [playWinWidth + 10, 80], lightGray, 30)
    msg_to_screen_corner(str(gen), [playWinWidth + 10, 105], lightGray, 30)

    msg_to_screen_corner("Min Num of Steps : ", [playWinWidth + 10, 150], lightGray, 30)
    if minSteps > 400 :
        msg_to_screen_corner("INF", [playWinWidth + 10, 175], lightGray, 30)
    else:
        msg_to_screen_corner(str(minSteps), [playWinWidth + 10, 175], lightGray, 30)

    msg_to_screen_corner("Min Unit Angles Change : ", [playWinWidth + 10, 220], lightGray, 30)
    if minAnglesChange >= 10**7:
        msg_to_screen_corner("INF", [playWinWidth + 10, 245], lightGray, 30)
    else:
        msg_to_screen_corner(str(int(minAnglesChange)), [playWinWidth + 10, 245], lightGray, 30)

    msg_to_screen_corner("The Best Unit :", [playWinWidth + 10, bestUnitImgHeightStart - 30], lightGray, 30)
    # pygame.draw.rect(gameDis, white, [playWinWidth + (winWidth - playWinWidth - bestUnitImgSize)/2, bestUnitImgHeightStart, winWidth - (winWidth - playWinWidth - bestUnitImgSize)/2, bestUnitImgHeightStart + bestUnitImgSize])
    pygame.draw.rect(gameDis, white, [bestUnitImgWidthStart, bestUnitImgHeightStart, bestUnitImgSize, bestUnitImgSize])


# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

class Wall:
    def __init__(self, pos, width, height):
        self.pos = pos
        self.height = height
        self.width = width
        global gameDis

    def show(self):
        pygame.draw.rect(gameDis, (170, 170, 170), [self.pos[0], self.pos[1], self.width, self.height])


# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

walls=[]

wall_1 = Wall([300, 500], 500, 20)
wall_2 = Wall([0, 300], 500, 10)

walls.append(wall_1)
walls.append(wall_2)

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------
"""
The Brain for each unit which contain the directions and angles matrices
and the number of steps were used to get to the goal
"""


class Brain:
    def __init__(self, size):
        self.size = size
        self.directions = []
        self.angles = []
        self.randomize()
        self.steps = 0
        self.mutationRate = mutationRate

    """
    Randomize the initial values for the directions matrix and calc the 
    angles matrix 
    """
    def randomize(self):
        for i in range(self.size):
            r = 2*math.pi*random.random()
            vector = [math.cos(r), math.sin(r)]
            self.directions.append(vector)
            self.angles.append(r*180/math.pi)

    """
    Clone the directions and angles matrices to give to new unit
    """
    def clone(self):
        clone = Brain(self.size)
        for i in range(self.size):
            clone.directions[i] = self.directions[i]
            clone.angles[i] = self.angles[i]
        return clone

    """
    Make small changes to some of the directions and angle values
    """
    def mutate(self, hugeMutate = False):
        for i in range(self.size):
            r = random.random()
            if r < self.mutationRate:
                r = 2 * math.pi * random.random()
                self.angles[i] = r*180/math.pi
                vector = [0.5*math.cos(r), 0.5*math.sin(r)]
                self.directions[i]=vector
        if hugeMutate:
            for i in range(self.size):
                r = random.random()
                if r < self.mutationRate*10:
                    r = 2 * math.pi * random.random()
                    self.angles[i] = r * 180 / math.pi
                    vector = [0.5 * math.cos(r), 0.5 * math.sin(r)]
                    self.directions[i] = vector


# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------
"""
The calss that define each unit and have the parameters position and
speed and acceleration and the brain 
"""


class Dot:
    def __init__(self, color=(0, 0, 0)):
        global maxSpeed
        global playWinHeight
        global playWinWidth
        global goal
        global gameDis
        global startPos

        self.pos = [playWinWidth/2, playWinHeight-20]
        self.speed = [0, 0]
        self.acc = [0, 0]
        self.radius = 4
        self.maxSpeed = maxSpeed
        self.brain = Brain(400)
        self.isDead = False
        self.reachedGoal = False
        self.fitness = 0
        self.color = color
        self.isBest = False
        self.angle = 90
        self.lastAngle = 90
        self.angleChanges = 0

    # ------------------------------------------------------

    def show(self):
        if self.isBest:
            imgDir = pygame.transform.rotate(bestUnit, self.angle -90)
            imgBigDir = pygame.transform.rotate(bestUnitBig, self.angle -90)
            rect = imgBigDir.get_rect()
            gameDis.blit(imgDir, (self.pos[0] - int(unitWidth/2), self.pos[1] - int(unitHeight/2)))
            gameDis.blit(imgBigDir, (bestUnitImgWidthStart-int((rect[2]-bestUnitImgSize)/2), bestUnitImgHeightStart-int((rect[3]-bestUnitImgSize)/2)))

        else:
            imgDir = pygame.transform.rotate(unit, self.angle -90)
            gameDis.blit(imgDir, (self.pos[0] - int(unitWidth/2), self.pos[1] - int(unitHeight/2)))
            # pygame.draw.circle(gameDis, self.color, [int(self.pos[0]), int(self.pos[1])], self.radius, 0)

    # ------------------------------------------------------

    def move(self):
        if (len(self.brain.directions) > self.brain.steps):
            self.acc = self.brain.directions[self.brain.steps]
            self.angle = self.brain.angles[self.brain.steps]
            self.angleChanges+= min(abs(self.angle - self.lastAngle), abs(min(self.angle, self.lastAngle) - max(self.angle, self.lastAngle) + 360))
            self.lastAngle = self.angle
            self.brain.steps += 1
        for i in range(2):
            self.pos[i] += self.speed[i]
            self.speed[i] += self.acc[i]
        if self.speed[0] > self.maxSpeed:
            self.speed[0] = self.maxSpeed
        elif self.speed[0] < -1*self.maxSpeed:
            self.speed[0] = -1*self.maxSpeed
        if self.speed[1] > self.maxSpeed:
            self.speed[1] = self.maxSpeed
        elif self.speed[1] < -1*self.maxSpeed:
            self.speed[1] = -1*self.maxSpeed

    # ------------------------------------------------------

    def check_if_out(self):
        if self.pos[0]<self.radius*1.2 or (self.pos[0]>playWinWidth-self.radius*1.2) or (self.pos[1]<self.radius*1.2) or (self.pos[1] > playWinHeight - self.radius*1.2):
            self.isDead = True
            return True
        return False

    # ------------------------------------------------------

    def check_if_hit_wall(self, wall):
        if (self.pos[0] > wall.pos[0] - self.radius) and (self.pos[0] < wall.pos[0] + wall.width + self.radius) and (self.pos[1] > wall.pos[1] - self.radius) and (self.pos[1] < wall.pos[1] + wall.height + self.radius):
            self.isDead = True
            return True
        return False

    # ------------------------------------------------------

    def check_if_reach_goal(self):
        global oneReachedGoal
        if dis(self.pos, goal.pos) < self.radius:
            self.reachedGoal = True
            oneReachedGoal = True
            # self.isDead = True
            return True
        return False

    # ------------------------------------------------------

    def update(self):
        if not (self.isDead or self.reachedGoal):
            self.check_if_reach_goal()
            self.check_if_out()
            if withWalls:
                for wall in walls:
                    self.check_if_hit_wall(wall)
            if not (self.isDead or self.reachedGoal):
                self.move()

    # ------------------------------------------------------

    def calc_fitness(self):
        # if self.reachedGoal:
        #     self.fitness = 10000 + (1/((0.001*(self.brain.steps-1.5*minStepsLimit))**6))*((10000/self.angleChanges)**3)
        # else:
        #     self.fitness = (100 / ((0.01*(dis(self.pos, goal.pos)))**4 + 0.05)) + 100/self.angleChanges

        if not oneReachedGoal:
            self.fitness = (1000 / ((0.01 * (dis(self.pos, goal.pos))) ** 4 + 0.05)) + 100 / self.angleChanges
        else:
            if not self.reachedGoal:
                self.fitness = (1000 / ((0.1 * (dis(self.pos, goal.pos))) ** 4)) /(3*max(0.5, self.brain.steps - minSteps)) / (max(0.9, self.angleChanges - minAnglesChange))
            else:
                self.fitness = 10**5 / (3 * max(1, self.brain.steps - minSteps)) / (max(1, self.angleChanges - minAnglesChange))

    # ------------------------------------------------------

    def get_baby(self):
        baby=Dot()
        baby.brain = self.brain.clone()
        return baby

    # ------------------------------------------------------

    def duplicate(self, dupl):
        self.brain.size = dupl.brain.size
        for i in range(self.brain.size):
            self.brain.directions[i] = dupl.brain.directions[i]

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------


class Population:
    def __init__(self, num):
        self.num = num
        self.dotsList = []
        self.fitnessSum = 0
        self.gen = 1
        self.minSteps = 1000
        self.minAnglesChange = 10**7
        self.plusStepsAllowed = 30

        for i in range(self.num):
            d = Dot()
            self.dotsList.append(d)

    # ------------------------------------------------------

    def show(self):
        if showAll:
            for i in range(self.num):
                self.dotsList[i].show()
        self.dotsList[0].show()

    # ------------------------------------------------------

    def update(self):
        for i in range(self.num):
            if self.dotsList[i].brain.steps > self.minSteps + self.plusStepsAllowed:
                self.dotsList[i].isDead = True
            else:
                self.dotsList[i].update()

    # ------------------------------------------------------

    def calc_min_steps(self):
        global  minSteps
        for i in range(self.num):
            if self.dotsList[i].reachedGoal and self.dotsList[i].brain.steps < self.minSteps:
                self.minSteps = self.dotsList[i].brain.steps

            minSteps = self.minSteps

    # ------------------------------------------------------

    def calc_min_angle_change(self):
        global minAnglesChange
        firstCalc = True
        for i in range(self.num):
            if self.dotsList[i].reachedGoal and self.dotsList[i].brain.steps == self.minSteps and firstCalc:
                firstCalc = False
                self.minAnglesChange = self.dotsList[i].angleChanges
            elif self.dotsList[i].reachedGoal and self.dotsList[i].brain.steps == self.minSteps and self.dotsList[i].angleChanges < self.minAnglesChange:
                self.minAnglesChange = self.dotsList[i].angleChanges

            minAnglesChange = self.minAnglesChange


    # ------------------------------------------------------

    def calc_fitness(self):
        for i in range(self.num):
            self.dotsList[i].calc_fitness()

    # ------------------------------------------------------

    def allAreDead(self):
        for i in range(self.num):
            if (not self.dotsList[i].isDead) and (not self.dotsList[i].reachedGoal):
                return False
        return True

    # ------------------------------------------------------

    def calc_fitness_sum(self):
        self.fitnessSum = 0
        for i in range(self.num):
            self.fitnessSum += self.dotsList[i].fitness

    # ------------------------------------------------------

    def get_parents(self):
        r = random.random()*self.fitnessSum
        fitTempSum = 0

        i = 0
        while(fitTempSum < r):
            fitTempSum += self.dotsList[i].fitness
            i += 1

        return self.dotsList[i-1]

    # ------------------------------------------------------

    def get_best_dot(self):
        global maxFitness
        global minSteps
        global bestAnglesChange
        global bestUnitsInGens
        maxFit = 0
        bestDotIndex = 0
        for i in range(self.num):
            if self.dotsList[i].fitness > maxFit:
                maxFit = self.dotsList[i].fitness
                bestDotIndex = i
                self.dotsList[i].isBest = False

        if self.dotsList[bestDotIndex].reachedGoal:
            self.minSteps = self.dotsList[bestDotIndex].brain.steps

        maxFitness = maxFit
        bestAnglesChange = int(self.dotsList[bestDotIndex].angleChanges)
        minSteps = self.dotsList[bestDotIndex].brain.steps
        if(self.gen%10 == 0 or gen == 1):
            bestUnitsInGens.append(self.dotsList[bestDotIndex].brain.angles)
        return bestDotIndex

    # ------------------------------------------------------

    def natural_selection(self):
        global gen

        newPop = Population(self.num)
        newPop.dotsList[0] = self.dotsList[self.get_best_dot()].get_baby()
        newPop.dotsList[0].isBest = True
        self.calc_fitness_sum()
        for i in range(self.num):
            if i > 0:
                parents = self.get_parents()
                newPop.dotsList[i].brain = parents.brain.clone()

        self.dotsList = newPop.dotsList
        self.gen += 1
        gen = self.gen

    # ------------------------------------------------------

    def mutate_baby(self):
        for i in range(self.num):
            if i > 0:
                self.dotsList[i].brain.mutate()
        for i in range(self.num):
            if i > 0:
                r = random.random()
                if r < hugeMutationRate:
                    self.dotsList[i].brain.mutate(True)

    # ------------------------------------------------------

    def get_new_gen(self):
        self.calc_min_steps()
        self.calc_min_angle_change()
        self.calc_fitness()
        self.calc_fitness_sum()
        self.natural_selection()
        self.mutate_baby()


# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

class Goal:
    def __init__(self, pos):
        self.pos = pos
        self.radius = 5
        global gameDis
    def show(self):
        pygame.draw.circle(gameDis, (255, 0, 0), self.pos, self.radius)









pop = Population(1000)
goal = Goal([int(playWinWidth/2), 20])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_b:
                showAll = not showAll
            if event.key == pygame.K_w:
                withWalls = not withWalls
            if event.key == pygame.K_p:
                pass

    gameDis.fill((255, 255, 255))

    goal.show()
    if withWalls:
        for wall in walls:
            wall.show()

    if(pop.allAreDead()):
        pop.get_new_gen()

    update_control_ban()
    pop.show()
    pop.update()


    pygame.display.update()
    clock.tick(FPS)

