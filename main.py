import pygame as pg
pg.font.init()
import os
from random import randint as rd
import time

D_WIDTH, D_HEIGHT = 1200, 800
WIN = pg.display.set_mode((D_WIDTH, D_HEIGHT)) 
pg.display.set_caption("Ping Pong")
BACKGROUND = pg.Rect(0,0,D_WIDTH, D_HEIGHT)
FPS=60

WHITE = (255,255,255)
GREY = (50,50,50)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

POINTS_FONT=pg.font.SysFont('Arial', 100)
MESSAGE_FONT=pg.font.SysFont('Arial', 120)
COUNTDOWN_FONT=pg.font.SysFont('Arial', 80)
BALL_IMG=pg.image.load(os.path.join('resources','ball.png'))
BALL_IMG=pg.transform.scale(BALL_IMG,(25,25))

MAX_POINTS=5
VEL=5
BALL_VEL=5
ball_prev_pos=[D_WIDTH/2-12.5,D_HEIGHT/2-12.5]
ball_dir=rd(5,11)/10


def draw_window(pl_A, pl_B, ball, points, message, countdown):
	#WIN.fill(WHITE)

	pg.draw.rect(WIN, BLACK, BACKGROUND)
	
	A_points_text=POINTS_FONT.render(str(points[0]), 1, GREY)
	B_points_text=POINTS_FONT.render(str(points[1]), 1, GREY)
	WIN.blit(A_points_text, (D_WIDTH//4-A_points_text.get_width()//2,D_HEIGHT//2-A_points_text.get_height()//2))
	WIN.blit(B_points_text, (3*D_WIDTH//4-B_points_text.get_width()//2,D_HEIGHT//2-B_points_text.get_height()//2))

	pg.draw.rect(WIN, RED, pl_A)
	pg.draw.rect(WIN, BLUE, pl_B)

	WIN.blit(BALL_IMG, (ball.x, ball.y))

	message_text=MESSAGE_FONT.render(message,1,WHITE)
	WIN.blit(message_text,(D_WIDTH//2-message_text.get_width()//2,D_HEIGHT//2-message_text.get_height()//2))
	countdown_text=COUNTDOWN_FONT.render(countdown,1,GREY)
	WIN.blit(countdown_text,(D_WIDTH//2-countdown_text.get_width()//2,D_HEIGHT//2-countdown_text.get_height()//2+message_text.get_height()))

	pg.display.update() 

def play_init(ball):
	ball_dir=rd(5,11)/10
	ball.x, ball.y = D_WIDTH//2-12.5, D_HEIGHT//2-12.5
	ball_prev_pos[0]=ball.x+rd(1,3)-1.5
	ball_prev_pos[1]=ball.y+rd(1,3)-1.5

def handle_movement_A(keys_pressed, pl_A):
	if keys_pressed[pg.K_w] and pl_A.y>0:
		pl_A.y-=VEL
	if keys_pressed[pg.K_s] and pl_A.y+VEL+pl_A.height<D_HEIGHT:
		pl_A.y+=VEL

def handle_movement_B(keys_pressed, pl_B):
	if keys_pressed[pg.K_UP] and pl_B.y>0:
		pl_B.y-=VEL
	if keys_pressed[pg.K_DOWN] and pl_B.y+VEL+pl_B.height<D_HEIGHT:
		pl_B.y+=VEL

def handle_movement_ball(ball, pl_A, pl_B):
	D=[ball.x-ball_prev_pos[0],ball.y-ball_prev_pos[1]]

	if ball.y>0 and ball.y<D_HEIGHT-ball.height:
		if D[1]>0:
			ball_prev_pos[1]=ball.y
			ball.y+=BALL_VEL
		else:
			ball_prev_pos[1]=ball.y
			ball.y-=BALL_VEL
	else:
		a=ball_prev_pos[1]
		ball_prev_pos[1]=ball.y
		ball.y=a

	if D[0]>0:
		ball_prev_pos[0]=ball.x
		ball.x+=BALL_VEL*ball_dir
	else:
		ball_prev_pos[0]=ball.x
		ball.x-=BALL_VEL*ball_dir

	if (ball.colliderect(pl_A) and ball.x>pl_A.x) or (ball.colliderect(pl_B) and ball.x<pl_B.x):
		a=ball_prev_pos[0]
		ball_prev_pos[0]=ball.x
		ball.x=a

def handle_score(pl_A, pl_B, ball, points):
	if ball.x<0 or ball.x>D_WIDTH-ball.width:
		mess="XD"
		if ball.x<0:
			#B scorred
			points[1]+=1
			mess="BLUE SCORED!"
		if ball.x>D_WIDTH-ball.width:
			#A scored
			points[0]+=1
			mess="RED SCORED!"
		countdown_text="Next round in "
		if points[0]<MAX_POINTS and points[1]<MAX_POINTS:
			for i in range(3,0,-1):
				draw_window(pl_A, pl_B, ball, points, mess, countdown_text+str(i))
				time.sleep(1)
		play_init(ball)
		

def main():

	game_clk=pg.time.Clock()

	pl_A = pg.Rect(50,D_HEIGHT//2-D_HEIGHT//20/2 ,5,D_HEIGHT//10)
	pl_B = pg.Rect(D_WIDTH-50-25,D_HEIGHT//2-D_HEIGHT//20/2 ,5,D_HEIGHT//10) 

	ball = pg.Rect(0,0,25,25)
	play_init(ball)

	points=[0,0]

	print(ball_prev_pos[0]-ball.x)

	game_run = True
	while game_run: 
		game_clk.tick(FPS)
		for event in pg.event.get():
			#WINDOW_EXIT
			if event.type == pg.QUIT:
				game_run = False
				pg.quit()
		
		#movement_handeling:
		keys_pressed=pg.key.get_pressed()
		handle_movement_A(keys_pressed, pl_A)
		handle_movement_B(keys_pressed, pl_B)

		handle_movement_ball(ball, pl_A, pl_B)

		handle_score(pl_A, pl_B, ball, points)

		if points[0]>=MAX_POINTS or points[1]>=MAX_POINTS:
			mess=""
			if points[0] >=MAX_POINTS:
				mess="RED Wins!"
			if points[1] >=MAX_POINTS:
				mess="BLUE WINS!"
			draw_window(pl_A, pl_B, ball, points, mess, "New game in 5")
			time.sleep(1)
			draw_window(pl_A, pl_B, ball, points, mess, "New game in 4")
			time.sleep(1)
			draw_window(pl_A, pl_B, ball, points, mess, "New game in 3")
			time.sleep(1)
			draw_window(pl_A, pl_B, ball, points, mess, "New game in 2")
			time.sleep(1)
			draw_window(pl_A, pl_B, ball, points, mess, "New game in 1")
			time.sleep(1)
			break
			

		#UPDATING_WINDOW
		draw_window(pl_A, pl_B, ball, points, "","")

	main()

if __name__ == "__main__":	#only run the game if we run this file directly 
	main()					# __name__ - name of the file