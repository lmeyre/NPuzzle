# NPuzzle

The goal of this project is to solve the N-puzzle ("taquin" in French) game using the A*
search algorithm or one of its variants

Run the program without argument to see the helper with all the differents options.

The program can run with 4 differents heuristics : `Manhattan` | `Out of place` | `Linear Conflict` | `Corner Tiles`

The program can have differents goals states : `Snail` or `Classic`

The program can use multiples pathing algorithm : `a_star` | `ida_star` | `greedy` | `uniform_cost`

There is also some small options, like performance optimisation that will reduce the overall time, but might not have the optimal path.

```
pip install -r requirements.txt
```
