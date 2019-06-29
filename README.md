# Chexers

## Overview

In this project part B, we need to implement a game playing program, so that it will be able to play a 3-player Chexers game. In order to play such a game, we start with creating a module named ***player.py***. This player module is created to interact with the ***referee*** package provided, thereby an internal state of the game can be created and updated. Using this internal game state, the player will then be able to choose the best possible action based on its knowledge of the game. In order to handle the game state more efficiently, we created another module named ***state.py***. This module contains a ***state*** class, which is used to represent the internal game state. In order to select the best action to be executed, we created a module named ***max_n.py*** to simulate the max-n algorithm, which will do a 3-ply search to find out the state with the highest evaluation score. This evaluation score is calculated based on a set of features, with their corresponding weights, which will be explained in more details in later sections. In order to find a set of accurate weights, so that the evaluation function will be as close as possible in approximating the utility value of the state, we created a ***TDLeaf.py*** module to update the weights according to the game states.


## General Approach

*Describe the approach your game-playing program uses for deciding on which actions to take. Comment on your search strategy, including on how you have handled the 3-player nature of the game. Explain your evaluation function and its features, including their strategic motivations.*

In order to decide which action to take, we used the ideas from the minimax algorithm, where we make the assumption that our opponents will always choose the actions that will lead to a game state that favour them the most. Based on this assumption, we can try to predict our opponents’ behaviours, which allows to find the action that will most likely lead us to our desired game state. This is the general idea of the ***max-n*** algorithm. One of the key component that determines the effectiveness of this algorithm is how well our evaluation function predicts the actual utility value of the game state. After analysing some of the game patterns and rules, we chose the following the features to evaluate the game state:

**Features**

- The total distance between each piece and the exit cell
- The number of pieces that need to exit to win the game
- The number of extra pieces besides the number of pieces needed to win the game
- The total number of pieces that have exited from the board for our opponents

**Motivations**

- The motivation behind the first feature is very straightforward. In order to win the game, the pieces need to get as close as possible to the exit cells and exit from board throughout the entire game. Therefore, a game state is generally good if the Chexers’ pieces can get close the the exit cells.
- The motivation behind the second feature is to encourage the pieces to exit when possible. To be more specific, this feature is used to reward the exit action when a piece lands on an exit cell.
- The motivation behind the third feature is to encourage the player to capture the opponents’ pieces while not being captured.
- The motivation for the final feature is to give penalty to the game state where our opponents can exit from board.

## Machine Learning

*If you have applied machine learning, discuss the learning methodology you followed for training and the intuition behind using that speciﬁc technique.*

Since we’re using the evaluation function to determine how good or bad a game state is, the accuracy of the evaluation function in approximating the utility value of the game state will become crucial to the success of this Chexers playing program. In order to get an accurate evaluation function, having a set of good weights to adjust the feature value can lead to a more accurate approximation. Therefore, some machine learning techniques can be applied to get the program to learn from the previous games, and adjust the weights accordingly. We chose **TDLeaf(λ) algorithm**, which is a variation of the Temporal Difference Learning. The reason we chose this algorithm is because it doesn't need to know the actual utility value of a game state to update the weights of the evaluation function, and this algorithm can be directly applied to the minimax search algorithm.

**TDLeaf(λ)**

The main idea behind this algorithm is to adjust the weights, so that the predicted reward between successive states will become stable. If the evaluation function is stable in predicting the game state score up to the final game state, then this can make the program to gradually approach to the winning game state.


## Overall Effectiveness

*Comment on the overall eﬀectiveness of your game-playing program. If you have created multiple game-playing programs using diﬀerent techniques, compare their relative eﬀectiveness.*

We have mainly used two approaches to solve this problem:

- Self Learning Player, which is a player uses machine learning technique to update the weights of the evaluation function.
- Expert Player, which is a player that uses expert knowledge to design the evaluation function.

**Self Learning Player**

This player uses the TDLeaf(λ) algorithm, and learnt a set of weights. During the learning phase of this player, we realised that the weights are not being significant updated. Another problem we faced is that a self learning player will learn a set of different weights when facing different opponents, which makes the weights unstable.

**Expert Player**

This player uses the Expert System approach to design its evaluation function. In other words, this player’s evaluation function is constructed based on our knowledge of the game. The main features implemented are quite similar to the self learning player, but the main difference is that we use conditional statements to determine the score of the game state.

After compare the generall performance, the expert player has a much better performance than the self learning player, because there might not be enough features for the self learning player to correctly evaluate the game state. Although, the expert player is much more simpler than the self-learning player, it can correctly give an evaluation to the state. This is very crucial in the success of a Chexers playing program.

## Creativity

*Include a discussion of any particularly creative techniques you have applied (such as evaluation function design, search strategy optimisations, specialised data structures, other optimisations, or any search algorithms not discussed in lectures) or any other creative aspects of your solution, or any additional comments you wish to be considered by the markers.*

**Genetic Algorithm**

For other search algorithm, we also considered one of the evolutionary algorithms called genetic algorithm. However, we thought this algorithm may not feasible due to the complexity in its implementation sense. The basic idea is to use this algorithm instead of max-n to decide a best action for each turn based on the evaluation of states.

Generally, the generic algorithm requires a population of candidates and applies crossover and mutations to generate a best solution. We want to use it to find a best action so the candidate population should be a group of possible actions. The evaluation of each action is the same as the method in max-n, which is by evaluating the corresponding resulted state. One aspect which makes it much abstract and complex to implement is applying generic operators like crossover and mutations. We can easily select a portion of best candidates from all possible actions but it is difficult to apply changes to them in the sense of the game. Any changes to a tuple representing a valid action may result in an invalid action, not to mention to generate a new generation of actions.

Another difficulty might be the stop point. Even if we managed to figure  out a way to produce new generation of actions, it is hard to decide at which point should we stop it and return the current best result. Lots of examples and reports online have demonstrated the generic algorithm by evolving random dataset to a desired state. However, in the case of chexers, we could not decide the best state in most cases. Other suggestion of a stop point might be when the evaluation of the new generation reaches a stable state. But to reach a stable state might take a long time and also that since our evaluation function is not guaranteed to be accurate, the stable state may not be as good as we expected.


## Conclusion

After implementing both of the two kinds of players, we realised the difficulty in implementing a player that can learn from its previous game states. Even though, the machine learning techniques will be very useful in an advanced level of game playing, but it will require a much careful thinking and design to achieve the same performance, where a player with expert knowledge can achieve easily with much less efforts to design. 
