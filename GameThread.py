import threading
import GameObjects as go
import random
class GameThread(threading.Thread):
    SPEED = 500000
    def __init__(self, canvas, window):
        threading.Thread.__init__(self)
        self.list_rectangles = []
        self.player_bat = go.Bat(100,580)
        self.canvas = canvas
        self.score = go.GameText(10,10)
        self.window = window

    def slowDown(self):
        #TODO: Improve this method by your own :)
        i = 0
        while(i<self.SPEED):
            i+=1

    def run(self):
        i = 0
        #Game-Calulation:
        while self.score.lost==False:
            #print(str(i))
            if(i%50==0):
                i = 0
                #Set Rectangles:
                self.set_rectangles()

            #Move Objects
            self.move()
            #Check for Collisions
            self.check_collisions()
            #Draw
            self.draw()
            i+=1
            self.slowDown()
        i = 0
        while i < 100000000:
            i+=1
        self.window.destroy()
        self._delete()

        #Game Over
        #TODO: Save Score, if highscore

    def set_rectangles(self):
        rndx = random.randrange(475)
        rndSpeed = random.randrange(2)+1
        y = 0
        rndColor = random.randrange(2)
        self.list_rectangles.append(go.Rectangle(rndx,y,rndSpeed,rndColor))

    def move(self):
        #Move Rectangles
        for rec in self.list_rectangles:
            rec.moveY()

    def check_collisions(self):
        removeIndixes = []
        i = 0
        while i < len(self.list_rectangles):
            detected = self.list_rectangles[i].collidedWith(self.player_bat)
            if(detected==1):
                self.list_rectangles.__delitem__(i)
                self.score.points+=1
            elif(detected==2):
                self.score.lost = True
                self.window.title("Game Over..")
                break
            else:
                i+=1


        for r in removeIndixes:
            print(r)
            self.list_rectangles.remove(r)

    def draw(self):
        self.canvas.delete('all')
        #self.canvas.update_idletasks()
        # Draw Rectangles
        for rec in self.list_rectangles:
            rec.draw(self.canvas)
        # Draw Bat
        self.player_bat.draw(self.canvas)
        # Draw Score
        self.score.draw(self.canvas)
