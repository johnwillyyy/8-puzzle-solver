#include "dfs.h"
#include "puzzle_utils.h"
#include <vector>
#include <algorithm>

SearchResult dfs(int initial_state, int goal_state) {
    std::vector<int> parent(MAX_STATES, -1);
    std::vector<bool> vis(MAX_STATES, false);

    int nodes_expanded = 0;
    int max_depth = 0;

    dfs_recursive(initial_state, goal_state, vis, parent, 0, max_depth, nodes_expanded);

    SearchResult result;
    result.parent = parent;
    result.nodes_expanded = nodes_expanded;
    result.search_depth = max_depth;
    return result;
}

int dfs_recursive(
    int current_state,
    int goal_state,
    std::vector<bool> &vis,
    std::vector<int> &parent,
    int depth,
    int &max_depth,
    int &nodes_expanded
) {
    vis[current_state] = true;
    nodes_expanded++;
    max_depth = std::max(max_depth, depth);

    if (current_state == goal_state)
        return true;

    for (int nb : get_neighbours(current_state)) {
        if (vis[nb]) continue;
        parent[nb] = current_state;
        bool done = dfs_recursive(nb, goal_state, vis, parent, depth + 1, max_depth, nodes_expanded);
        if (done) return true;
    }

    return false;
}
