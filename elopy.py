"""
Created 5-18-17
All of the classes for EloPy. The users should only interact with the Implementation class.
@author - Hank Hang Kai Sheehan

Modified 6-20-18
Tentative implementation for games with scores following https://www.eloratings.net methodology
@author - Felippe Rodrigues
"""

class Implementation:
    """
    A class that represents an implementation of the Elo Rating System
    """

    def __init__(self, base_rating=1000):
        """
        Runs at initialization of class object.
        @param base_rating - The rating a new player would have
        """
        self.base_rating = base_rating
        self.players = []

    def __getPlayerList(self):
        """
        Returns this implementation's player list.
        @return - the list of all player objects in the implementation.
        """
        return self.players

    def getPlayer(self, name):
        """
        Returns the player in the implementation with the given name.
        @param name - name of the player to return.
        @return - the player with the given name.
        """
        for player in self.players:
            if player.name == name:
                return player
        return None

    def contains(self, name):
        """
        Returns true if this object contains a player with the given name.
        Otherwise returns false.
        @param name - name to check for.
        """
        for player in self.players:
            if player.name == name:
                return True
        return False

    def addPlayer(self, name, rating=None):
        """
        Adds a new player to the implementation.
        @param name - The name to identify a specific player.
        @param rating - The player's rating.
        """
        if rating == None:
            rating = self.base_rating

        self.players.append(_Player(name=name,rating=rating))

    def removePlayer(self, name):
        """
        Adds a new player to the implementation.
        @param name - The name to identify a specific player.
        """
        self.__getPlayerList().remove(self.getPlayer(name))


    def recordMatch(self, name1, name2, location=None, score=[]):
        """
        Should be called after a game is played.
        @param name1 - name of the first player.
        @param name2 - name of the second player.
        """
        player1 = self.getPlayer(name1)
        player2 = self.getPlayer(name2)

        expected1 = player1.getWinExpectancy(player2, location)
        expected2 = player2.getWinExpectancy(player1, location)
        
        k = len(self.__getPlayerList()) * 42

        rating1 = player1.rating
        rating2 = player2.rating

        if score[0] == score[1]:
            result1 = 0.5
            result2 = 0.5
        elif score[0] > score[1]:
            result1 = 1.0
            result2 = 0.0
        elif score[0] > score[1]:
            result1 = 0.0
            result2 = 1.0
        else:
            raise InputError('A score must be informed')
        
        diff = abs(score[0] - score[1])
        
        if diff == 2:
            adj = (1 + 1/2) # increase by half
        elif diff == 3:
            adj = (1 + 3/4) # increase by 3/4
        elif diff > 3:
            adj = (1 + 3/4 + (diff-3)/8) # increase by 3/4 plus differential
        else:
            adj = 1
            
        newRating1 = rating1 + k * adj * (result1 - expected1)
        newRating2 = rating2 + k * adj * (result2 - expected2)

        if newRating1 < 0:
            newRating1 = 0
            newRating2 = rating2 - rating1

        elif newRating2 < 0:
            newRating2 = 0
            newRating1 = rating1 - rating2

        player1.rating = newRating1
        player2.rating = newRating2

    def getPlayerRating(self, name):
        """
        Returns the rating of the player with the given name.
        @param name - name of the player.
        @return - the rating of the player with the given name.
        """
        player = self.getPlayer(name)
        return player.rating

    def getRatingList(self):
        """
        Returns a list of tuples in the form of ({name},{rating})
        @return - the list of tuples
        """
        lst = []
        for player in self.__getPlayerList():
            lst.append((player.name,player.rating))
        return lst

class _Player:
    """
    A class to represent a player in the Elo Rating System
    """

    def __init__(self, name, rating):
        """
        Runs at initialization of class object.
        @param name - TODO
        @param rating - TODO
        """
        self.name = name
        self.rating = rating

    def getWinExpectancy(self, opponent, location=None):
        """
        Compares the two ratings of the this player and the opponent.
        @param opponent - the player to compare against.
        @param location - check for home_factor.
        @returns - The expected score between the two players.
        """
        
        if location == self.name:
            home_factor = 100
        elif location == opponent.name:
            home_factor = -100
        else:
            home_factor = 0
            
        return ( 1+10**( ( opponent.rating - (self.rating + home_factor) )/400.0 ) ) ** -1
