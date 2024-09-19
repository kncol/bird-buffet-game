# Import pygame so the game will and all functions work
import pygame
# Import this to make sure the game quits all the way at the end
import sys
# Import random for the variable that get respawned after being hit
import random
# Begin to run the actual game 
pygame.init()

###################################################################
# Import music of the game

from pygame import mixer
mixer.init()
mixer.music.load('Chill.mp3')
mixer.music.play()


###################################################################
# This is for the basic window set up

screen_width = 600
screen_height = 600
# This sets the game state, so that you can switch menus (it basically just redraws the screen and the function displayed, hence a new menu)
# This was an idea that was inspired by the website in "README" and very helpful for making my menus
game_current_state = "intro_menu"

###################################################################
# Create the actual screen
screen = pygame.display.set_mode((screen_width, screen_height))
# Name the actual screen
pygame.display.set_caption("Bird Buffet")

# Import all the images needed

backgroud = pygame.image.load ("Background.jpg")
backgroud2 = pygame.image.load ("Background2.jpg")
backgroud3 = pygame.image.load ("Background3.jpg")
backgroud4 = pygame.image.load ("Background4.jpg")
Snow1 = pygame.image.load ("Snow1.png")
Snow2 = pygame.image.load ("Snow2.png")
Snow3 = pygame.image.load ("Snow3.png")
Snow4 = pygame.image.load ("Snow4.png")
bird_img = pygame.image.load("Bird_Art.png")
worm_img = pygame.image.load("Worm_Art2.png")
cat_img = pygame.image.load("Cat_Art3.png")
frog_img = pygame.image.load("Frog.png")
puddle_img = pygame.image.load("Puddle.png")
roberson_img = pygame.image.load("Roberson.png")
cazalas_img = pygame.image.load("Cazalas.png")
santa_bird_img = pygame.image.load("Santa_Bird.png")
one_flower = pygame.image.load("1Flower.png")
two_flower = pygame.image.load("2Flowers.png")
three_flower = pygame.image.load("3Flowers.png")
snow_flake = pygame.image.load("Snow_Flake.png")

# Scale all the images to correct size in game
cazalas_display = pygame.transform.scale(cazalas_img,(200,200))
cazalas_art = pygame.transform.scale(cazalas_img,(100,100))
roberson_display = pygame.transform.scale(roberson_img,(200,200))
roberson_art = pygame.transform.scale(roberson_img,(100,100))
cat_art = pygame.transform.scale(cat_img,(150,150))
puddle_art = pygame.transform.scale(puddle_img, (75,75))
frog_art = pygame.transform.scale(frog_img,(50,50))
worm_art = pygame.transform.scale(worm_img,(50,50))
bird_art = pygame.transform.scale(bird_img,(100,100))
bird_display = pygame.transform.scale(bird_img,(200,200))
santa_art = pygame.transform.scale(santa_bird_img,(100,100))
santa_display = pygame.transform.scale(santa_bird_img,(250,250))
single = pygame.transform.scale(one_flower,(200,200))
double = pygame.transform.scale(two_flower,(200,200))
triple = pygame.transform.scale(three_flower,(200,200))
snow = pygame.transform.scale(snow_flake,(100,100))

###################################################################
# Define the rectangle used for the bird
bird_state = "original"
background_state = "original"
 # Create a class for the moving bird and all it's functions
