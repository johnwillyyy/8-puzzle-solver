#include <iostream>
#include <vector>
#include <algorithm>
#include "puzzle_utils.h"
#include "bfs.h"
#include "dfs.h"
#include "a_star.h"


void solve() {
    std::vector<std::vector<int>> board(3, std::vector<int>(3));
    for (auto &v : board)
        for (int &i : v)
            std::cin >> i;

    int encoded_init_state = encode(board);
    int encoded_goal_state = encode(goal);
    std::vector<int> parent = a_star(encoded_init_state, encoded_goal_state, heuristic_euclidean);
    
    if (parent[encoded_goal_state] == -2) {
        std::cout << "no solution found";
        return;
    }

    int current_state = encoded_goal_state;
    std::vector<int> path;
    while (current_state != -1) {
        path.push_back(current_state);
        current_state = parent[current_state];
    }

    std::reverse(path.begin(), path.end());

    std::cout<<"cost: "<<path.size()-1<<'\n';
    for (int i = 0; i < path.size(); i++){
        std::cout<<"step "<<i<<'\n';
        print_board(decode(path[i]));
        std::cout<<'\n';
    }
}

int main() {    
    init_factorial();
    while (true)
        solve();
    
    return 0;
}