#ifndef DFS_H
#define DFS_H

#include <vector>

std::vector<int> dfs(int initial_state, int goal_state);
int dfs(
    int current_state,
    int goal_state, 
    std::vector<bool> &vis, 
    std::vector<int> &parent
);

#endif