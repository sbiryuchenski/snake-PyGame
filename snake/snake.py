import pygame
import random
import time
#import os.path
pygame.font.init()

ver = "0.4.5" 

#1 Костыль. UP это ВНИЗ, а DOWN это я по ходу....
#2 Блять, я теперь буду писать комментарии, обещаю


##########

##########

score = 0
score2 = 0
bestscore = 0

#settings
window = 500
sizeofsnake = 10 #size of squares of snakes body
fps = 60#if you setting fps higher don't forget make step slower. ect: fps 60 - step 3, fps 120 - step 2, fps 180 - step 1. maxfps = 180. 
step = 3
speed = 1#you can choose speed of snake: 1x 2x 3x ect. if > 3 correct working not guaranted

secbegx = 0
secbegy = 0

#directions
RIGHT = "r"
LEFT = "l"
DOWN = "d"
UP = "u"
dir = RIGHT
dir2 = LEFT
speedup = False
speedup2 = False

#params
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0 , 0]
BLUE = [0, 0, 255]
alive = True
restart = False
width = window
height = window
looser = 0


#initialization game
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Гадюка")
clock = pygame.time.Clock()

#initialization shit
font = pygame.font.SysFont('comicsans', 50)
fontsmall = pygame.font.SysFont(None, 20)
scoretext = font.render(str(score), 1, WHITE)
bestscoretext = fontsmall.render(str(bestscore), 1, WHITE)
bestscoretext1 = fontsmall.render("Best: ", 1, WHITE)
pausetext = font.render("PAUSE", 1, WHITE)
menutext1 = font.render("Press any key to start", 1, WHITE)
menutext2 = fontsmall.render("USE ARROWS TO CONTROL YOU SNAKE", 1, WHITE)
menutext3 = fontsmall.render("PRESS SPACE TO SPEED UP, PRESS R TO RESTART", 1, WHITE)
version = fontsmall.render("ver " + str(ver) + " pre alpha", 1, WHITE)
imgbody = pygame.image.load('images/body.png').convert_alpha()
imgbody2 = pygame.image.load('images/body2.png').convert_alpha()
imgfone = pygame.image.load('images/fone.png').convert_alpha()
imghead_l = pygame.image.load('images/head.png').convert_alpha()
imghead_r = pygame.transform.rotate(imghead_l, 180)
imghead_u = pygame.transform.rotate(imghead_l, 270)
imghead_d = pygame.transform.rotate(imghead_l, 90)
imghead_l2 = pygame.image.load('images/head2.png').convert_alpha()
imghead_r2 = pygame.transform.rotate(imghead_l2, 180)
imghead_u2 = pygame.transform.rotate(imghead_l2, 270)
imghead_d2 = pygame.transform.rotate(imghead_l2, 90)
imgapple = pygame.image.load('images/apple.png').convert_alpha()
imgabout = pygame.image.load('images/about.png').convert_alpha()
imgsingle = pygame.image.load('images/single.png').convert_alpha()
imgmulti = pygame.image.load('images/multi.png').convert_alpha()
imgsoon = pygame.image.load('images/soon.png').convert_alpha()
imgcomeback = pygame.image.load('images/comeback.png').convert_alpha()
imgab = pygame.image.load('images/aboutimg.png').convert_alpha()
imgexit = pygame.image.load('images/exit.png').convert_alpha()
imgexyes = pygame.image.load('images/exyes.png').convert_alpha()
imgexno = pygame.image.load('images/exno.png').convert_alpha()
imgstartyes = pygame.image.load('images/startyes.png').convert_alpha()
imgstartno = pygame.image.load('images/startno.png').convert_alpha()
menuchoise = [imgsingle, imgmulti, imgabout, imgexit]

blindlist = []
for i in range(10):
    blindlist.append(pygame.image.load('images/blind/blind'+str(i+1)+'.png').convert_alpha())

sparklesanim = []
for i in range(19):
    sparklesanim.append(pygame.image.load('images/sparkles/fire (' + str(i) + ').png').convert_alpha())
    sparklesanim[i] = pygame.transform.scale(sparklesanim[i], (300, 300))
sparklesanim = sparklesanim * 2


applelist = [[250, 250, True]]

twoxlist = []
for x in range(38):
    path = str('images/2x/'+str(x+1)+'.png')
    twoxlist.append(pygame.image.load(path))
