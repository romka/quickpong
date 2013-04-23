# Developed by Roman Arkharov, arkharov@gmail.com. 04.2013

"""
    Instance of this class is created for every game, it is contains information about every game and methods
    for change game state.

    see class Quickpong(), method checkWaitingList().
"""

from math import sin, cos, pi
from twisted.python import log


class QuickpongGame:
    """
      This class contain info about one game
      
      Statuses:
        prestart -- wait for both players click "start button"
        started -- both players click "start button", ball is launched
    """

    def __init__(self, gamer1, gamer2):
        self.gamer1 = gamer1
        self.gamer2 = gamer2
        self.status = 'prestart' # wait for both players click "start button"
        self.statuses = ['prestart', 'start']
        self.ball = {}
        self.ball['x'] = 120
        self.ball['y'] = 200
        #self.ball['x_client'] = []
        #self.ball['y_client'] = []
        self.ball['vector'] = 30
        #self.ball['vector'] = 0
        self.ball['speed'] = 10
        self.ball['default_speed'] = self.ball['speed']
        #self.ball['speed_delta'] = 0.2
        self.ball['speed_delta'] = 1
        self.pongs = 0
        self.game_data = []
        self.tick = 0
        self.score_left = 0
        self.score_right = 0
        self.left_y = 300.0
        self.right_y = 300.0
        self.data_frame = 0
        #self.force_counter = 10

        self.field_width = 800
        self.field_height = 600
        self.board_height = 100

        self.left_last_processed_frame = 0
        self.right_last_processed_frame = 0

        self.bounce_range = -50

    def gamers_list(self):
        return [self.gamer1.client_id, self.gamer2.client_id]

    def set_status(self, status):
        if status in self.statuses:
            self.status = status
        else:
            pass

    """
    def get_ball(self):
        return self.ball
    """

    """
    def set_ball(self, new_ball):
        self.ball['x'] = new_ball['x']
        self.ball['y'] = new_ball['y']
        self.ball['vector'] = new_ball['vector']
        self.ball['speed'] = new_ball['speed']
    """

    def update_ball(self):
        """
            Recalculate ball and boards positions.
        """
        if self.ball['y'] >= self.field_height and self.ball['vector'] >= 0 and self.ball['vector'] <= 180:
            self.ball['vector'] = 360 - self.ball['vector']

        if self.ball['y'] <= 0 and self.ball['vector'] >= 180 and self.ball['vector'] <= 360:
            self.ball['vector'] = 360 - self.ball['vector']
            #print 'VER CHAGE %s' % self.ball['vector']

        # pong from the vertical walls
        if self.ball['x'] >= self.field_width and ((self.ball['vector'] >= 0 and self.ball['vector'] < 90) or (
                self.ball['vector'] > 270 and self.ball['vector'] <= 360)):
            self.ball['vector'] = -self.ball['vector'] + 360 + 180
            self.score_left += 1
            self.ball['speed'] = self.ball['default_speed']

        if self.ball['x'] <= 0 and self.ball['vector'] >= 90 and self.ball['vector'] <= 270:
            self.ball['vector'] = -self.ball['vector'] + 360 + 180
            self.score_right += 1
            self.ball['speed'] = self.ball['default_speed']

        # pong from the right player board
        if self.gamer2.data != 'init data':
            if self.ball['x'] >= 765 and self.ball['y'] > (self.right_y) and self.ball['y'] < (self.right_y + 100) and ((self.ball['vector'] >= 0 and self.ball['vector'] < 90) or (self.ball['vector'] > 270 and self.ball['vector'] <= 360)):
                old_vector = self.ball['vector']
                #self.ball['vector'] = -self.ball['vector'] + 360 + 180 - (self.ball['y'] - self.right_y + self.bounce_range) / 4
                self.ball['vector'] = -self.ball['vector'] + 360 + 180
                self.ball['speed'] += self.ball['speed_delta']
                log.msg('right pong: before %d after %d. Angle change %d' % (old_vector, self.ball['vector'], (self.ball['y'] - self.right_y + self.bounce_range)))

        # pong from the left player board
        if self.gamer1.data != 'init data':
            if self.ball['x'] <= 35 and self.ball['y'] > (self.left_y) and self.ball['y'] < (self.left_y + 100) and self.ball['vector'] >= 90 and self.ball['vector'] <= 270:
                old_vector = self.ball['vector']
                self.ball['vector'] = -self.ball['vector'] + 360 + 180
                self.ball['speed'] += self.ball['speed_delta']
                log.msg('left pong: before %d after %d' % (old_vector, self.ball['vector'] ))

        if self.ball['vector'] < 0:
            self.ball['vector'] += 360
        elif self.ball['vector'] > 360:
            self.ball['vector'] -= 360

        vector_rad = self.ball['vector'] * pi / 180

        # Real ball coordinates for server calculations.
        delta_x = self.ball['speed'] * round(cos(vector_rad), 3)
        delta_y = self.ball['speed'] * round(sin(vector_rad), 3)
        self.ball['delta_x'] = delta_x
        self.ball['delta_y'] = delta_y
        self.ball['x'] += delta_x
        self.ball['y'] += delta_y
        self.ball['x'] = round(self.ball['x'], 3)
        self.ball['y'] = round(self.ball['y'], 3)

        self.ball['score_left'] = self.score_left
        self.ball['score_right'] = self.score_right

        return self.ball

