
# Connect 4 Minimax AI

An Ai using the minimax algorithm with alpha-beta pruning to beat humans at connect 4.


## Features

- Minimax algorithm
- Alpha-Beta Pruning
- Move exploration order
  
## Future Improvements/ Optimisations 
- Transposition table using zorbist hashing
    - Caches outcomes of past computations so time is not wasted re-evaluating the same state again. This is needed as when the tree is traversed positions are analysed more than once which can be reached from a different combination of moves. This solution would trade computation time against memory to increse the depth of traversal possible in a given time. 
- Multithreading
    - Each branch from root node (current board state) can be traversed and evaluated in parallel reducing processing time by up to 1/7 (assuming no other bottlenecks)

  