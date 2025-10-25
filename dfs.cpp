#include "dfs.h"
#include "puzzle_utils.h"
#include <vector>
#include <algorithm>

std::vector<int> dfs(int initial_state, int goal_state) {
    std::vector<int> parent (MAX_STATES, -1);
    std::vector<bool> vis (MAX_STATES);
    dfs(initial_state, goal_state, vis, parent);
    return parent;
}

int dfs(
    int current_state,
    int goal_state, 
    std::vector<bool> &vis, 
    std::vector<int> &parent
) {
    vis[current_state] = true;
    if(current_state == goal_state)
        return true;
    
    for (int nb : get_neighbours(current_state)){
        if(vis[nb]) continue;
        parent[nb] = current_state;
        bool done = dfs(nb, goal_state, vis, parent);
        if(done) return true;
    }
    return false;
}