threelist = []
for x in range(38):
    path = str('images/3x/'+str(x+1)+'.png')
    threelist.append(pygame.image.load(path))

snotec = pygame.mixer.Sound('sounds/C.wav')
snotee = pygame.mixer.Sound('sounds/E.wav')
snoteg = pygame.mixer.Sound('sounds/G.wav')
snotec2 = pygame.mixer.Sound('sounds/C2.wav')
auch1 = pygame.mixer.Sound('sounds/auch1.wav')
auch2 = pygame.mixer.Sound('sounds/auch2.wav')
auch3 = pygame.mixer.Sound('sounds/auch3.wav')
chord1 = pygame.mixer.Sound('sounds/chord1.wav')
chord2 = pygame.mixer.Sound('sounds/chord2.wav')
chord3 = pygame.mixer.Sound('sounds/chord3.wav')
chord4 = pygame.mixer.Sound('sounds/chord4.wav')



sbitelist = []
for i in range(7):
    sbitelist.append(pygame.mixer.Sound('sounds/bite' + str(i+1) + '.wav'))
    sbitelist[i].set_volume(0.5)

chordlist = [chord1, chord2, chord3, chord4]
#GACHI
swelcome = pygame.mixer.Sound('sounds/GYM/welcome.wav')
orgasmlist = []
for i in range(4):
    orgasmlist.append(pygame.mixer.Sound('sounds/GYM/orgasm'+str(i)+'.wav'))

appleOrgasmList = [pygame.mixer.Sound('sounds/GYM/orgasm2.wav'), pygame.mixer.Sound('sounds/GYM/orgasm3.wav')] # Sound when takes a bonus 5 apples

gymsoumdslist = []
for i in range(12):
    gymsoumdslist.append(pygame.mixer.Sound('sounds/GYM/srandom'+str(i)+'.wav'))
#gachi

auchlist = [auch1, auch2, auch3]
notelist = []
bitelist = []
for n in range(50):
    notelist.append(random.choice([snotec, snotee, snoteg, snotec2]))
    bitelist.append(random.choice([sbitelist[0], sbitelist[1], sbitelist[2], sbitelist[3], sbitelist[4], sbitelist[5], sbitelist[6]]))

firstrun = True
run = True
menu = True
pause = False

bonusTime = 1600 # Time of bonus collecting
appleRealSize = 10 # Eating range of apple
m=3000
n=0
seconder = False
booster = 0
koef = 13
animtwox = 0
animtwoxhelp = 0
animsparkles = 1
gym = False
g = False
y = False
d = False
e = False
mgym = False
hello = True
abouter = False
headbump = False
alive = False
exchoise = False
exitask = False
comebacker = False
exitt = False
newgamescreen = False
choisenew = True
blind = False
b = 0
applecounter = 0

DEV_MODE = False # Developer mode. Ввести dev во в меню. Змея становится бессмертной, змее проще попасть в яблоки, на достижение комбо даётся 5 секунд вместо 1,6 секунды в обычном режиме

