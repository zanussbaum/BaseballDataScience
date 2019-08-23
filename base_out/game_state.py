import numpy as np 

out_types = ['field_out', 'strikeout', 'sac_fly', 'sac_bunt', 'caught_stealing_3b',
'caught_stealing_2b', 'pickoff']
class GameState:
    def __init__(self):
       self.outs = 0
       self.runs_scored = 0
       self.scenarios = {0:0}
       self.runs_per_scenario = {'0':0}
       self.runners = {'1B':False,'2B':False, '3B':False}
       self.events = {'single':0, 'double':1, 'triple':2, 
       'home_run':3, 'field_error':4, 'hit_by_pitch':5, 
       'walk':6, 'strikeout':7, 'field_out':8}

       self.X = np.zeros((24,10))
    #    self.y = np.zeros((24,10))


    def __str__(self):
        s =  """
            .......{}.......
            ....../.\.....
            ...../...\.....
            ..../.....\....
            ../.........\..
            {}.............{}
            ..\........./..
            ...\....../...
            .....\.../.....
            ......\./......
            .......1.......
            """.format(int(self.runners['2B']),int(self.runners['3B']),int(self.runners['1B']))
        return s 

    def __repr__(self):
        return self.__str__()

    def update(self,event):
        result = event[0]
        count = event[1]
        runners = event[2]

        outs = count['outs']
        scored = 0

        #add events first, then add runs if people scored
        try:
            self._add_scenario(runners[0]['details']['eventType'])
        except Exception as e:
            print(e)
        
        for runner in runners:
            is_out = runner['movement']['isOut']
            start_base = runner['movement']['start']
            end_base = runner['movement']['end']
    
            if not is_out:
                if start_base is not None:
                    self.runners[start_base] = False
                    if end_base == 'score':
                        self.runs_scored += 1
                        # index = np.where(self.X >= 1)
                        # self.y[index] += 1
                    else:
                        self.runners[end_base] = True
                else:
                    if end_base == 'score':
                        self.runs_scored += 1
                        # index = np.where(self.X >= 1)
                        # self.y[index] += 1
                    else:
                        self.runners[end_base] = True
            else:
                self.outs += 1

        print("updated game state to {} outs and {} total runs scored".format(self.outs, self.runs_scored))
        print(self)
        print("for event {}\n".format(event))
        print("occurances matrix\n {}".format(self.X))
        print("number of runs scored for occurance\n {}\n".format(self.runs_scored))

    def _add_scenario(self,event):
        if event in self.events:
            event = self.events[event]
        else:
            event = 9
        if self.runners['1B']:
            if self.runners['2B']:
                if self.runners['3B']:
                    #bases loaded encoded as 7 
                    self.X[7*3 + self.outs, event] += 1
                else:
                    #1st and 2nd encoded as 4
                    self.X[4*3 + self.outs, event] += 1
            elif self.runners['3B']:
                #first and third encoded as 5
                self.X[5*3 + self.outs,event] += 1
            else:
                #first encoded as 1
                self.X[1*3 + self.outs,event] += 1
        elif self.runners['2B']:
            if self.runners['3B']:
                #second and third encoded as 6
                self.X[6*3 + self.outs, event] += 1
            else:
                #second encoded as 2
                self.X[2*3 + self.outs, event] += 1
        elif self.runners['3B']:
            #third encoded as 3
            self.X[3*3 + self.outs, event] += 1
        else:
            #bases empty encoded as 0
            self.X[self.outs, event] += 1

if __name__ == '__main__':
    inning = GameState()
    print(inning)

        
