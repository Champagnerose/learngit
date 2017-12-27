import pygame
import sys
import random  

sys.setrecursionlimit(100000) #增加递归次数

class Snake(object):
        def __init__(self):
                self.body = []
                self.direction = pygame.K_RIGHT
                for i in range(5):
                        initX = [200+25*i,200,25,25]
                        self.body.insert(0,initX)

        def addnode(self):
                newone=self.body[0].copy()
                if self.direction  == pygame.K_RIGHT:
                        newone[0] +=25       
                elif self.direction  == pygame.K_LEFT:
                        newone[0] -=25
                elif self.direction  == pygame.K_UP:
                        newone[1] -=25
                elif self.direction  == pygame.K_DOWN:
                        newone[1] +=25
                self.body.insert(0,newone)

        def delnode(self):
                self.body.pop()

        def move(self):
                self.addnode()
                self.delnode()

        def change_direction(self,keymove):
                LR = [pygame.K_LEFT,pygame.K_RIGHT]
                UD = [pygame.K_UP,pygame.K_DOWN]
                if self.direction in LR and keymove in UD:        
                        self.direction = keymove
                if self.direction in UD and keymove in LR:
                        self.direction = keymove

        def crash(self):
                #检查是否撞墙
                if self.direction == pygame.K_RIGHT and ((self.body[0][0] + 25) >600):
                        return False
                if self.direction == pygame.K_LEFT and (self.body[0][0] <0):
                        return False
                if self.direction == pygame.K_UP and (self.body[0][1] <0):
                        return False
                if self.direction == pygame.K_DOWN and ((self.body[0][1] + 25) >600):
                        return False
                #检查是否撞自己,有一个点的延迟
                for each in self.body[1:]:
                        if each == self.body[0]:
                                return False
                else:
                        return True

class Food(object):
        def __init__(self):
                self.newfood = [[random.randint(0,23)*25,random.randint(0,23)*25,25,25]]

        def create_newfood(self):
                newfood = [random.randint(1,22)*25,random.randint(1,22)*25,25,25]
                self.newfood[0] = newfood
        
def show_text(screen,pos,text,color,font_bold = False, font_size = 60, font_italic = False):
        cur_font = pygame.font.SysFont('宋体', font_size)
        cur_font.set_bold(font_bold)
        cur_font.set_italic(font_italic)
        text_fmt = cur_font.render(text, 1, color)
        screen.blit(text_fmt, pos)

def main():       
        pygame.init()
        screen_size = (600,600)
        screen = pygame.display.set_mode(screen_size) #设定屏幕尺寸
        pygame.display.set_caption('贪吃蛇')#设定标题

        snake = Snake()
        food = Food()
        life = True
        
        while True:
                screen.fill((255,255,255))
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                sys.exit()
                        if event.type == pygame.KEYDOWN:
                                snake.change_direction(event.key)
                                if (not life) and (event.key == pygame.K_SPACE):
                                        return main()
                if life:
                        snake.move()
                        life = snake.crash()
                        if snake.body[0] == food.newfood[0]:
                                snake.addnode()
                                food.create_newfood()
                                while food.newfood[0] in snake.body:
                                        food.create_newfood()
                                
                for rect in snake.body:
                        pygame.draw.rect(screen,(0,255,0),rect,0)
                for rect in food.newfood:                
                        pygame.draw.rect(screen,(0,0,255),rect,0)

                if not life:
                        show_text(screen,(100,200),'GAME OVER!', (227,29,18),False,100)
                        show_text(screen,(150,260),'use space-key to restart the game...', (0,0,22),False,30)

                score = len(snake.body) - 5
                show_text(screen, (0, 550), 'Scores:' + str(score),(200,200,200))
                
                pygame.display.update()
                pygame.time.Clock().tick(5)

if __name__ == '__main__':
        main()
