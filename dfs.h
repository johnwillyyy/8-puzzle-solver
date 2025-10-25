#ifndef DFS_H
#define DFS_H

#include <vector>
#include "search_result.h"

SearchResult dfs(int initial_state, int goal_state);

int dfs_recursive(
    int current_state,
    int goal_state,
    std::vector<bool> &vis,
    std::vector<int> &parent,
    int depth,
    int &max_depth,
    int &nodes_expanded
);

#endif