class Birdie():
    def __init__(self,x,y):
        # Create the bird's rectangle that will be the actual object
        self.width = 75
        self.height = 75
        self.bird_x = 300
        self.bird_y = 300
        self.rect = pygame.Rect(self.bird_x, self.bird_y, self.width, self.height)
        self.rect.center = (x,y)


    def move_bird(self):
        # Determine what key is being pressed and control whether the bird goes up or down
        key = pygame.key.get_pressed()
        # If the corresponding key is pressed, and the bird is still within the game screen, the bird will go in that direction by 4 increments
        if key[pygame.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= 4
        # The rectangle for the bird(self) cannot pass the screenwidth (including it's body size in that calculation)
        if key[pygame.K_RIGHT] and self.rect.x <= screen_width - self.width:
            self.rect.x += 4
        if key[pygame.K_UP] and self.rect.y >= 0:
            self.rect.y -= 4
        if key[pygame.K_DOWN] and self.rect.y <= screen_height - self.height:
            self.rect.y += 4

    def speedyboy(self):
        # When the bird touches the puddle/powerup (determined further down in code) speed the bird up by 1
        key = pygame.key.get_pressed()
        # If the corresponding key is pressed, and the bird is still within the game screen, the bird will go in that direction by 5 increments
        if key[pygame.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= 5
        if key[pygame.K_RIGHT] and self.rect.x <= screen_width - self.width:
            self.rect.x += 5
        if key[pygame.K_UP] and self.rect.y >= 0:
            self.rect.y -= 5
        if key[pygame.K_DOWN] and self.rect.y <= screen_height - self.height:
            self.rect.y += 5


    def draw_birdie(self):
        # Draw/ blit the actual image of the bird on the rectangle/ these will be determined on the bird_state that on the customization pages
        if bird_state == "original": 
            screen.blit(bird_art, (self.rect.x, self.rect.y))
        if bird_state == "roberson":
            screen.blit(roberson_art, (self.rect.x, self.rect.y))
        if bird_state == "cazalas":
            screen.blit(cazalas_art, (self.rect.x, self.rect.y))
        # This bird_state is only available on the "customization2" menu while the other three are only available on the "customizatin1" menu
        if bird_state == "Santa":
            screen.blit(santa_art,(self.rect.x, self.rect.y))
           
###################################################################
# Get a counter for how much prey the user collects
counter = 0
# Variabel to hold string that states why the bird resets (either win or loses)
reason = ""
# worm_art = pygame.image.load('Worm_Art.png').convert_alpha()
# Define the worm's rectangle

worm1_width = 25
worm1_height = 25
worm1_x = random.randint(50,550)
worm1_y = random.randint(50,550)
worm1 = pygame.Rect(worm1_x, worm1_y, worm1_width, worm1_height)

###################################################################
# Define the frog's rectangle

frog_width = 25
frog_height = 25
frog_x = random.randint(50,550)
frog_y = random.randint(50,550)
frog = pygame.Rect(frog_x, frog_y, frog_width, frog_height)

###################################################################
# Make a class for the puddle/powerup which speeds up the user
class PowerUp():
    
    def __init__(self, x, y):
        # Power up for increase speed for a certian time that appears randomly anywhere around screen
        self.width = 75
        self.height = 75
        self.power_x = random.randint(75,525)
        self.power_y = random.randint(75,525)
        self.rect = pygame.Rect(self.power_x, self.power_y, self.width, self.height)
        self.rect.center = (x,y)

    def move(self):
        # Moves the puddle to a random location on screen
        powerup.power_x = random.randint(75,525)
        powerup.power_x = random.randint(75,525)

    def draw_powerup(self):
        # Draws the image of the puddle on the rectangle
        screen.blit(puddle_art, (self.rect.x, self.rect.y))
###################################################################
# Get the pygame font for the next text
text_font = pygame.font.SysFont("monospace", 30)

# This will be the function that draws the score on the screen during the game
def draw_text(text, font, text_color, x, y):
    img = font.render(text,True, text_color)
    screen.blit(img, (x, y))

# This class is for drawing the image of the Roberson Bird on the screen in customization
class Roberson():
    
    def __init__(self, x, y):
        # Power up for increase speed for a certian time that appears randomly anywhere around screen
        self.width = 75
        self.height = 75
        self.x = 100
        self.y = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.width)
        self.rect.center = (x,y)
    # Draw/blit the image of the Roberson Bird ontop of the rectangle
    def draw_roberson(self):
        screen.blit(roberson_display, (self.rect.x, self.rect.y))

# This class is for drawing the image of the Cazalas Bird on the screen in customization
class Cazalas():
    
    def __init__(self, x, y):
        # Power up for increase speed for a certian time that appears randomly anywhere around screen
        self.width = 75
        self.height = 75
        self.x = 100
        self.y = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.width)
        self.rect.center = (x,y)
    # Draw/blit the image of the Cazalas Bird ontop of the rectangle
    def draw_cazalas(self):
        screen.blit(cazalas_display, (self.rect.x, self.rect.y))

# This class is for drawing the image of the Santa Bird on the screen in customization
class Santa():
    
    def __init__(self, x, y):
        # Power up for increase speed for a certian time that appears randomly anywhere around screen
        self.width = 75
        self.height = 75
        self.x = 100
        self.y = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.width)
        self.rect.center = (x,y)
    # Draw/blit the image of the Santa Bird ontop of the rectangle
    def draw_Santa(self):
        screen.blit(santa_display, (self.rect.x, self.rect.y))


