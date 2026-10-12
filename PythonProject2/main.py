import pygame
import sys
import random
import math
import time

# ============ Настройки ============
WIN_W, WIN_H = 1100, 700
FPS = 60

WHEEL_RADIUS = 200
BALL_RADIUS  = 8

# Европейская рулетка
SECTORS = [
    0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,
    10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26
]
reds = {32,19,21,25,34,27,36,30,23,5,16,1,14,9,18,7,12,3}
COLORS = {n: ((0,160,0) if n==0 else (200,30,30) if n in reds else (0,0,0))
          for n in SECTORS}

GREEN  = (12,100,12)
WHITE  = (255,255,255)
BLACK  = (  0,  0,  0)
RED    = (200, 30, 30)
GRAY   = ( 50, 50, 50)
YELLOW = (240,240,20)


class Button:
    def __init__(self, rect, text, color=GRAY, fg=WHITE):
        self.rect  = pygame.Rect(rect)
        self.text  = text
        self.color = color
        self.fg    = fg
        self.font  = pygame.font.SysFont(None, 24)

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        txt = self.font.render(self.text, True, self.fg)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class RouletteGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Казино: Рулетка")
        self.clock = pygame.time.Clock()

        self.show_settings = False

        # Позиция колеса
        self.wheel_x = WIN_W//2 - 300
        self.wheel_y = WIN_H//2

        # Параметры спина
        self.spin_speed    = 2.0
        self.spin_time     = 5.0
        self.decel_start   = None
        self.initial_speed = None
        self.wheel_dir     = 1

        # Шарик
        self.ball_speed  = 0.0
        self.ball_dir    = 1
        self.lock_time   = 0.0
        self.locked      = False
        self.ball_offset = 0.0

        # Состояние
        self.wheel_ang  = 0.0
        self.ball_ang   = 0.0
        self.spinning   = False
        self.spin_start = 0.0

        # Баланс и ставки
        self.balance      = 1000
        self.bet_size     = 10
        self.bets_num     = {}
        self.bets_color   = {}
        self.bets_evenodd = {}
        self.bets_dozen   = {}
        self.bets_range   = {}
        self.last_win     = None

        # Основная UI-панель
        UI_X, UI_Y = 750, 20
        self.btns = {
            "spin":     Button((UI_X,   UI_Y,    100,40), "СПИН",      YELLOW),
            "refill":   Button((UI_X,   UI_Y+60,100,40), "Пополнить", RED),
            "bet-":     Button((UI_X+120,UI_Y+80,40,35), "-"),
            "bet+":     Button((UI_X+160,UI_Y+80,40,35), "+"),
            "red":      Button((UI_X,   UI_Y+130,100,35), "Красное",  color=RED,   fg=WHITE),
            "black":    Button((UI_X+110,UI_Y+130,100,35),"Чёрное",  color=BLACK, fg=WHITE),
            "even":     Button((UI_X,   UI_Y+180,100,35),"Чётное"),
            "odd":      Button((UI_X+110,UI_Y+180,100,35),"Нечётное"),
            "doz1":     Button((UI_X,   UI_Y+230,80,30),  "1–12"),
            "doz2":     Button((UI_X+90,UI_Y+230,80,30),"13–24"),
            "doz3":     Button((UI_X+180,UI_Y+230,80,30),"25–36"),
            "low":      Button((UI_X,   UI_Y+280,100,30),"1–18"),
            "high":     Button((UI_X+110,UI_Y+280,100,30),"19–36"),
            "settings": Button((20, WIN_H-60,120,40),    "Настройки")
        }

        # Меню настроек: справа от «Настройки», выравнено по нижнему краю
        sb = self.btns["settings"].rect
        bw, bh, gap = 80, 30, 5
        mx = sb.right + 10
        # Поднимаем меню так, чтобы его нижний край совпадал с нижним краем кнопки
        menu_height = 2*bh + gap
        my = sb.bottom - menu_height
        self.btns.update({
            "spd+": Button((mx,        my,       bw, bh), "Скор +"),
            "spd-": Button((mx,        my+bh+gap, bw, bh), "Скор -"),
            "t+":   Button((mx+bw+gap, my,       bw, bh), "Время +"),
            "t-":   Button((mx+bw+gap, my+bh+gap, bw, bh), "Время -")
        })

        self.create_bet_buttons()

    def create_bet_buttons(self):
        self.bet_buttons = []
        w, h = 50, 35
        x0, y0 = self.wheel_x + WHEEL_RADIUS + 50, 20
        for i, num in enumerate(SECTORS):
            col, row = divmod(i, 12)
            x = x0 + col*(w+5)
            y = y0 + row*(h+5)
            clr = COLORS[num]
            fg  = WHITE if clr!=(0,160,0) else BLACK
            b = Button((x,y,w,h), str(num), color=clr, fg=fg)
            self.bet_buttons.append((num, b))

    def start_spin(self):
        if self.spinning or not any((self.bets_num, self.bets_color,
                                     self.bets_evenodd, self.bets_dozen,
                                     self.bets_range)):
            return
        self.spinning     = True
        self.spin_start   = time.time()
        self.initial_speed= self.spin_speed
        self.decel_start  = self.spin_time * 0.6
        self.wheel_dir    = random.choice([1, -1])
        self.ball_dir     = random.choice([1, -1])
        self.ball_speed   = self.spin_speed * 3.5 * self.ball_dir
        self.ball_ang     = self.wheel_ang
        self.lock_time    = random.uniform(self.spin_time*0.3, self.spin_time*0.8)
        self.locked       = False

    def update(self, dt):
        if not self.spinning:
            return
        t = time.time() - self.spin_start
        # колесо с плавным торможением
        if t < self.spin_time:
            if t > self.decel_start:
                frac = (t - self.decel_start)/(self.spin_time - self.decel_start)
                speed = self.initial_speed * max(0,1-frac)
            else:
                speed = self.initial_speed
            self.wheel_ang += speed * dt * self.wheel_dir
        # шарик
        if not self.locked:
            self.ball_ang += self.ball_speed * dt
            if t >= self.lock_time:
                self.locked      = True
                self.ball_offset = self.ball_ang - self.wheel_ang
        else:
            self.ball_ang = self.wheel_ang + self.ball_offset
        r = WHEEL_RADIUS - BALL_RADIUS - 5
        self.ball_pos = (
            self.wheel_x + r*math.cos(self.ball_ang),
            self.wheel_y + r*math.sin(self.ball_ang)
        )
        if t > self.spin_time + 1.0:
            self.spinning = False
            self.resolve_bets()

    def resolve_bets(self):
        dx = self.ball_pos[0] - self.wheel_x
    dy = self.ball_pos[1] - self.wheel_y
    angle_ball = math.atan2(dy, dx) % (2*math.pi)
    angle_rel  = (angle_ball - self.wheel_ang) % (2*math.pi)
    sector_ang = 2*math.pi / len(SECTORS)
    idx        = int(angle_rel / sector_ang)
    win_num    = SECTORS[idx]

    # ✅ корректное определение цвета
    if win_num == 0:
        win_color = "зелёный"
    elif win_num in reds:
        win_color = "красный"
    else:
        win_color = "чёрный"

    self.last_win = (win_num, win_color)

    # Выплаты
    if win_num in self.bets_num:
        self.balance += self.bets_num[win_num] * 36
    if win_color in self.bets_color:
        self.balance += self.bets_color[win_color] * 2
    if win_num != 0:
        eo = "чётное" if win_num%2==0 else "нечётное"
        if eo in self.bets_evenodd:
            self.balance += self.bets_evenodd[eo] * 2
    if 1 <= win_num <= 12 and "1-12" in self.bets_dozen:
        self.balance += self.bets_dozen["1-12"] * 3
    if 13 <= win_num <= 24 and "13-24" in self.bets_dozen:
        self.balance += self.bets_dozen["13-24"] * 3
    if 25 <= win_num <= 36 and "25-36" in self.bets_dozen:
        self.balance += self.bets_dozen["25-36"] * 3
    if 1 <= win_num <= 18 and "1-18" in self.bets_range:
        self.balance += self.bets_range["1-18"] * 2
    if 19 <= win_num <= 36 and "19-36" in self.bets_range:
        self.balance += self.bets_range["19-36"] * 2

    # Очистка ставок
    self.bets_num.clear()
    self.bets_color.clear()
    self.bets_evenodd.clear()
    self.bets_dozen.clear()
    self.bets_range.clear()

    def draw_wheel(self):
        cx, cy = self.wheel_x, self.wheel_y
        n = len(SECTORS)
        for i, num in enumerate(SECTORS):
            a1 = i*(2*math.pi/n) + self.wheel_ang
            a2 = (i+1)*(2*math.pi/n) + self.wheel_ang
            pts = [(cx,cy)]
            for s in range(9):
                frac = s/8
                a = a1 + (a2-a1)*frac
                pts.append((cx + WHEEL_RADIUS*math.cos(a),
                            cy + WHEEL_RADIUS*math.sin(a)))
            pygame.draw.polygon(self.screen, COLORS[num], pts)
        pygame.draw.circle(self.screen, BLACK, (cx,cy), WHEEL_RADIUS+5, 5)
        font = pygame.font.SysFont(None, 20)
        for i, num in enumerate(SECTORS):
            a = (i+0.5)*(2*math.pi/n) + self.wheel_ang
            x = cx + (WHEEL_RADIUS-30)*math.cos(a)
            y = cy + (WHEEL_RADIUS-30)*math.sin(a)
            txt = font.render(str(num), True, WHITE)
            self.screen.blit(txt, txt.get_rect(center=(x,y)))

    def draw_ball(self):
        if hasattr(self, "ball_pos"):
            pygame.draw.circle(self.screen, WHITE,
                               (int(self.ball_pos[0]), int(self.ball_pos[1])),
                               BALL_RADIUS)

    def draw_ui(self):
        f = pygame.font.SysFont(None, 28)
        UI_X, UI_Y = 750, 20

        # Баланс и ставка
        self.screen.blit(f.render(f"Баланс: {self.balance}", True, WHITE),
                         (UI_X+120, UI_Y+10))
        self.screen.blit(f.render(f"Ставка: {self.bet_size}", True, WHITE),
                         (UI_X+120, UI_Y+60))

        # Основные кнопки
        main_keys = ("spin","refill","bet-","bet+",
                     "red","black","even","odd",
                     "doz1","doz2","doz3","low","high")
        for key in main_keys:
            self.btns[key].draw(self.screen)

        # Кнопка «Настройки»
        self.btns["settings"].draw(self.screen)

        # Кнопки чисел
        for _, b in self.bet_buttons:
            b.draw(self.screen)

        # Меню настроек (не перекрывает остальное)
        if self.show_settings:
            sb = self.btns["settings"].rect
            bw, bh, gap = 80, 30, 5
            mx = sb.right + 10
            menu_height = 2*bh + gap
            my = sb.bottom - menu_height
            # фон меню
            pygame.draw.rect(self.screen, (40,40,40),
                             (mx-5, my-5, 2*bw+gap+10, menu_height+10))
            # кнопки скорости/времени
            for key in ("spd+","spd-","t+","t-"):
                self.btns[key].draw(self.screen)
            # подписи
            small = pygame.font.SysFont(None, 20)
            self.screen.blit(small.render(f"Скорость: {self.spin_speed:.1f}", True, WHITE),
                             (mx, my-25))
            self.screen.blit(small.render(f"Время:    {self.spin_time:.1f}s", True, WHITE),
                             (mx + bw + gap, my-25))

        # Результат
        if self.last_win:
            num, col = self.last_win
            self.screen.blit(f.render(f"Выпало: {num} ({col})", True, YELLOW),
                             (750, WIN_H-60))

    def run(self):
        while True:
            dt = self.clock.tick(FPS)/1000.0
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    p = ev.pos
                    if self.btns["settings"].clicked(p):
                        self.show_settings = not self.show_settings
                    elif self.btns["spin"].clicked(p):
                        self.start_spin()
                    elif self.btns["refill"].clicked(p):
                        self.balance   = 1000
                        self.last_win = None
                    elif not self.spinning:
                        # изменение ставки
                        if self.btns["bet+"].clicked(p) and self.bet_size<100:
                            self.bet_size += 10
                        if self.btns["bet-"].clicked(p) and self.bet_size>10:
                            self.bet_size -= 10
                        # цвет, чет/нечет, дюжины, диапазоны
                        for key, mapping in (
                            ("red",    self.bets_color),
                            ("black",  self.bets_color),
                            ("even",   self.bets_evenodd),
                            ("odd",    self.bets_evenodd),
                            ("doz1",   self.bets_dozen),
                            ("doz2",   self.bets_dozen),
                            ("doz3",   self.bets_dozen),
                            ("low",    self.bets_range),
                            ("high",   self.bets_range),
                        ):
                            if self.btns[key].clicked(p) and self.balance>=self.bet_size:
                                k = self.btns[key].text
                                mapping[k] = mapping.get(k,0) + self.bet_size
                                self.balance -= self.bet_size
                        # числа
                        for num, btn in self.bet_buttons:
                            if btn.clicked(p) and self.balance>=self.bet_size:
                                self.bets_num[num] = self.bets_num.get(num,0)+self.bet_size
                                self.balance -= self.bet_size
                    # настройки
                    if self.show_settings:
                        if self.btns["spd+"].clicked(p) and self.spin_speed<10:
                            self.spin_speed += 0.5
                        if self.btns["spd-"].clicked(p) and self.spin_speed>0.5:
                            self.spin_speed -= 0.5
                        if self.btns["t+"].clicked(p):
                            self.spin_time += 1
                        if self.btns["t-"].clicked(p) and self.spin_time>1:
                            self.spin_time -= 1

            self.update(dt)
            self.screen.fill(GREEN)
            self.draw_wheel()
            self.draw_ball()
            self.draw_ui()
            pygame.display.flip()

if __name__ == "__main__":
    RouletteGame().run()