'''

Name:            LIN Xufeng

Student ID:      2043 1281

Email-address:   xlinax@connect.ust.hk

Information : Dear marker , you can change game model by clicking
"Switch theme" and change it back by clicking again , and start
it by clicking "START" , game will start after 2-second to let user
preprare to start game ! 
thank you for your marking !

'''

import turtle
import time
import pygame
import random

# Sound effect control 
pygame.init()
pygame.mixer.init(buffer=16)

# Sound file
shootsoundeffect = pygame.mixer.Sound('shoot.wav')
gamestarsoundeffect = pygame.mixer.Sound('gamestartsoundeffect.wav')
gameoversoundeffect = pygame.mixer.Sound('gameover.wav')
gamewinsoundeffect  = pygame.mixer.Sound('gamewin.wav')
enenyexplodesoundeffect = pygame.mixer.Sound('enenyexplode.wav')
new_shootsoundeffect = pygame.mixer.Sound('new_shoot.wav')
new_gamestarsoundeffect = pygame.mixer.Sound('new_gamestartsoundeffect.wav')
new_gameoversoundeffect = pygame.mixer.Sound('new_gameover.wav')
new_gamewinsoundeffect  = pygame.mixer.Sound('new_gamewin.wav')
new_enenyexplodesoundeffect = pygame.mixer.Sound('new_enemyexplode.wav')

# Shape Control
turtle.addshape("bookfire.gif")
turtle.addshape("new_enemy.gif")
turtle.addshape("new_enemy2.gif")
turtle.addshape("spaceship.gif")
turtle.addshape("enemy.gif")
turtle.addshape("enemy2.gif")
# Cheat control value 
cheatcontrol = 1
click_hit_enemy_distance = 20
# New theme game control 
newthemegamecontrol = 0
# General parameters
window_height = 600
window_width = 600
window_margin = 50
update_interval = 25    # The screen update interval in ms, which is the
                        # interval of running the updatescreen function
# Player's parameters
player_size = 50        # The size of the player image plus margin
player_init_x = 0
player_init_y = -window_height / 2 + window_margin
player_speed = 10       # The speed the player moves left or right

# Enemy's parameters
enemy_number = 6        
enemy_size = 50         # The size of the enemy image plus margin
enemy_init_x = -window_width / 2 + window_margin
enemy_init_y = window_height / 2 - window_margin
enemy_min_x = enemy_init_x
enemy_max_x = window_width / 2 - enemy_size * enemy_number
enemy_shooting_time_interval = 1000  # Initial can be changed on (200,1000)
    # The maximum x coordinate of the first enemy, which will be used
    # to restrict the x coordinates of all other enemies
enemy_hit_player_distance = 30
    # The player will lose the game if the vertical
    # distance between the enemy and the player is smaller
    # than this value

# Enemy movement parameters
enemy_speed = 2
enemy_speed_increment = 1
    # The increase in speed every time the enemies move
    # across the window and back
enemy_direction = 1
    # The current direction the enemies are moving:
    #     1  means from left to right and
    #     -1 means from right to left

# The list of enemies and bullets
enemies = []
bullets = [] 
enemyleft = []
# Enemy bullet control
bullet_speed = 5 * cheatcontrol
bullet_hit_player_distance = 20 
# Laser parameter
laser_width = 2
laser_height = 15
laser_speed = 20
laser_hit_enemy_distance = 20
    # The laser will destory an enemy if the distance
    # between the laser and the enemy is smaller than
    # this value
def decrease_enemy_number(x,y):
    global enemy_number 
    if enemy_number>1:
        enemy_number -= 1

    # Update the display on enemy_number_text

    enemy_number_text.clear()
    enemy_number_text.write(str(enemy_number),font=("System",12,"bold"))
    
    
def increase_enemy_number(x,y):
    global enemy_number
    if enemy_number<48:
        enemy_number += 1
    enemy_number_text.clear()
    enemy_number_text.write(str(enemy_number),font=("System",12,"bold"))
    
"""
    Handle the player movement
"""
def playermoveleft():
    # Get current player position
    x, y = player.position()
    
    # Part 2.2 - Keeping the player inside the window
    # Player should only be moved only if it is within the window range
    # Limit the movement so that it always in screen 
    if x - player_speed > -window_width / 2 + window_margin:
        player.goto(x - player_speed, y)