###################################################################
# This is the class for the cat obstacle
class Cat():
    def __init__(self, x, y):

        self.width = 140
        self.height = 125
        self.cat_x = -200
        self.cat_y = random.randint(50,550)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)
        self.speed = 4
    def move(self):
        # This will move the cat to the right
        self.rect.x += self.speed
        # This will reset the cats placement whenever it passes the width of the screen
        if self.rect.x > screen_width:
            self.rect.x = -200
            self.rect.y = random.randint(50,550)
        # This if-else statment will continue to increase the cats speed at ten seconds, twenty seconds, and thirty seconds
        if ongoing_time - current_time >= 10000:
            self.speed = 6
        elif ongoing_time - current_time >= 20000:
            self.speed = 8
        elif ongoing_time - current_time >= 30000:
            self.speed = 10
    # Draw/blit the image of the cat ontop of the rectangle
    def draw_cat(self):
        screen.blit(cat_art, (self.rect.x, self.rect.y))

###################################################################

# Set up the time
clock = pygame.time.Clock()

###################################################################
# Make variables so that the classes and their functions can be called
cat = Cat(0,random.randint(50,550))
birdie = Birdie(300,300)
powerup = PowerUp(random.randint(50, 550), random.randint(50,500))
roberson = Roberson(235, 200)
cazalas = Cazalas(430, 200)
santa = Santa(200,200)

# Loop for the entire game until quit (This is the actual game loop)
while True:
    # This is said in the beginning so that closing the game (not throught the quit function) still occurs
    for event in pygame.event.get():
        # function to quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            # This sys.exit() function is to ensure that the game will close out all the way if pygame.quit() does not close all
            sys.exit()

######################################################################################################################################
    # This is the first menu the user will encounter when starting the game and directly leads to both the "game" and "customization" menus
    if game_current_state == "intro_menu":
        # The screen.fill makes the background color and the rest creates the text that will be displayed (Adds the font, color, and what it will say)
        screen.fill((109,203,108))
        font = pygame.font.SysFont('monospace', 35)
        title_font = pygame.font.SysFont('monospace', 80)
        title = title_font.render('Bird Buffet', True, (125,76,48))
        custom = font.render('Customization (C)', True, (125,76,48))
        start_button = font.render('Press Space Key to Start', True, (125,76,48))

        # Draws/blits both text and images onto the main menu
        screen.blit(triple,(0,0))
        screen.blit(double,(400,350))
        screen.blit(single,(0,450))
        screen.blit(title, (screen_width/2 - title.get_width()/2, 175))
        screen.blit(custom, (screen_width/2 - custom.get_width()/2, 275))
        screen.blit(start_button, (screen_width/2 - start_button.get_width()/2, 325))

        # Reset cat variables whenever you get back to the menu so that the score and reason can be displayed on the game_over menu
        cat.cat_x = -200
        cat.cat_y = random.randint(50,550)
        cat.rect = pygame.Rect(0, 0, cat.width, cat.height)

        # Redraws the bird so that it does not respawn where the user left off (this can lead get spawn killed if ending on the right side)
        birdie.rect = pygame.Rect(birdie.bird_x,birdie.bird_y,birdie.width,birdie.height)

        # Reset the final score
        final_score = 0
        counter = 0
        # Update the screen with the pygame update function
        pygame.display.update()

        # When space is pressed, change the current state of the game to "game" and recognize the space bar has been pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_current_state = "game"
            # Get the single time (instance being space bar pressed) to subtract the running game time with so that you can end at certain times multiple play throughs
            current_time = pygame.time.get_ticks()

        # Go to the customization menu if 'c' is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_c]:
            game_current_state = "customization"
    # This menu is achieved only through the game menu after colliding with the cat or dodging it reaches 40 seconds. This is the only menu that a button allows you to quit (without going outside of the game to close it)
    elif game_current_state == "game_over":
        # The screen.fill makes the background color and the rest creates the text that will be displayed (Adds the font, color, and what it will say)
        screen.fill((109,203,108))
        font = pygame.font.SysFont('monospace', 40)
        big_font = pygame.font.SysFont('monospace', 80)
        title = big_font.render('Game Over', True, (125,76,48))
        message = font.render("{}".format(reason), True, (125,76,48))
        final_score = font.render("Final Score: {}".format(counter), True, (125,76,48))
        restart_button = font.render('Restart (R)', True, (125,76,48))
        quit_button = font.render('Quit (Q)', True, (125,76,48))

        # Draws/blits both text and images onto the main menu
        screen.blit(single,(400,200))
        screen.blit(double,(0,400))
        screen.blit(triple,(0,0))
        screen.blit(title, (screen_width/2 - title.get_width()/2, 100))
        screen.blit(message,(screen_width/2 - message.get_width()/2, 200))
        screen.blit(final_score, (screen_width/2 - restart_button.get_width()/1.6,240))
        screen.blit(restart_button, (screen_width/2 - restart_button.get_width()/2, 340))
        screen.blit(quit_button, (screen_width/2 - quit_button.get_width()/2, 380))
        # Update the screen with the pygame update function
        pygame.display.update()

        # Return to the menu if the user presses 'r'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_current_state = "intro_menu"
        # Quit out of the game entirely if the user presses 'q'
        if keys[pygame.K_q]:
           pygame.quit()
           quit()

