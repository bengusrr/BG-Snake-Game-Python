import pygame
import sys
import random

pygame.init()

# Fuente
# fuente = pygame.font.SysFont("Menlo",30)

# Constantes
ANCHO = 800
ALTO = 600
color_negro = (0,0,0)
colo_amarillo = (255,255,0)
color_verde = (0,143,57)
color_rojo = (255,0,0)

eje_movimiento = 'x'
fps = 2


# Jugador
jugador_size = 20
jugador = [
	{'salto':2, 'mov_X':25, 'mov_Y':0, 'direc':'R'},
	{'salto':1, 'mov_X':25, 'mov_Y':0, 'direc':'R'},
	{'salto':0, 'mov_X':25, 'mov_Y':0, 'direc':'R'}
]

salto = [
	{'salto':0, 'x':50, 'y':40, 'direc':'R', 'mov_X':25, 'mov_Y':0},
	{'salto':1, 'x':75, 'y':40, 'direc':'R', 'mov_X':25, 'mov_Y':0},
	{'salto':2, 'x':100, 'y':40, 'direc':'R', 'mov_X':25, 'mov_Y':0}
]

num_salto = 2

# Frutas
fruta_size = 20
fruta_pos = [random.randint(0, ANCHO - fruta_size),random.randint(0, ALTO - fruta_size)]
marcador = 0


# crear nueva ventana
ventana = pygame.display.set_mode((800,600))
pygame.display.set_caption('Marcador: 0' + ' | speed: ' + str(fps))


game_over = False
stop = False
clock = pygame.time.Clock()


# Funciones
def registra_mov(num_salto):
	num_salto += 1
	salto.append({'salto':num_salto,
				'x':salto[num_salto-1]['x'] + jugador[0]['mov_X'],
				'y':salto[num_salto-1]['y'] + jugador[0]['mov_Y'],
				'direc':jugador[0]['direc'],
				'mov_X':jugador[0]['mov_X'],
				'mov_Y':jugador[0]['mov_Y']})

	if salto[num_salto]['x']<0 or salto[num_salto]['x']>ANCHO: return 0
	if salto[num_salto]['y']<0 or salto[num_salto]['y']>ALTO: return 0

	#print(salto[num_salto])
	return num_salto

def mover_jugador(num_salto):
	for i in range(0, len(jugador)):
		jugador[i]['salto'] = num_salto
		jugador[i]['mov_X'] = salto[num_salto]['mov_X']
		jugador[i]['mov_Y'] = salto[num_salto]['mov_Y']
		jugador[i]['direc'] = salto[num_salto]['direc']
		num_salto -=1

def detectar_colision_fruta(num_salto, fruta_pos):
	jx = salto[jugador[0]['salto']]['x']
	jy = salto[jugador[0]['salto']]['y']
	ex = fruta_pos[0]
	ey = fruta_pos[1]

	if (ex >= jx and ex < (jx + jugador_size)) or (jx >= ex and jx < (ex + fruta_size)):
		if (ey >= jy and ey < (jy + jugador_size)) or (jy >= ey and jy < (ey + fruta_size)):
			return True
	return False

def detectar_colision_jugador():
	jx = salto[jugador[0]['salto']]['x']
	jy = salto[jugador[0]['salto']]['y']

	for i in range(1, len(jugador)-1):
		ex = salto[jugador[i]['salto']]['x']
		ey = salto[jugador[i]['salto']]['y']

		if (ex >= jx and ex < (jx + jugador_size)) or (jx >= ex and jx < (ex + jugador_size)):
			if (ey >= jy and ey < (jy + jugador_size)) or (jy >= ey and jy < (ey + jugador_size)):
				return True
	return False


while not game_over:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			game_over = True

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_LEFT and eje_movimiento == 'y':
				#print('LEFT')
				eje_movimiento = 'x'
				jugador[0]['direc'] = 'L'
				jugador[0]['mov_X'] = -25
				jugador[0]['mov_Y'] = 0

			if event.key == pygame.K_RIGHT and eje_movimiento == 'y':
				#print('RIGHT')
				eje_movimiento = 'x'
				jugador[0]['direc'] = 'R'
				jugador[0]['mov_X'] = 25
				jugador[0]['mov_Y'] = 0

			if event.key == pygame.K_UP and eje_movimiento == 'x':
				#print('UP')
				eje_movimiento = 'y'
				jugador[0]['direc'] = 'U'
				jugador[0]['mov_X'] = 0
				jugador[0]['mov_Y'] = -25

			if event.key == pygame.K_DOWN and eje_movimiento == 'x':
				#print('DOWN')
				eje_movimiento = 'y'
				jugador[0]['direc'] = 'D'
				jugador[0]['mov_X'] = 0
				jugador[0]['mov_Y'] = 25

			if event.key == pygame.K_SPACE:
				ind=len(jugador)- 1
				jugador.append({'salto':jugador[ind]['salto']-1,
							    'mov_X':jugador[ind]['mov_X'],
							    'mov_Y':jugador[ind]['mov_Y'],
							    'direc':jugador[ind]['direc']})


	num_salto = registra_mov(num_salto)
	if num_salto > 0:
		mover_jugador(num_salto)
	else:
		stop = True


	ventana.fill(color_negro)

	# Comprueba si se ha comido una fruta
	if detectar_colision_fruta(num_salto, fruta_pos):
		fruta_pos = [random.randint(0, ANCHO - fruta_size),random.randint(0, ALTO - fruta_size)]

		ind=len(jugador)-1
		jugador.append({'salto':jugador[ind]['salto']-1,
						'mov_X':jugador[ind]['mov_X'],
						'mov_Y':jugador[ind]['mov_Y'],
						'direc':jugador[ind]['direc']})

		marcador += 1
		if marcador % 2 == 0: fps = fps * 1.1
		pygame.display.set_caption('Marcador: ' + str(marcador) + ' | speed: ' + str(fps))


	if detectar_colision_jugador(): stop = True


	# Dibujar fruta
	pygame.draw.rect(ventana, colo_amarillo,
		(fruta_pos[0], fruta_pos[1], fruta_size, fruta_size))


	# Dibujar jugador
	for player in jugador:

		x = salto[player['salto']]['x']
		y = salto[player['salto']]['y']

		pygame.draw.rect(ventana, color_verde,
			(x, y, jugador_size, jugador_size))


	dt = clock.tick(fps)
	#print('tiempo transcurrido: {} milisegundos'.format(dt))
	if not stop: pygame.display.update()