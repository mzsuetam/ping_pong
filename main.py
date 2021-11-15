import pygame as pg
pg.font.init()
import os
from random import randint as rd

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
BALL_IMG=pg.image.load(os.path.join('resources','ball.png'))
BALL_IMG=pg.transform.scale(BALL_IMG,(25,25))

MAX_POINTS=5
VEL=5
BALL_VEL=5
ball_prev_pos=[D_WIDTH/2-12.5,D_HEIGHT/2-12.5]


def draw_window(pl_A, pl_B, ball, A_points, B_points):
	#WIN.fill(WHITE)

	pg.draw.rect(WIN, BLACK, BACKGROUND)
	
	A_points_text=POINTS_FONT.render(str(A_points), 1, GREY)
	B_points_text=POINTS_FONT.render(str(B_points), 1, GREY)
	WIN.blit(A_points_text, (D_WIDTH//4-A_points_text.get_width()//2,D_HEIGHT//2-A_points_text.get_height()//2))
	WIN.blit(B_points_text, (3*D_WIDTH//4-B_points_text.get_width()//2,D_HEIGHT//2-B_points_text.get_height()//2))

	pg.draw.rect(WIN, RED, pl_A)
	pg.draw.rect(WIN, BLUE, pl_B)

	WIN.blit(BALL_IMG, (ball.x, ball.y))

	pg.display.update() 

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

def main():

	game_clk=pg.time.Clock()

	pl_A = pg.Rect(50,D_HEIGHT//2-D_HEIGHT//20/2 ,25,D_HEIGHT//20)
	pl_B = pg.Rect(D_WIDTH-50-25,D_HEIGHT//2-D_HEIGHT//20/2 ,25,D_HEIGHT//20) 

	ball = pg.Rect(D_WIDTH//2-12.5, D_HEIGHT//2-12.5,25,25)
	if rd(0,1):
		ball_prev_pos[0]=-rd(1,10)/10
	else:
		ball_prev_pos[0]=rd(1,10)/10
	ball_prev_pos[1]=ball.y+rd(1,3)-1.5

	A_points, B_points = 0,0

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

		#win_handling
		winner_text=""
		if A_points >=MAX_POINTS:
			winner_text="pl_A 1 Wins!"
		if B_points >=MAX_POINTS:
			winner_text="pl_A 2 Wins!"
		# if winner_text!="":
		# 	draw_window(A_points, B_points)
		# 	break


		#UPDATING_WINDOW
		draw_window(pl_A, pl_B, ball, A_points, B_points)

	main()

if __name__ == "__main__":	#only run the game if we run this file directly 
	main()					# __name__ - name of the file