###################################################################
    # This is the menu that is available after clicking 'c' on the main menu
    elif game_current_state == "customization":
        # The screen.fill makes the background color and the rest creates the text that will be displayed (Adds the font, color, and what it will say)
        screen.fill((109,203,108))
        font = pygame.font.SysFont('monospace', 35)
        smaller_font = pygame.font.SysFont('monospace', 25)
        smallest_font = pygame.font.SysFont('monospace',20)
        custom_menu = font.render('Game Customization Page 1', True, (125,76,48))
        back = smallest_font.render('Go Back to Menu(B)', True, (125,76,48))
        forward = smallest_font.render('Next Custom Page(M)', True, (125,76,48))
        screen.blit(custom_menu, (screen_width/2 - custom_menu.get_width()/2, 75))

        # Draws/blits both text and images onto the main menu
        screen.blit(back, (10, 550))
        screen.blit(forward,(360,550))
        screen.blit(bird_display, (0,165))
        # Call the draw functions from the class variables
        roberson.draw_roberson()
        cazalas.draw_cazalas()
        number1 = smaller_font.render('Press 1', True, (125,76,48))
        number2 = smaller_font.render('Press 2', True, (125,76,48))
        number3 = smaller_font.render('Press 3', True, (125,76,48))
        screen.blit(number1, (65, 350))
        screen.blit(number2, (260, 350))
        screen.blit(number3, (455, 350))

        # Make the bird a certain "state"/ skin whenever the user presses the correlating number 1-3
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            bird_state = "original"
            # Since there is a "Christmas" background_state, make sure to keep the background consistent for the other birds
            background_state = "original"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_2]:
            bird_state = "roberson"
            background_state = "original"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_3]:
            bird_state = "cazalas"
            background_state = "original"
        # Update the screen with the pygame update function
        pygame.display.update()
        # Go back to the menu if the user presses 'b'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            game_current_state = "intro_menu"
        # Go to the next customization page if the user presses 'm'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            game_current_state = "customization2"

###################################################################
    # This is the second customization page when pressing the 'm' key on the "customization1" menu (this is basically the Christmas-themed page)
    elif game_current_state == "customization2":
        # The screen.fill makes the background color and the rest creates the text that will be displayed (Adds the font, color, and what it will say)
        screen.fill((0,135,62))
        font = pygame.font.SysFont('monospace', 35)
        smaller_font = pygame.font.SysFont('monospace', 25)
        smallest_font = pygame.font.SysFont('monospace',20)
        custom_menu = font.render('Game Customization Page 2', True, (125,10,10))
        back = smallest_font.render('Go Back to Menu(B)', True, (125,10,10))
        forward = smallest_font.render('Previous Custom Page(N)', True, (125,10,10))
        number4 = smaller_font.render('Press 4', True, (125,10,10))

        # Draws/blits both text and images onto the main menu
        screen.blit(snow,(0,250))
        screen.blit(snow,(120,100))
        screen.blit(snow,(460,300))
        screen.blit(snow,(100,400))
        screen.blit(snow,(400,140))
        screen.blit(snow,(400,425))
        screen.blit(custom_menu, (screen_width/2 - custom_menu.get_width()/2, 75))
        screen.blit(back, (10, 550))
        screen.blit(number4, (240, 425))
        screen.blit(forward,(320,550))
        # Call the draw functions from the class variables
        santa.draw_Santa()

        # if the user presses 4, this will customize both the bird and background
        keys = pygame.key.get_pressed()
        if keys[pygame.K_4]:
            bird_state = "Santa"
            background_state = "Christmas"
        # Update the screen with the pygame update function
        pygame.display.update()
         # Go back to the menu if the user presses 'b'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_b]:
            game_current_state = "intro_menu"
        # Go to the next customization page if the user presses 'm' 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            game_current_state = "customization"
        # Both customization menu buttons where going to be 'n', but pygame sometimes takes the press as holding and would change quickly to the customization1 menu)
