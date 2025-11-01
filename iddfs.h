#ifndef IDDFS_H
#define IDDFS_H

#include <vector>
#include "search_result.h"

SearchResult iddfs(int initial_state, int goal_state);

int dfs_recursive_with_unmarking_backtrack(
    int current_state,
    int goal_state,
    std::vector<bool> &vis,
    std::vector<int> &parent,
    int max_level_to_explore,
    int depth,
    int &max_depth,
    int &nodes_expanded
);

#endif
