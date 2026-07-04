from tkinter import *
import random

WIDTH = 900
HEIGHT = 500

PAD_W = 10
PAD_H = 100

BALL_RADIUS = 15

INITIAL_SPEED = 6
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED

PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# =====================
# Membuat Window
# =====================
root = Tk()
root.title("Pong Game AI")

canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="darkgreen")
canvas.pack()

# Garis Lapangan
canvas.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="white", dash=(5,5))
canvas.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
canvas.create_line(WIDTH-PAD_W, 0, WIDTH-PAD_W, HEIGHT, fill="white")

# =====================
# Paddle
# =====================
player = canvas.create_rectangle(
    PAD_W,
    HEIGHT/2-PAD_H/2,
    PAD_W+PAD_W,
    HEIGHT/2+PAD_H/2,
    fill="white"
)

ai = canvas.create_rectangle(
    WIDTH-PAD_W*2,
    HEIGHT/2-PAD_H/2,
    WIDTH-PAD_W,
    HEIGHT/2+PAD_H/2,
    fill="white"
)

# =====================
# Bola
# =====================
ball = canvas.create_oval(
    WIDTH/2-BALL_RADIUS,
    HEIGHT/2-BALL_RADIUS,
    WIDTH/2+BALL_RADIUS,
    HEIGHT/2+BALL_RADIUS,
    fill="white"
)

# =====================
# Score
# =====================
score1 = canvas.create_text(
    WIDTH/2-50,
    30,
    text="0",
    fill="white",
    font=("Arial",24)
)

score2 = canvas.create_text(
    WIDTH/2+50,
    30,
    text="0",
    fill="white",
    font=("Arial",24)
)

# =====================
# Kontrol Keyboard
# =====================
move_up = False
move_down = False


def key_press(event):
    global move_up, move_down

    if event.keysym == "w":
        move_up = True
    elif event.keysym == "s":
        move_down = True


def key_release(event):
    global move_up, move_down

    if event.keysym == "w":
        move_up = False
    elif event.keysym == "s":
        move_down = False


root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

# =====================
# Reset Bola
# =====================
def reset_ball():
    global BALL_X_SPEED, BALL_Y_SPEED

    canvas.coords(
        ball,
        WIDTH/2-BALL_RADIUS,
        HEIGHT/2-BALL_RADIUS,
        WIDTH/2+BALL_RADIUS,
        HEIGHT/2+BALL_RADIUS
    )

    BALL_X_SPEED = random.choice([-INITIAL_SPEED, INITIAL_SPEED])
    BALL_Y_SPEED = random.choice([-INITIAL_SPEED, INITIAL_SPEED])

# =====================
# Game Loop
# =====================
def game():

    global BALL_X_SPEED
    global BALL_Y_SPEED
    global PLAYER_1_SCORE
    global PLAYER_2_SCORE

    # Gerak Paddle Player
    if move_up:
        if canvas.coords(player)[1] > 0:
            canvas.move(player,0,-8)

    if move_down:
        if canvas.coords(player)[3] < HEIGHT:
            canvas.move(player,0,8)

    # AI
    ai_pos = canvas.coords(ai)
    ball_pos = canvas.coords(ball)

    ai_center = (ai_pos[1]+ai_pos[3])/2
    ball_center = (ball_pos[1]+ball_pos[3])/2

    if ai_center < ball_center:
        canvas.move(ai,0,6)

    elif ai_center > ball_center:
        canvas.move(ai,0,-6)

    # Gerak Bola
    canvas.move(ball,BALL_X_SPEED,BALL_Y_SPEED)

    ball_pos = canvas.coords(ball)
    player_pos = canvas.coords(player)
    ai_pos = canvas.coords(ai)

    # Atas bawah
    if ball_pos[1] <= 0 or ball_pos[3] >= HEIGHT:
        BALL_Y_SPEED *= -1

    # Tabrak paddle kiri
    if (
        ball_pos[0] <= player_pos[2]
        and ball_pos[3] >= player_pos[1]
        and ball_pos[1] <= player_pos[3]
    ):
        BALL_X_SPEED *= -1

    # Tabrak paddle kanan
    if (
        ball_pos[2] >= ai_pos[0]
        and ball_pos[3] >= ai_pos[1]
        and ball_pos[1] <= ai_pos[3]
    ):
        BALL_X_SPEED *= -1

    # Skor
    if ball_pos[0] <= 0:
        PLAYER_2_SCORE += 1
        canvas.itemconfig(score2,text=str(PLAYER_2_SCORE))
        reset_ball()

    elif ball_pos[2] >= WIDTH:
        PLAYER_1_SCORE += 1
        canvas.itemconfig(score1,text=str(PLAYER_1_SCORE))
        reset_ball()

    root.after(20,game)

# =====================
# Mulai Game
# =====================
game()

root.mainloop()