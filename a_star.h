#ifndef a_star_H
#define a_star_H


#include <vector>

std::vector<int> a_star(int initial_state, int goal_state,int (*heuristic_fn)(int));
int heuristic_manhattan(int state);
int heuristic_euclidean(int state);


#endif