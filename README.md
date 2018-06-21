# EloPy

A python library for the Elo Rating System created by [HandMD](https://github.com/HankMD/EloPy) and adapted by me to score-based games with home-field advantage. Implementation right now is tailored to football (soccer for americans).


## What is the Elo Rating System?
* The Elo Rating System (Elo) is a rating system used for rating players in games. Originally developed for chess by Arpad Elo, Elo has been applied to a large array of games.
* Each player is assigned a number as a rating. The system predicts the outcome of a match between two players by using an expected score formula (i.e. a player whose rating is 100 points greater than their opponent's is expected to win 64% of the time).
* Everytime a game is played, the Elo rating of the participants change depending on the outcome and the expected outcome. The winner takes points from the loser; the amount is determined by the players' scores and ratings
* A win is counts as a score of 1, loss is a score of 0, and draw is a score of 0.5


## Calculations

Win Expectancy:
`winExpectancy = 1 / ( 1 + 10 ** ( opponentRating - (teamRating + homeFactor) ) / 400.0 ) )`

Home Factor:
`+ 100` for teams playing at home
`- 100` for teams playing away
`0` for neutral venue

K:
Right now the K factor is set as `40` (constant). Working on adjusting for competition/game importance.

Score adjustment to K:
increase by `1/2` if game was won by 2 goals.
increase by `3/4` if game was won by 3 goals.
increase by `3/4 + (goalDiff-3)/8` if game was won by 3 or more goals, `goalDiff` being the absolute difference of goals.

Result:
`1` for win
`0.5` for draw
`0` for loss

Rating:
`newRating = oldRating + (k * adj) * (result1 - expected1)`


## Syntax when using EloPy

#### Creating your own implementation
```python
from elopy import *

i = Implementation()
```

#### Adding and removing players
```python
i.addPlayer("Brazil") #default ranking is 1000
i.addPlayer("Germany",rating=900)
i.addPlayer("Italy")

print(i.getPlayerRating("Brazil"), i.getPlayerRating("Germany"))
>>> 1000, 900

i.removePlayer("Italy")

print(i.getRatingList())
>>> [('Brazil', 1000), ('Germany', 900)]
```

#### Recording a match
```python
i.recordMatch("Brazil","Germany",score=[7,1],location=None) # score follows team names order

print(i.getRatingList())
>>> [('Brazil', 1089.25), ('Germany', 910.75)]
```
