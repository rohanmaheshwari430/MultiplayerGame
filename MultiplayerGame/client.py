import pygame
from network import Network
import pickle

pygame.font.init()

width = 700
height = 700

win = pygame.display.set_mode((width,height))



pygame.display.set_caption("Client")

class button: 
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x,self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2))) #centering the text in the button

    def click(self, pos): #checking if the coordinate of our mouse is in the region of the button  
        x1 = pos[0]
        y1 = pos[1]
        
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - round(text.get_width()/2), height/2 - round(text.get_height()/2)))

    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0,255,255))
        win.blit(text, (80,200))

        text = font.render("Opponents", 1, (0,255,255))
        win.blit(text, (380,200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0,0,0))
        else:
            if game.p1Went and p == 0: #player 1 went and the current client is player 1
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went: #player 1 went but the current client is not player 1
                text1 = font.render("Locked in", 1, (0,0,0))
            else:
                text1 = font.render("Waiting...", 1, (0,0,0))

            if game.p2Went and p == 1: #player 1 went and the current client is player 1
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went: #player 1 went but the current client is not player 1
                text2 = font.render("Locked in", 1, (0,0,0))
            else:
                text2 = font.render("Waiting...", 1, (0,0,0))

        if p == 1:
            win.blit(text2, (100,350))
            win.blit(text1, (400,350))
        else:
            win.blit(text1, (100,350))
            win.blit(text2, (400,350))

        for button in buttons:
            button.draw(win)
            
    pygame.display.update()
                
  

buttons = [button("Rock", 50,500, (0,0,0)), button("Scissors", 250, 500, (255,0,0)), button("Paper", 450, 500, (0,255,0))]


def main(): #initially will be getting the game running. but once we exist this main function, we will get into a game menu
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP()) #this is the initial step where the client receives either a 0 or 1 for player number 
    print("You are player: ", player)
    

    while run:
        clock.tick(60)

        try: 
            game = n.send("get")

        except:
            run = False
            print("Could not get game")
            break


        if game.bothWent(): #resetting the window to start a new round, telling the server to reset the status of players move
            redrawWindow(win, game, player)
            pygame.time.delay(500)

            try:
                game = n.send("reset")
            except:
                run = False
                print("Could not get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0): #determining round winner and showing win/tie/loss status on client window
                text = font.render("You won!", 1, (0,255,0))

            elif game.winner() == -1:
                text = font.render("Tie game!", 1, (0,0,255))

            else:
                text = font.render("You lost!", 1, (255,0,0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN: #checking if they clicked the button
                pos = pygame.mouse.get_pos() #storing mouse pointer location in position varible 
                for button in buttons:
                    if button.click(pos) and game.connected(): #checking if pos is in button region and also checking if both clients are connected to avoid one client making moves before the other
                        if player == 0: #ensuring that players cannot change their move after the other player has moved
                            if not game.p1Went:
                                n.send(button.text)

                        else:
                            if not game.p2Went:
                                n.send(button.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()
    
    
    while run:
        clock.tick(60)
        win.fill((128,128,128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to play!", 1, (0,0,255))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()

while True:
    menu_screen()
