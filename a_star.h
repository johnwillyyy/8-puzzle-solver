#ifndef A_STAR_H
#define A_STAR_H

#include <vector>
#include "search_result.h"

SearchResult a_star(int initial_state, int goal_state, int (*heuristic_fn)(int));
int heuristic_manhattan(int state);
int heuristic_euclidean(int state);

#endif