def playermoveright():
    # Get current player position
    x, y = player.position()

    # Part 2.2 - Keeping the player inside the window
    # Player should only be moved only if it is within the window range
    # Limit
    if x + player_speed < window_width / 2 - window_margin:
        player.goto(x + player_speed, y)

def increase_enemy_shooting_time_interval():
    global enemy_shooting_time_interval
    if enemy_shooting_time_interval >= 200 and enemy_shooting_time_interval < 1000:
        enemy_shooting_time_interval += 100
turtle.onkeypress(increase_enemy_shooting_time_interval,"period")

def decrease_enemy_shooting_time_interval():
    global enemy_shooting_time_interval
    if enemy_shooting_time_interval > 200 and enemy_shooting_time_interval <= 1000:
        enemy_shooting_time_interval -= 100
turtle.onkeypress(decrease_enemy_shooting_time_interval,"comma")


"""
    Handle the screen update and enemy movement
"""

# This function is run in a fixed interval. It updates the position of all
# elements on the screen, including the player and the enemies. It also checks
# for the end of game conditions.
def updatescreen():
    # Use the global variables here because we will change them inside this
    # function
    global enemy_direction, enemy_speed
    global enemy_shooting_time_interval

    Enemyshoottimeturtle.clear()
    Enemyshoottimeturtle.write("Shoot Interval:"+" "+str(enemy_shooting_time_interval)\
                               ,font=("Italic", 10, "bold"))


    # x and y displacements for all enemies
    dx = (enemy_speed * enemy_direction)*cheatcontrol  
    dy = 0

    # Part 3.3
    # Perform several actions if the enemies hit the window border
    x0 = enemies[0].xcor()
    if x0 + dx > enemy_max_x or x0 + dx < enemy_min_x:
        # Switch the moving direction
        # If eneny_direction == -1,enemy_direction = 1 
        # And vice verse
        enemy_direction = -enemy_direction
        # Bring the enemies closer to the player
        dy = (-enemy_size/2)*cheatcontrol        
        # Increase the speed when the direction switches to right again

        if enemy_direction==1:
            enemy_speed = enemy_speed + enemy_speed_increment
    # Move the enemies according to the dx and dy values determined above
    for enemy in enemies:
        x, y = enemy.position()
        enemy.goto(x + dx, y + dy)

        if(x//20)%2==0 and newthemegamecontrol == 0:
            enemy.shape("enemy.gif")
        if(x//20)%2!=0 and newthemegamecontrol == 0:
            enemy.shape("enemy2.gif")
        if(x//20)%2==0 and newthemegamecontrol == 1:
            enemy.shape("new_enemy.gif")
        if(x//20)%2!=0 and newthemegamecontrol == 1:
            enemy.shape("new_enemy2.gif")
    # Enemy take thier bullet at the same time
    # Bullet update
    
    for bullet in bullets:
        global bullet_speed
        if bullet.isvisible()== True  :
            bullet.forward(bullet_speed*cheatcontrol)
        if bullet.ycor() < -window_height/2:
            bullet.hideturtle()
            bullets.remove(bullet)
            
    for bullet in bullets:
        if  player.isvisible() == True \
           and player.distance(bullet)< bullet_hit_player_distance :
            bullet.hideturtle()
            player.hideturtle()
            gameover(" YOU LOSE ! ")
            break
           
    
    # Part 4.3 - Moving the laser
    # Perfrom several actions if the laser is visible
    if laser.isvisible():
        laser.forward(laser_speed)
        if laser.ycor() > window_height/2:
            laser.hideturtle()
        for enemy in enemies:
            if enemy.isvisible() and laser.distance(enemy)< laser_hit_enemy_distance:
                laser.hideturtle()
                if newthemegamecontrol==0:
                    enenyexplodesoundeffect.play()
                if newthemegamecontrol==1:
                    new_enenyexplodesoundeffect.play()
                enemy.hideturtle()
                break
    # Part 5.1 - Gameover when one of the enemies is close to the player

    # If one of the enemies is very close to the player, the game will be over
    for enemy in enemies:
        if enemy.ycor()-player.ycor() < enemy_hit_player_distance \
           and enemy.isvisible() == True :
            # Show a message
            gameover(" YOU LOSE ! ")

            # Return and do not run updatescreen() again
            return

    # Part 5.2 - Gameover when you have killed all enemies

    # Set up a variable as a counter
    count = 0
    
    # For each enemy
    for enemy in enemies :
        # Increase the counter if the enemy is visible
        if enemy.isvisible():
            count=count+1

    # If the counter is 0, that means you have killed all enemies
    if count==0 : 
        # Perform several gameover actions
        gameover(" YOU WIN ! ")
        # Return and do not run updatescreen() again
        return

    # Part 3.1 - Controlling animation using the timer event

    turtle.update()   
    turtle.ontimer(updatescreen,update_interval)
    
    #
"""
    Sound effect area 
"""

def gamebeginsoundeffect():
    shootsoundeffect.play()
"""
    Shoot the laser
"""

def shoot():
    global newthemegamecontrol
    if newthemegamecontrol==0:       
        shootsoundeffect.play()
    else:
        new_shootsoundeffect.play()


    # Part 4.2 - the shooting function
    # Shoot the laser only if it is not visible
    if laser.isvisible() == False:
        # Make it visibal
        laser.showturtle()

        # Move it to the player s position 
        x, y = player.position()
        laser.goto(x,y)
"""
    Enemy attack
"""
def enemy_attack():
    global bullets
    global enemyleft 
    global enemy_shooting_time_interval
    turtle.addshape("bulletnew.gif")
    for enemy in enemies:
        if enemy.isvisible()== True and cheatcontrol==1 :
            enemyleft.append(enemy)
    if len(enemyleft)>0 and cheatcontrol==1 :
        no_of_enemy = random.randint(0,len(enemyleft)-1) 
        
        bullet = turtle.Turtle()
        bullet.hideturtle()
        if newthemegamecontrol == 0:
            bullet.shape("circle")
            bullet.shapesize(0.5,0.5,1)
            bullet.fillcolor("red")
        if newthemegamecontrol == 1:
            bullet.shape("bulletnew.gif")
            bullet.shapesize(0.5,0.5,1)          
        bullet.up()
        bullet.goto(enemyleft[no_of_enemy].xcor(),\
                    enemyleft[no_of_enemy].ycor())
        bullet.right(90)
        bullets.append(bullet)
        bullet.showturtle()
    enemyleft=[]        
    turtle.ontimer(enemy_attack,enemy_shooting_time_interval)
   
"""
    Game start
"""
def modeljudge(x,y):
    global newthemegamecontrol
    if newthemegamecontrol==0:
        gamestart()
        return newthemegamecontrol
    if newthemegamecontrol==1:
        newthemegamestart()
        return newthemegamecontrol
        
    
# This function contains things that have to be done when the game starts.
def gamestart():
    global intro_line
    global new_intro_line
    global newthemegamecontrol
    
    newthemegamecontrol=0
    gamestarsoundeffect.play()
    time.sleep(2)
    global player, laser
    global enemy_shooting_time_interval
    # Hide the introduction
    intro_line.clear()
    new_intro_line.clear()
    # Hide start button
    start_button.clear()
    start_button.hideturtle()
    new_theme_start_button.clear()
    new_theme_start_button.hideturtle()

    # Hide start button
    left_arrow.hideturtle()
    right_arrow.hideturtle()

    labels.clear()
    enemy_number_text.clear()
    #gamebeginsoundeffect()
    # recover sound effect function after finishing everything
    if enemy_number>=6:
        enemy_max_x = window_width/2 - enemy_size * 6
    else:
        enemy_max_x = window_width/2 - enemy_size * enemy_number 
    

    
    ### Player turtle ###

    # Create the player turtle and move it to the initial position
    player = turtle.Turtle()
    player.shape("spaceship.gif")
    player.up()
    player.goto(player_init_x, player_init_y)
    #enemy.goto(enemy_init_x + enemy_size * (i % 6), enemy_init_y - enemy_size * (i // 6))
    # Part 2.1
    # Map player movement handlers to key press events

    #
    # Add code here
    
    turtle.onkeypress(playermoveleft,"Left")
    turtle.onkeypress(playermoveright,"Right")
    turtle.listen()
    
    ### Enemy turtles ###

    # Add the enemy picture
    turtle.addshape("enemy.gif")

    for i in range(enemy_number):
        # Create the turtle for the enemy
        enemy = turtle.Turtle()
        enemy.shape("enemy.gif")
        enemy.up()

        # Move to a proper position counting from the top left corner
        enemy.goto(enemy_init_x + enemy_size * (i % 6), \
                   enemy_init_y - enemy_size * (i // 6))

        # Add the enemy to the end of the enemies list
        enemies.append(enemy)

    ### Laser turtle ###

    # Create the laser turtle using the square turtle shape
    laser = turtle.Turtle()
    laser.shape("square")
    laser.color("white")

    # Change the size of the turtle and change the orientation of the turtle
    laser.shapesize(laser_width / 20, laser_height / 20)
    laser.left(90)
    laser.up()

    # Hide the laser turtle
    laser.hideturtle()

    # Part 4.2 - Mapping the shooting function to key press event

    turtle.onkeypress(shoot,"space")
    turtle.listen()
    turtle.update()

    # Part 3.2 - Controlling animation using the timer event
    #turtle.ontimer(enemy_attack,enemy_shooting_time_interval)
    turtle.ontimer(enemy_attack,enemy_shooting_time_interval)  
    turtle.ontimer(updatescreen,update_interval)

"""
    Game over
"""

"""
    New theme game start
"""
# This function contains things that have to be done when the game starts.
def newthemegamestart():
    global newthemegamecontrol
    global intro_line
    global new_intro_line
    newthemegamecontrol = 1
    turtle.bgpic("BGPICNEW.gif")
    new_gamestarsoundeffect.play()
    time.sleep(2)
    global player, laser
    global enemy_shooting_time_interval
    intro_line.clear()
    new_intro_line.clear()
    start_button.clear()
    start_button.hideturtle()
    new_theme_start_button.clear()
    new_theme_start_button.hideturtle()
    left_arrow.hideturtle()
    right_arrow.hideturtle()
    labels.clear()
    enemy_number_text.clear()
    if enemy_number>=6:
        enemy_max_x = window_width/2 - enemy_size * 6
    else:
        enemy_max_x = window_width/2 - enemy_size * enemy_number 
    turtle.addshape("new_spaceship.gif")
    player = turtle.Turtle()
    player.shape("new_spaceship.gif")
    player.up()
    player.goto(player_init_x, player_init_y)  
    turtle.onkeypress(playermoveleft,"Left")
    turtle.onkeypress(playermoveright,"Right")
    turtle.listen()
    for i in range(enemy_number):
        enemy = turtle.Turtle()
        enemy.shape("new_enemy.gif")
        enemy.up()
        enemy.goto(enemy_init_x + enemy_size * (i % 6), \
                   enemy_init_y - enemy_size * (i // 6))
        enemies.append(enemy)
    laser = turtle.Turtle()
    laser.shape("bookfire.gif")
    

    # Change the size of the turtle and change the orientation of the turtle
    laser.shapesize(laser_width / 20, laser_height / 20)
    laser.left(90)
    laser.up()

    # Hide the laser turtle
    laser.hideturtle()

    # Part 4.2 - Mapping the shooting function to key press event

    turtle.onkeypress(shoot,"space")
    turtle.listen()
    turtle.update()

    turtle.ontimer(enemy_attack,enemy_shooting_time_interval)  
    turtle.ontimer(updatescreen,update_interval)

"""
    New theme game over
"""

# This function shows the game over message.
def gameover(message):
    global newthemegamecontrol
    # Part 5.3 - Improving the gameover() function
    congratuationturtle=turtle.Turtle()
    congratuationturtle.color("yellow")
    congratuationturtle.hideturtle()
    laser.hideturtle()
    player.hideturtle()
    for bullet in bullets:
        bullet.hideturtle()
    congratuationturtle.write(message,font=("System", 30, "bold"), align="center")
    turtle.update()
    if message==" YOU WIN ! " and newthemegamecontrol==0:
        gamewinsoundeffect.play()
    if message==" YOU LOSE ! "and newthemegamecontrol==0:
        gameoversoundeffect.play()
    if message==" YOU WIN ! " and newthemegamecontrol==1:
        new_gamewinsoundeffect.play()
    if message==" YOU LOSE ! "and newthemegamecontrol==1:
        new_gameoversoundeffect.play()

"""

    Set up main Turtle parameters
"""

# This is cheat mode , use "s" to run it

def cheat_stopenemy():
    global cheatcontrol
    if cheatcontrol==1:
        cheatcontrol=0
    else:
        cheatcontrol=1
turtle.onkeypress(cheat_stopenemy,"s")
turtle.listen()


def cheat_mousekillthem(x,y):
    global enemy
    if cheatcontrol==0:
        for enemy in enemies:    
            if enemy.isvisible() == True\
               and enemy.distance(x,y) < click_hit_enemy_distance :
                enemy.hideturtle()
        for bullet in bullets:
            if bullet.isvisible() == True\
               and bullet.distance(x,y) < click_hit_enemy_distance :
                bullet.hideturtle()
turtle.onscreenclick(cheat_mousekillthem)

# Enemy shooting time interval display turtle
Enemyshoottimeturtle = turtle.Turtle()
Enemyshoottimeturtle.hideturtle()
Enemyshoottimeturtle.color("white","white")
Enemyshoottimeturtle.up()
Enemyshoottimeturtle.goto(130,280)


# Set up the turtle window
turtle.setup(window_width, window_height)
turtle.bgcolor("black")
turtle.bgpic("BGPIC.gif")
turtle.up()
turtle.hideturtle()
turtle.tracer(False)

# Give introduction to player
intro_line = turtle.Turtle()
intro_line.hideturtle()
intro_line.color("yellow","yellow")
intro_line.up()
intro_line.goto(0,180)
intro_line.write("Python", font=("Arial", 50, "bold"), align="center")
intro_line.goto(0,110)
intro_line.write("Space Invaders", font=("Arial", 50, "bold"), align="center")
intro_line.goto(0,30)
intro_line.write("Control your spaceship", font=("Times", 30, "bold"), align="center")
intro_line.goto(0,intro_line.ycor()-40)
intro_line.write("using the arrow keys", font=("Times", 30, "bold"), align="center")
intro_line.goto(0,intro_line.ycor()-40)
intro_line.write("and spacebar to shoot", font=("Times", 30, "bold"), align="center")
intro_line.goto(0,intro_line.ycor()-40)
intro_line.write("and kill the aliens !", font=("Times", 30, "bold"), align="center")

# Start the start button
start_button = turtle.Turtle()
start_button.onclick(modeljudge)

start_button.up()
start_button.goto(-40, -40-160)
start_button.color("yellow", "DarkGray")
start_button.begin_fill()
for _ in range(2):
    start_button.forward(80)
    start_button.left(90)
    start_button.forward(25)
    start_button.left(90)
start_button.end_fill()

start_button.color("yellow")
start_button.goto(0, -35-160)
start_button.write("START", font=("System", 15, "bold"), align="center")

# Reshape turtle icon to cover the whole button
start_button.goto(0,-28-160)
start_button.shape("square")
start_button.shapesize(1.25,4)
start_button.color("")

################################
new_intro_line = turtle.Turtle()
new_intro_line.hideturtle()
def newthemegameintroduction(x,y):
    global newthemegamecontrol
    global new_intro_line
    global intro_line
    if newthemegamecontrol == 0:
        newthemegamecontrol=1
        new_intro_line.clear()
        intro_line.clear()
        turtle.bgpic("BGPICNEW.gif")
        intro_line.clear()
        new_theme_start_button.hideturtle()
        enemy_number_text.clear()
        labels.clear()
        labels.write("Number of Enemies:", font=("System", 12, "bold"))
        #new_intro_line = turtle.Turtle()
        new_intro_line.hideturtle()
        new_intro_line.color("yellow","yellow")
        new_intro_line.up()
        new_intro_line.goto(0,180)
        new_intro_line.write("Python", font=("Arial", 40, "bold"), align="center")
        new_intro_line.goto(0,110)
        new_intro_line.write("Magic World Protection", font=("Arial", 35, "bold"), align="center")
        new_intro_line.goto(0,30)
        new_intro_line.write("Move your magical book", font=("Times", 30, "bold"), align="center")
        new_intro_line.goto(0,-10)
        new_intro_line.write("using the arrow keys and", font=("Times", 30, "bold"), align="center")
        new_intro_line.goto(0,-50)
        new_intro_line.write("spacebar to release magical", font=("Times", 30, "bold"), align="center")
        new_intro_line.goto(0,-90)
        new_intro_line.write("light and kill the devils !", font=("Times", 30, "bold"), align="center")
        enemy_number_text.write(str(enemy_number), font=("System", 12, "bold"), align="center")
        return newthemegamecontrol
    if newthemegamecontrol == 1:
        newthemegamecontrol=0
        new_intro_line.clear()
        intro_line.clear()
        turtle.bgpic("BGPIC.gif")
        intro_line.clear()
        new_theme_start_button.hideturtle()
        enemy_number_text.clear()
        labels.clear()
        labels.write("Number of Enemies:", font=("System", 12, "bold"))
        new_intro_line = turtle.Turtle()
        new_intro_line.hideturtle()
        new_intro_line.color("yellow","yellow")
        new_intro_line.up()
        new_intro_line.goto(0,180)
        new_intro_line.write("Python", font=("Arial", 50, "bold"), align="center")
        new_intro_line.goto(0,110)
        new_intro_line.write("Space Invaders", font=("Arial", 50, "bold"), align="center")
        new_intro_line.goto(0,30)
        new_intro_line.write("Control your spaceship", font=("Times", 30, "bold"), align="center")
        new_intro_line.goto(0,-10)
        new_intro_line.write("using the arrow keys", font=("Times", 30, "bold"), align="center")
        new_intro_line.goto(0,-50)
        new_intro_line.write("and spacebar to shoot", font=("Times", 30, "bold"), align="center")
        new_intro_line.goto(0,-90)
        new_intro_line.write("and kill the aliens !", font=("Times", 30, "bold"), align="center")
        enemy_number_text.write(str(enemy_number), font=("System", 12, "bold"), align="center")
        return newthemegamecontrol





new_theme_start_button = turtle.Turtle()
new_theme_start_button.onclick(newthemegameintroduction)
new_theme_start_button.up()
new_theme_start_button.goto(-40, -40-200)
new_theme_start_button.color("yellow", "DarkGray")
new_theme_start_button.begin_fill()

for _ in range(2):
    new_theme_start_button.forward(80)
    new_theme_start_button.left(90)
    new_theme_start_button.forward(25)
    new_theme_start_button.left(90)
new_theme_start_button.end_fill()

new_theme_start_button.color("yellow")
new_theme_start_button.goto(0, -35-200)
new_theme_start_button.write("Swith Theme", font=("System", 15, "bold"), align="center")

new_theme_start_button.goto(0,-28-200)
new_theme_start_button.shape("square")
new_theme_start_button.shapesize(1.25,4)
new_theme_start_button.color("")
################################


# Set up other controls
labels=turtle.Turtle()
labels.hideturtle()
labels.pencolor("yellow")
labels.up()
labels.goto(-100, 0-160) # Put the text next to the spinner control
labels.write("Number of Enemies:", font=("System", 12, "bold"))

enemy_number_text=turtle.Turtle()
enemy_number_text.hideturtle()
enemy_number_text.pencolor("yellow")
enemy_number_text.up()

enemy_number_text.goto(80,0-160)
enemy_number_text.write(str(enemy_number), font=("System", 12, "bold"), align="center")

# Arrow button
left_arrow=turtle.Turtle()
left_arrow.shape("arrow")
left_arrow.color("yellow")
left_arrow.shapesize(0.5,1)
left_arrow.lt(180)
left_arrow.up()
left_arrow.goto(60,8-160)

right_arrow=turtle.Turtle()
right_arrow.shape("arrow")
right_arrow.color("yellow")
right_arrow.shapesize(0.5,1)
right_arrow.up()
right_arrow.goto(100,8-160)


left_arrow.onclick(decrease_enemy_number)
right_arrow.onclick(increase_enemy_number)

turtle.listen()
turtle.update()

# Switch focus to turtle graphics window
turtle.done()
