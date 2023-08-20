# Assignment 2 - Student's Report

Please make sure that the report is no longer than 500 words.

## Author: Francis Ozoka - 220228986

## Complexity of the Problem 

The complexity of the proble is O(b^d) in he worst case with alpha beta prunning. The best case is O(b^(d/2)) b being the branching factor and d being the search depth. This is computationaly intensive. In my implementation, depth of 4 seems to be the only reasonable option. On average, it took about 7 seconds for each move in the early stages of the game, getting faster as the number of empty cells decrease. The space complexity seems to be the same and lead to crashes.

## AI Techniques Considered

When trying to silve the problem, I considered MCTS, minimax alpha beta amd optimized minimax. 

MCTS never seems to be competitive enough, optimized minimax for some reason too longer when given same depth as minimax alpha beta, making deeper depths non feasible.

Eventually, i settled for minimax alpha beta which seemed to perfom better in terms of play and move times, though sometimes making aweful mistakes. The added complexity of power ups and popups makes it really hard to implement a straightforward soluton.

## Reflections

Figuring out how to include the advanced rules was the first hurfle to overcome. It took me a while to figure out that i had to check the board before including popups and power ups as legal actions.

Comming up with a grading system for moves seemed unachievable initially. I was forced to write my own functions to return openings in order to grade moves better. This seem to have some shortcomings as well, though sometimes it lead to a draw.

Overall I would say this activity was more challenging as i initially though and I think it is something to return to in the future when i have more time.