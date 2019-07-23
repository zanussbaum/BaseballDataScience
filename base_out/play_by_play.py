from statsapi import schedule, get
class Season:
    """ This class allows you to grab all play by play data for the calendar year
    It uses the statsapi module to call the MLB statsapi endpoint.
    Note this will take a while to import and use as one year of games has ~3000 
    games

    methods:
        _get_game_ids(): grabs all the game ids for the
        _get_play_by_play() grabs the play by play data for all specified games
            
    """
    def __init__(self, start_year, end_year):
        """Class object initializer
        Note this assumes that you want data for whole calendar years 

        Params:
            start_year: an int representing the start year
            end_year: an int representing the end year 
        """
        self.dates = {2017:('2017-04-02','2017-10-1')}
        if start_year > end_year:
            raise ValueError("The start year cannot be after the end year")
        if end_year-start_year > 0:
            start_date = self.dates[start_year][0]
            end_date = self.dates[end_year][1]
            date = (start_date,end_date)
            self.game_ids(date)
        else:
            self.game_ids = self._get_game_ids(self.dates[start_year])
        self.play_by_play = self._get_play_by_play()


    def _get_game_ids(self, date):
        """Grabs all the game ids for the given years

        Params:
            start_year: the starting year
            end_year: the end year 

        Returns:
            games: a list of all game ids within the time frame 
        """
        start_date = date[0]
        end_date = date[1]
        print("getting game ids from %s to %s" %(start_date, end_date))
        
        try:
            games = [str(game['game_id']) for game in schedule(start_date=start_date,end_date=end_date)]
            print("success getting game id's")
            return games
        except:
            print("failed to get the game id's")
        

    def _get_play_by_play(self):
        """Returns the play by play data for all games within the timeframe designated

        Returns:
            play_by_play: a dictionary of game_id mapped to play by play data 
        """
        play_by_play = []
        params = {}
        print("getting the play by play data")
        for this_game_id in self.game_ids:
            print("getting data for game %s" %this_game_id)
            params.update({'gamePk':this_game_id})
            games = get('game_playByPlay',params)
            this_game_plays = [[game['result'],game['count'],game['runners']] for game in games['allPlays']]
            play_by_play.append({this_game_id:this_game_plays})
        print("success")
        return play_by_play

if __name__ == '__main__':
    test = Season(2017,2018)
    print(test.game_ids)
    print(test.play_by_play)