#include "bfs.h"
#include "puzzle_utils.h"
#include <queue>
#include <vector>
#include <algorithm>

std::vector<int> bfs(int initial_state, int goal_state) {
    std::queue<int> frontier;
    std::vector<bool> visited(MAX_STATES, false);
    std::vector<int> parent(MAX_STATES, -1);

    frontier.push(initial_state);
    visited[initial_state] = true;
    parent[initial_state] = -1;

    while (!frontier.empty()) {
        int state = frontier.front();
        frontier.pop();
        
        if (state == goal_state) 
            return parent;

        for (int nb : get_neighbours(state)) {
            if (visited[nb]) continue;
            visited[nb] = true;
            parent[nb] = state;
            frontier.push(nb);
        }
    }
    parent[goal_state] = -2;
    return parent;
}