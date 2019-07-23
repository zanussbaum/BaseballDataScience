
import numpy as np
from timeit import default_timer as timer
from play_by_play import Season
from pymongo import MongoClient
from bson.objectid import ObjectId
from game_state import GameState


class Data:
    def __init__(self, start_year, end_year, new_database):
        client = MongoClient()
        self.db = client['game_play_by_play_{}_{}'.format(start_year, end_year)]
        self.collection = self.db.plays
        if new_database:
            self.season = Season(start_year, end_year)
            client.drop_database('game_play_by_play_{}_{}'.format(start_year, end_year))
            self.insert()
            
        self.plays = self._find()
       
    def insert(self):
        self._ids = self.collection.insert_many(self.season.play_by_play)

    def _find(self):
        return list(self.collection.find({},{'_id': 0 }))
    def _find_one(self,game_id):
        return self.collection.find_one({'_id':ObjectId(game_id)})

    def iterate_game(self, game):
        """Create 24X7 matrix
                Each row is the scenario, column is event
        count number of occurances 
        This will be X values
        Each inning is a single input 

        also create 1X7 of number of runs scored 
        this will be the y values 
        Could be also 24X7 

        Need to make sure that you keep track of runs scored that inning 

        Maybe helper to split up innings 
        then count runs from scenario 
        """
        runs = 0
        X = []
        Y = []
        inning_state = GameState()
        for key, inning in game.items():
            for event in inning:
                #means end of the inning, create new Inning Captor
                if inning_state.outs == 3:
                    print(inning_state.X)
                    X.append(inning_state.X)
                    inning_state = GameState()
                
                inning_state.update(event)

        print(len(X))

        

if __name__ == '__main__':
    data = Data(2017,2017,False)
    data.iterate_game(data.plays[0])
    

    
