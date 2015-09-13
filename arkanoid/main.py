from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
    ObjectProperty, ListProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color

from random import randint


class ArkanoidBreakable(Widget):
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            offset = (ball.center_x - self.center_x) / (self.width / 2)
            vx, vy = ball.velocity
            ball.velocity = vx + offset, vy * -1
            return True
        return False


class ArkanoidPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            offset = (ball.center_x - self.center_x) / (self.width / 2)
            vx, vy = ball.velocity
            bounced = Vector(vx, -1 * vy)
            vel = bounced * 1.025
            ball.velocity = vel.x + offset, vel.y


class ArkanoidBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class ArkanoidGame(Widget):
    ball = ObjectProperty(None)
    breakables = ListProperty(None)
    broken = ListProperty(None)
    player = ObjectProperty(None)

    game_over = StringProperty("")

    def serve_ball(self, vel=(0, -7)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def create_breakables(self, rows=7, row_items=8, size_y=30):
        def color():
            return randint(0, 256) / 256.0

        size_x = (Window.width - row_items) / row_items
        pos_x, pos_y = 0, Window.height - size_y

        available_colors = [[color(), color(), color()] for _ in range(0, rows)]
        for current in range(0, rows * row_items):
            breakable = ArkanoidBreakable(size=(size_x, size_y),
                                          pos=(pos_x, pos_y))

            with breakable.canvas.before:
                c = available_colors[current / row_items]
                Color(c[0], c[1], c[2], 1)

            self.breakables.append(breakable)
            self.add_widget(breakable)

            if (current + 1) % row_items == 0:
                pos_x = 0
                pos_y -= breakable.size[1] + 1
            else:
                pos_x += breakable.size[0] + 1

    def check_breakables_bounce(self):
        bounced = False
        for breakable in self.breakables:
            if not bounced and breakable not in self.broken:
                bounced = breakable.bounce_ball(self.ball)
                if bounced:
                    self.player.score += 100
                    self.remove_widget(breakable)
                    self.broken.append(breakable)

    def check_ball_position(self):
        if self.ball.y < self.y:
            self.player.score -= 1000
            self.serve_ball()

        if self.ball.top > self.top:
            self.ball.velocity_y *= -1

        if self.ball.x < self.x:
            self.ball.velocity_x *= -1

        if self.ball.right > self.width:
            self.ball.velocity_x *= -1

    def check_game_over(self):
        if self.player.score < 0 or set(self.broken) == set(self.breakables):
            # self.game_over = True
            self.remove_widget(self.ball)
            if self.player.score < 0:
                self.game_over = "Game Over"
            else:
                self.game_over = "You Win"

    def update(self, dt):
        if self.game_over:
            return

        self.ball.move()
        self.player.bounce_ball(self.ball)
        self.check_breakables_bounce()
        self.check_ball_position()
        self.check_game_over()

    def on_touch_move(self, touch):
        self.player.center_x = touch.x


class ArkanoidApp(App):
    def build(self):
        game = ArkanoidGame()
        game.create_breakables()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

ArkanoidApp().run()