while run:
    n+=1
    if menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                abouter = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if alive:
                    menu = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                exchoise = not exchoise
                choisenew = not choisenew
                notelist[n%50].play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                exchoise = not exchoise
                choisenew = not choisenew
                notelist[n%50].play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                g = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                if g:
                    y = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if y:
                    mgym = True
            #///////////////////////////DEVELOPER MODE//////////////////////////////
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                d = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if d:
                    e = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                if e:
                    DEV_MODE = True
                    bonusTime = 5000
                    appleRealSize = 25
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and not exitask:
                m+=1
                notelist[n%50].play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not exitask:
                m-=1
                notelist[n%50].play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if m%4 == 0:
                    if alive:
                        if newgamescreen == False:
                            newgamescreen = True
                        else:
                            if choisenew:
                                seconder = False
                                menu = False
                                alive = True
                                firstrun = True
                                newgamescreen = False
                            else:
                                newgamescreen = False
                    else:
                        seconder = False
                        menu = False
                        alive = True
                        firstrun = True
                        newgamescreen = False

                if m%4 == 1:
                     if alive:
                         if newgamescreen == False:
                            newgamescreen = True
                         else:
                            if choisenew:
                                seconder = True
                                menu = False
                                alive = True
                                firstrun = True
                                gym = False
                                newgamescreen = False
                            else:
                                newgamescreen = False
                     else:
                         seconder = True
                         menu = False
                         alive = True
                         firstrun = True
                         gym = False
                         newgamescreen = False
                if m%4 == 2:
                    abouter = True

                if exitask == False:
                    if m%4 == 3:
                        exitask = True
                else:
                    if exchoise:
                        screen.blit(imgcomeback, (0, 0))
                        exitt = True
                        pygame.display.flip()
                        time.sleep(2)
                        run = False
                    else:
                        exitask = False
            if exitask and not exitt:
                if exchoise:
                    screen.blit(imgexyes, (0, 0))
                else:
                    screen.blit(imgexno, (0, 0))
            else:
                if not exitt:
                    screen.blit(menuchoise[m%4], (0, 0))
            if abouter:
                screen.blit(imgab, (0, 0))
                screen.blit(version, (10, window - 20))
            if g and y and mgym:
                gym = True
            if hello and gym:
                swelcome.play()
                hello = False

            if newgamescreen:
                if choisenew:
                    screen.blit(imgstartyes, (0, 0))
                else:
                    screen.blit(imgstartno, (0, 0))
        
    else:
        if firstrun:
            score = 0
            begx = random.randint(0, window)
            begy = random.randint(0, window)
            scoretext = font.render(str(score), 1, WHITE)
            if seconder:
                secbegx = random.randint(0, window)
                secbegy = random.randint(0, window)
                scoretext2 = font.render(str(score2), 1, BLUE)
                scoretext = font.render(str(score), 1, RED)
                snake2 = [[secbegy, secbegx, LEFT]]
            while (begx == secbegx and begy == secbegy):
                secbegx = random.randint(0, window)
                secbegy = random.randint(0, window)
            snake = [[begy, begx, RIGHT]]
            applex = random.randint(0, window)
            appley = random.randint(0, window)
            while(applex == begx and appley == begy and applex == secbegx and appley == secbegy):
                applex = random.randint(0, window)
                appley = random.ramdint(0, window)
            firstrun = False
            played = True
            alive = True
            applebonus = False
            

    #key handling  
        if booster >= 3:
            animtwoxhelp += 1
            if animtwoxhelp % 3 == 0:
                animtwox += 1
        if applecounter == 5:
            applebonus = False
            applecounter = 0
            applex = random.randint(0, window)
            appley = random.randint(0, window)
                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                speedup = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                speedup = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL and seconder:
                speedup2 = True
            if event.type == pygame.KEYUP and event.key == pygame.K_LCTRL and seconder:
                speedup2 = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                firstrun = True
                headbump = False
                score = 0
                scoretext = font.render(str(score), 1, WHITE)
                if seconder:
                    scoretext = font.render(str(score), 1, RED)
                    score2 = 0
                    scoretext2 = font.render(str(score2), 1, BLUE)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause = True
                screen.blit(pausetext, (window/6, window/2))
                pygame.display.flip()
                while pause:
                    i = 228
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                            pause = False
            #control
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if dir != DOWN:
                    dir = UP
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if dir != UP:
                    dir = DOWN
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if dir != LEFT:
                    dir = RIGHT
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if dir != RIGHT:
                    dir = LEFT


            if event.type == pygame.KEYDOWN and event.key == pygame.K_s and seconder:
                if dir2 != DOWN:
                    dir2 = UP
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w and seconder:
                if dir2 != UP:
                    dir2 = DOWN
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d and seconder:
                if dir2 != LEFT:
                    dir2 = RIGHT
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a and seconder:
                if dir2 != RIGHT:
                    dir2 = LEFT
            
            snake[0][2] = dir
            if seconder:
                snake2[0][2] = dir2


        #TWO PLAYERS//////////////////////////////////////////////////////////////////////////////////////////////////
        if seconder and alive:
            #die handling
            if len(snake) > 1:
                for d in range(1, len(snake)):
                    if(abs(snake[0][0] - snake2[0][0]) < 7 and abs(snake[0][1] - snake2[0][1]) < 7 ):
                        headbump = True
                        alive = False
                        if score > score2:
                            looser = 2
                        elif score < score2:
                            looser = 1
                        else:
                            looser = random.randint(1, 2)
                    if(abs(snake[0][0] - snake[d][0]) < 1 and abs(snake[0][1] - snake[d][1]) < 1 and alive):
                        alive = False
                        looser = 1
                        auchlist[random.randint(0, 2)].play()
                        played = False
                        score = 0
                        score2 = 0
                    elif(abs(snake2[0][0] - snake[d][0]) < 7 and abs(snake2[0][1] - snake[d][1]) < 7 and alive):
                        alive = False
                        looser = 2
                        auchlist[random.randint(0, 2)].play()
                        played = False
                        score = 0
                        score2 = 0
            if len(snake2) > 1 and headbump == False:
                for d in range(1, len(snake2)):
                    if(abs(snake2[0][0] - snake2[d][0]) < 1 and abs(snake2[0][1] - snake2[d][1]) < 1 and alive):
                        alive = False
                        looser = 2
                        auchlist[random.randint(0, 2)].play()
                        played = False
                        score = 0
                        score2 = 0
                    
                    elif(abs(snake[0][0] - snake2[d][0]) < 7 and abs(snake[0][1] - snake2[d][1]) < 7 and alive):
                        alive = False
                        looser = 1
                        auchlist[random.randint(0, 2)].play()
                        played = False
                        score = 0
                        score2 = 0

             #appleeat handling
            if (abs(snake[0][0] - applex) <= 10 and abs(snake[0][1] - appley) <= 10):
                score+=1
                bitelist[n%50].play()
                scoretext = font.render(str(score), 1, RED)
                snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1], snake[len(snake)-1][2]])
                snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1], snake[len(snake)-1][2]])
                applex = random.randint(0, window)
                appley = random.randint(0, window)

            elif (abs(snake2[0][0] - applex) <= 10 and abs(snake2[0][1] - appley) <= 10):
                score2+=1
                bitelist[n%50].play()
                scoretext2 = font.render(str(score2), 1, BLUE)
                snake2.append([snake2[len(snake2)-1][0], snake2[len(snake2)-1][1], snake2[len(snake2)-1][2]])
                snake2.append([snake2[len(snake2)-1][0], snake2[len(snake2)-1][1], snake2[len(snake2)-1][2]])
                applex = random.randint(0, window)
                appley = random.randint(0, window)

            while((applex == snake[0][0] and appley == snake[0][1] and applex == snake2[0][0] and appley == snake2[0][1]) or (applex < 15 and appley < 15)):
                applex = random.randint(0, window)
                appley = random.randint(0, window)

            #second snake moving
            if speedup2:
                for j in range(len(snake2)-1, 0, -1):
                        snake2[j][1] = snake2[j-1][1]
                        snake2[j][0] = snake2[j-1][0]
                if dir2 == DOWN:
                    if(snake2[0][1] - step <= 0):
                        snake2[0][1] = window
                    else:
                        snake2[0][1] = snake2[0][1] - step

                if dir2 == UP:
                    if(snake2[0][1] + step >= window):
                        snake2[0][1] = 0
                    else:
                        snake2[0][1] = snake2[0][1] + step   

                if dir2 == RIGHT:
                    if(snake2[0][0] + step >= window):
                        snake2[0][0] = 0
                    else:
                        snake2[0][0] = snake2[0][0] + step  

                if dir2 == LEFT:
                    if(snake2[0][0] - step <= 0):
                        snake2[0][0] = window
                    else:
                        snake2[0][0] = snake2[0][0] - step 

            for j in range(len(snake2)-1, 0, -1):
                snake2[j][1] = snake2[j-1][1]
                snake2[j][0] = snake2[j-1][0]
            if dir2 == DOWN:
                if(snake2[0][1] - step <= 0):
                    snake2[0][1] = window
                else:
                    snake2[0][1] = snake2[0][1] - step

            if dir2 == UP:
                if(snake2[0][1] + step >= window):
                    snake2[0][1] = 0
                else:
                    snake2[0][1] = snake2[0][1] + step   

            if dir2 == RIGHT:
                if(snake2[0][0] + step >= window):
                    snake2[0][0] = 0
                else:
                    snake2[0][0] = snake2[0][0] + step  

            if dir2 == LEFT:
                if(snake2[0][0] - step <= 0):
                    snake2[0][0] = window
                else:
                    snake2[0][0] = snake2[0][0] - step 


        
        #ONE PLAYER//////////////////////////////////////////////////////////////////////////////////////////////////
        else:
            if not DEV_MODE:
                if not applebonus:
                    #die handling1
                    if len(snake) > 5:
                        for d in range(5, len(snake)):
                            if(abs(snake[0][0] - snake[d][0]) < 1 and abs(snake[0][1] - snake[d][1]) < 1):
                                alive = False
                                booster = 0
                                if gym:
                                    if played:
                                        orgasmlist[random.randint(0, 2)].play()
                                        played = False
                                else:
                                    if played:
                                        auchlist[random.randint(0, 2)].play()
                                        played = False
                                if score > bestscore:
                                    bestscore = score
                                    bestscoretext = fontsmall.render(str(bestscore), 1, WHITE)
                                    score = 0


    #appleeat handling
            if (abs(snake[0][0] - applex) <= appleRealSize and abs(snake[0][1] - appley) <= appleRealSize):
                if booster > 0:
                    if (pygame.time.get_ticks() - starttics <= bonusTime):#1900  
                        booster+=1
                        starttics = pygame.time.get_ticks()
                        animtwox = 0
                        animtwoxhelp = 0
                    else:
                        booster = 0
                else:
                    starttics = pygame.time.get_ticks()
                    booster+=1
                if booster >= 3:
                    blind = True
                    b = 0
                    score+=1
                    if gym:
                        gymsoumdslist[n%12].play()
                    elif booster <= 4:
                        chordlist[0].play()
                    elif booster <= 6:
                        chordlist[1].play()
                    elif booster <= 8:
                        chordlist[2].play()
                    elif booster == 9:
                        chordlist[3].play()
                score+=1
                bitelist[n%50].play()
                scoretext = font.render(str(score), 1, WHITE)
                snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1], snake[len(snake)-1][2]])
                snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1], snake[len(snake)-1][2]])
                if booster >= 3:
                    if booster <= 4:
                        snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1], snake[len(snake)-1][2]])
                        snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1], snake[len(snake)-1][2]])
                    elif booster <= 6:
                        for app in range(4):
                            snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1], snake[len(snake)-1][2]])
                    elif booster <= 8:
                        for app in range(6):
                            snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1], snake[len(snake)-1][2]])
                    elif booster == 9:
                        for app in range(5):
                            applelist.append([random.randint(5, window-5), random.randint(5, window-5), True])
                        if gym:
                            appleOrgasmList[random.randint(0, 1)].play()
                        applebonus = True
                        booster = 0
                if applebonus:
                    applex = 600
                    appley = 600
                else:
                    applex = random.randint(5, window-5)
                    appley = random.randint(5, window-5)
                while((applex == snake[0][0] and appley == snake[0][1]) or (applex < 15 and appley < 15)):
                    applex = random.randint(5, window-5)
                    appley = random.randint(5, window-5)
            if applebonus:
                for app in range(5):
                    if (abs(snake[0][0] - applelist[app][0]) <= 10 and abs(snake[0][1] - applelist[app][1]) <= 10 and applelist[app][2]):
                        applelist[app][2] = False
                        score += 1
                        applecounter+=1
                        scoretext = font.render(str(score), 1, WHITE)
                        bitelist[n%50].play()
                        snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1], snake[len(snake)-1][2]])
                        snake.append([snake[len(snake)-1][0], snake[len(snake)-1][1], snake[len(snake)-1][2]])


    #moving handle 

        if speedup:
            for j in range(len(snake)-1, 0, -1):
                    snake[j][1] = snake[j-1][1]
                    snake[j][0] = snake[j-1][0]
            if dir == DOWN:
                if(snake[0][1] - step <= 0):
                    snake[0][1] = window
                else:
                    snake[0][1] = snake[0][1] - step

            if dir == UP:
                if(snake[0][1] + step >= window):
                    snake[0][1] = 0
                else:
                    snake[0][1] = snake[0][1] + step   

            if dir == RIGHT:
                if(snake[0][0] + step >= window):
                    snake[0][0] = 0
                else:
                    snake[0][0] = snake[0][0] + step  

            if dir == LEFT:
                if(snake[0][0] - step <= 0):
                    snake[0][0] = window
                else:
                    snake[0][0] = snake[0][0] - step 

        for j in range(len(snake)-1, 0, -1):
                snake[j][1] = snake[j-1][1]
                snake[j][0] = snake[j-1][0]
        if dir == DOWN:
            if(snake[0][1] - step <= 0):
                snake[0][1] = window
            else:
                snake[0][1] = snake[0][1] - step

        if dir == UP:
            if(snake[0][1] + step >= window):
                snake[0][1] = 0
            else:
                snake[0][1] = snake[0][1] + step   

        if dir == RIGHT:
            if(snake[0][0] + step >= window):
                snake[0][0] = 0
            else:
                snake[0][0] = snake[0][0] + step  

        if dir == LEFT:
            if(snake[0][0] - step <= 0):
                snake[0][0] = window
            else:
                snake[0][0] = snake[0][0] - step 

 
        

    #drawing
        if menu == False:
            if alive:
                screen.blit(imgfone, (0, 0))
                if booster >= 3 and animtwox < 38:
                    screen.blit(sparklesanim[animtwox], (195-animtwox*4, -120))
                    if booster <= 4:
                        screen.blit(twoxlist[animtwox], (0, 0))
                    elif booster <= 6:
                        screen.blit(threelist[animtwox], (0, 0))
                screen.blit(imgapple, (applex-koef+3, appley-koef))
                if applebonus:
                    for app in range(5):
                        if applelist[app][2]:
                            screen.blit(imgapple, (applelist[app][0]-koef+3, applelist[app][1]-koef))
                #pygame.draw.circle(screen, (255, 0, 0), (applex, appley), 5)#draw apple
                for i in range(1, len(snake)):
                    #pygame.draw.rect(screen, (255, 255, 255), (snake[i][0]-5, snake[i][1]-5, sizeofsnake, sizeofsnake))#draw snake
                    if i % 2 == 0:
                        screen.blit(imgbody, (snake[i][0]-5, snake[i][1]-5))

                if seconder==False:
                    screen.blit(scoretext, (10, 10))#draw text  
                    if bestscore > 0:
                        screen.blit(bestscoretext1, (window - 70, 10))
                        screen.blit(bestscoretext, (window-40, 10))
                else:
                    screen.blit(scoretext, (window-40, 10))
                    screen.blit(scoretext2, (10, 10))
                    if dir2 == DOWN:
                        screen.blit(imghead_d2, (snake2[0][0]-koef+4, snake2[0][1]-koef))
                    if dir2 == UP:
                        screen.blit(imghead_u2, (snake2[0][0]-koef+2, snake2[0][1]-koef+6))
                    if dir2 == RIGHT:
                        screen.blit(imghead_l2, (snake2[0][0]-koef+5, snake2[0][1]-koef+4))
                    if dir2 == LEFT:
                        screen.blit(imghead_r2, (snake2[0][0]-koef, snake2[0][1]-koef+2))
                     
                    for i in range(1, len(snake2)):
                        if i % 2 == 0:
                            screen.blit(imgbody2, (snake2[i][0]-5, snake2[i][1]-5))

                      
                if dir == DOWN:
                    screen.blit(imghead_d, (snake[0][0]-koef+4, snake[0][1]-koef))
                if dir == UP:
                    screen.blit(imghead_u, (snake[0][0]-koef+2, snake[0][1]-koef+6))
                if dir == RIGHT:
                    screen.blit(imghead_l, (snake[0][0]-koef+5, snake[0][1]-koef+4))
                if dir == LEFT:
                    screen.blit(imghead_r, (snake[0][0]-koef, snake[0][1]-koef+2))
                if blind:
                    screen.blit(blindlist[b], (0, 0))
                    
                    b+=1
                    if b == 9:
                        b = 0
                        blind = False

                #drawing second snake:

                

            else:
                if seconder:
                    screen.blit(imgfone, (0, 0))
                    if looser == 1:
                        deathtext = font.render('Blue wins!', 1, BLUE)
                    if looser == 2:
                        deathtext = font.render('RED wins!', 1, RED)
                    screen.blit(deathtext, (window/6, window/2))

                else:
                    screen.blit(imgfone, (0, 0))
                    deathtext = font.render('Your snake is dead', 1, WHITE)
                    scoretext = font.render(str(score), 1, WHITE)
                    screen.blit(deathtext, (window/6, window/2))
                    screen.blit(scoretext, (10, 10))
                if bestscore > 0:
                    screen.blit(bestscoretext1, (window - 70, 10))
                    screen.blit(bestscoretext, (window-40, 10))
    time_passed = clock.tick(fps)
    pygame.display.flip()


pygame.quit()