######################################################################################################################################
    # This is the actual game itself, achieved after pressing space on the main menu and leads to the end_game menu after getting caught by the cat or surviving the cat after 4 seconds
    elif game_current_state == "game":
        # Create the background color
        if background_state == "original":
            screen.blit(backgroud,(0,0))
        elif background_state == "Christmas":
            screen.blit(Snow1,(0,0))
        
        # Countinously check the current time of the game
        ongoing_time = pygame.time.get_ticks()
        # Change Background as it gets closer to nighttime aka 30 seconds by subtracting the current time by the time gotten after pressing space and starting the game
        if background_state == "original":
            if ongoing_time - current_time >= 30000:
                screen.blit(backgroud2,(0,0))
            if ongoing_time - current_time >= 35000:
                screen.blit(backgroud3,(0,0))  
            if ongoing_time - current_time >= 38000:
                screen.blit(backgroud4,(0,0))
        # Draw/blit a different image to the screen if the background state is Christmas   
        elif background_state == "Christmas":
            if ongoing_time - current_time >= 30000:
                screen.blit(Snow2,(0,0))
            if ongoing_time - current_time >= 35000:
                screen.blit(Snow3,(0,0))  
            if ongoing_time - current_time >= 38000:
                screen.blit(Snow4,(0,0)) 

        # Consider making a key where the x and y equal something so the bird can teleport and give the game a bit more competitive feeling
        # Make the counter visible on screen
        draw_text("Score: {}".format(counter), text_font, ('black'), 425, 10)
            
        # Now check whether the bird will run into the worm with pygame function and redraw it somewhere else
        if birdie.rect.colliderect(worm1):
            # Add 1 count to the score if they collide
            counter += 1
            worm1_x = random.randint(50,550)
            worm1_y = random.randint(50,550)
            worm1 = pygame.Rect(worm1_x, worm1_y, worm1_width, worm1_height)

    ###################################################################
        # Now check whether the bird will run into the frog with pygame function and redraw it somewhere else
        if birdie.rect.colliderect(frog):
            # Add 2 count to the score if they collide
            counter += 2
            frog_x = random.randint(50,550)
            frog_y = random.randint(50,550)
            frog = pygame.Rect(worm1_x, frog_y, frog_width, frog_height)

    ###################################################################
        # Redraw the frog and worm on screen if they are overlapping when respawned
        if worm1.colliderect(frog):
            counter += 1
            frog_x = random.randint(50,550)
            frog_y = random.randint(50,550)
            frog = pygame.Rect(worm1_x, frog_y, frog_width, frog_height)
            worm1_x = random.randint(50,550)
            worm1_y = random.randint(50,550)
            worm1 = pygame.Rect(worm1_x, worm1_y, worm1_width, worm1_height)
        # Call the functions if the bird goes over the puddle
        if birdie.rect.colliderect(powerup.rect):
            birdie.speedyboy()
            powerup.move()
        # End the game and show that the user ran into the cat if the bird and cat collide
        if cat.rect.colliderect(birdie.rect):
            reason = "Oh no! The cat got you!"
            game_current_state = "game_over"

    ###################################################################

        #pygame.draw.rect(screen,brown, worm1)
        powerup.draw_powerup()

        screen.blit(worm_art, worm1)
        screen.blit(frog_art, frog)
        # Draw 
        cat.draw_cat()
        cat.move()
        # Draw the bird and the moving bird
        birdie.draw_birdie()
        birdie.move_bird()

        # if time is equal to or exceeds 40 seconds
        if 40000 <= ongoing_time - current_time:
            # print "game end"
            game_current_state = "game_over"
            reason = "Congrats! You win!"
        # Update what the screen displays whenever player move
        pygame.display.update()

        #takes anything thats drawn in while loop and draws it
        pygame.display.flip()

    clock.tick(60)