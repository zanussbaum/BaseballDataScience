import numpy as np 

class GameState:
    def __init__(self):
       self.outs = 0
       self.runs = 0
       self.scenarios = {0:0}
       self.runs_per_scenario = {'0':0}
       self.runners = {'1B':False,'2B':False, '3B':False}
       self.events = {'single':0, 'double':1, 'triple':2, 
       'home_run':3, 'field_error':4, 'hit_by_pitch':5, 
       'walk':6, 'strikeout':7, 'field_out':8}

       self.X = np.zeros((24,10))
       self.Y = np.zeros((24,10))

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
        for runner in runners:
            is_out = runner['movement']['isOut']
            start_base = runner['movement']['start']
            end_base = runner['movement']['end']
    
            if not is_out:
                if start_base is not None:
                    self.runners[start_base] = False
                    self.runners[end_base] = True
                else:
                    self.runners[end_base] = True

            if runner['details']['isScoringEvent']:
                scored += 1
        print("updated game state to")
        print(self)

        self._add_scenario(runners[0]['details']['eventType'])

        if runners[0]['details']['eventType'] == 'field_out':
            self.outs += 1

    def _add_scenario(self,event):
        """Look at this
        Need to return the right scenario 
        Also add it to the right 
        Can probably just mutate X value here
        """
        if event in self.events:
            event = self.events[event]
        else:
            event = 9
        if self.runners['1B']:
            if self.runners['2B']:
                if self.runners['3B']:
                    #bases loaded encoded as 7 
                    self.X[7*3 + self.outs, event] += 1
                    #need to do bookeeping of what scenarios have occurred in this order
                    #to then add runs 
                    # if 'bases loaded' not in self.scenarios:
                        
                    # else:
                    #     self.scenarios.update({'bases loaded':self.scenarios.get('bases loaded') + 1})

                else:
                    #1st and 2nd encoded as 4
                    self.X[4*3 + self.outs, event] += 1
                    # if 'first and second' not in self.scenarios:
                    #     self.scenarios.update({'first and second':1})
                    # else:
                    #     self.scenarios.update({'first and second':self.scenarios.get('first and second')+ 1})
            elif self.runners['3B']:
                #first encoded as 1
                self.X[5*3 + self.outs,event] += 1
                # if 'first' not in self.scenarios:
                #     self.scenarios.update({'first':1})
                # else:
                #     self.scenarios.update({'first':self.scenarios.get('first')+ 1})
            else:
                #first encoded as 1
                self.X[1*3 + self.outs,event] += 1
                # if 'first' not in self.scenarios:
                #     self.scenarios.update({'first':1})
                # else:
                #     self.scenarios.update({'first':self.scenarios.get('first')+ 1})

        elif self.runners['2B']:
            if self.runners['3B']:
                #second and third encoded as 6
                self.X[6*3 + self.outs, event] += 1
                    # if 'second and third' not in self.scenarios:
                    #     self.scenarios.update({'second and third':1})
                    # else:
                    #     self.scenarios.update({'second and third':self.scenarios.get('second and third') + 1})
            else:
                #second encoded as 2
                self.X[2*3 + self.outs, event] += 1
                # if 'second' not in self.scenarios:
                #     self.scenarios.update({'second':1})
                # else:
                #     self.scenarios.update({'second':self.scenarios.get('second') + 1})

        elif self.runners['3B']:
            #third encoded as 3
            self.X[3*3 + self.outs, event] += 1
            # if 'third' not in self.scenarios:
            #         self.scenarios.update({'third':1})
            # else:
            #     self.scenarios.update({'third':self.scenarios.get('third') + 1})

        else:
            #bases empty encoded as 0
            self.X[self.outs, event] += 1
            # if 'bases empty' not in self.scenarios:
            #         self.scenarios.update({'bases empty':1})
            # else:
            #     self.scenarios.update({'bases empty':self.scenarios.get('bases empty') + 1})

            

if __name__ == '__main__':
    inning = GameState()
    print(inning)

        
