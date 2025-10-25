#include "bfs.h"
#include "puzzle_utils.h"
#include <queue>
#include <vector>
#include <algorithm>

SearchResult bfs(int initial_state, int goal_state) {
    std::queue<int> frontier;
    std::vector<bool> visited(MAX_STATES, false);
    std::vector<int> parent(MAX_STATES, -1);
    std::vector<int> depth(MAX_STATES, 0);

    int nodes_expanded = 0;
    int max_depth = 0;

    frontier.push(initial_state);
    visited[initial_state] = true;

    while (!frontier.empty()) {
        int state = frontier.front();
        frontier.pop();
        nodes_expanded++;

        if (state == goal_state) {
            SearchResult result;
            result.parent = parent;
            result.nodes_expanded = nodes_expanded;
            result.search_depth = max_depth;
            return result;
        }

        for (int nb : get_neighbours(state)) {
            if (visited[nb]) continue;
            visited[nb] = true;
            parent[nb] = state;
            depth[nb] = depth[state] + 1;
            max_depth = std::max(max_depth, depth[nb]);
            frontier.push(nb);
        }
    }

    SearchResult result;
    result.parent = parent;
    result.nodes_expanded = nodes_expanded;
    result.search_depth = max_depth;
    return result;
}
