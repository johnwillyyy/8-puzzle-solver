#include "iddfs.h"
#include "puzzle_utils.h"
#include <vector>
#include <algorithm>

SearchResult iddfs(int initial_state, int goal_state) {
    std::vector<int> parent(MAX_STATES, -1);
    std::vector<bool> vis(MAX_STATES, false);

    int nodes_expanded = 0;
    int max_depth = 0;

    int state = 0;

    for (int i = 0; state == 0; i++)
    {
        parent.assign(MAX_STATES, -1);
        vis.assign(MAX_STATES, false);
        nodes_expanded = 0;
        max_depth = 0;
        state = dfs_recursive_with_unmarking_backtrack(initial_state, goal_state, vis, parent, i, 0, max_depth, nodes_expanded);
    }

    SearchResult result;
    result.parent = parent;
    result.nodes_expanded = nodes_expanded;
    result.search_depth = max_depth;
    return result;
}

int dfs_recursive_with_unmarking_backtrack(
    int current_state,
    int goal_state,
    std::vector<bool> &vis,
    std::vector<int> &parent,
    int max_level_to_explore,
    int depth,
    int &max_depth,
    int &nodes_expanded
) {
    if(depth > max_level_to_explore)
        return 0;
    vis[current_state] = true;
    nodes_expanded++;
    max_depth = std::max(max_depth, depth);

    if (current_state == goal_state)
        return 1;

    int flag = false;
    for (int nb : get_neighbours(current_state)) {
        if (vis[nb]) continue;
        parent[nb] = current_state;
        int done = dfs_recursive_with_unmarking_backtrack(nb, goal_state, vis, parent, max_level_to_explore, depth + 1, max_depth, nodes_expanded);
        if (done == 0) flag = true;
        if (done == 1) return 1;
    }
    vis[current_state] = false;

    return flag? 0: -1;
}
