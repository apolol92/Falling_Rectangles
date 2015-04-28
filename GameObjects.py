import tkinter as tk

class Bat:
    WIDTH = 60
    HEIGHT=10

    def __init__(self, posX, posY):
        self.x = posX
        self.y = posY

    def moveX(self,speedX):
        self.x+=speedX

    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.x+self.WIDTH, self.y+self.HEIGHT)

class Rectangle:
    WIDTH = 25
    HEIGHT = 25
    def __init__(self, posX, posY, speedY, c):
        self.x = posX
        self.y = posY
        self.speedY = speedY
        self.color = c

    def moveY(self):
        self.y += self.speedY
        print("Rectangle moved..")

    def draw(self, canvas):
        if(self.color==0):
            canvas.create_rectangle(self.x, self.y, self.x+self.WIDTH, self.y+self.HEIGHT, fill="red")
        else:
            canvas.create_rectangle(self.x, self.y, self.x+self.WIDTH, self.y+self.HEIGHT, fill="green")

    def collidedWith(self, bat):
        if(self.x < bat.x + bat.WIDTH and self.x + self.WIDTH > bat.x and self.y < bat.y + bat.HEIGHT and self.y + self.HEIGHT > bat.y):
            if(self.color == 0):
                return 2
            else:
                #Green
                return 1
        return 0


class GameText:

    def __init__(self, posX, posY):
        self.x = posX
        self.y = posY
        self.points = 0
        self.lost = False

    def draw(self, canvas):
        canvas.create_text(self.x,self.y,text=str(self.points))