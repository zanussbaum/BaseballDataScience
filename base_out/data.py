import time
import numpy as np
from timeit import default_timer as timer
from play_by_play import Season
from game_state import GameState

class Data:
    def __init__(self, start_year, end_year, new_pkl):
        if new_pkl:
            self.season = Season(start_year, end_year)
            self.save()
            
        self.plays = self.load()
        self.X = []
        self.y = []
       
    def save(self):
        """Overwritten pymongo insert method for data class 
        """
        np.save('play_by_play',np.array(self.season.play_by_play))
        print('saved data')

    def load(self):
        print('loading data')
        return np.load('play_by_play.npy')

    def _iterate_game(self, game):
        """Private method that iterates over
        the event in every inning
        """
        inning_state = GameState()
        for key, inning in game.items():
            for event in inning:
                #means end of the inning, create new Inning Captor
                if inning_state.outs == 3:
                    self.X.append(inning_state.X)
                    self.y.append(inning_state.runs_scored)
                    inning_state = GameState()
                
                inning_state.update(event)
            
    def generate_data(self):
        """Generate the X data and y labels
        """
        for play in self.plays:
            self._iterate_game(play)

        np.save('x_data',np.array(self.X))
        np.save('y_data', np.array(self.y))


if __name__ == '__main__':
    data = Data(2014,2018,True )
    data.generate_data()
    

    
