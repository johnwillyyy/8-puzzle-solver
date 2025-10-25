#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include "puzzle_utils.h"
#include "bfs.h"
#include "dfs.h"
#include "a_star.h"
#include "search_result.h"

using namespace std;
using namespace std::chrono;

void print_analysis(const string &name, const SearchResult &result, int goal_state) {
    cout << "=============================\n";
    cout << "Algorithm: " << name << "\n";
    cout << "=============================\n";

    if (result.parent[goal_state] == -2) {
        cout << "No solution found.\n\n";
        return;
    }

    // reconstruct path
    int current = goal_state;
    vector<int> path;
    while (current != -1) {
        path.push_back(current);
        current = result.parent[current];
    }
    reverse(path.begin(), path.end());

    cout << "Path to goal:\n";
    for (int i = 0; i < path.size(); i++) {
        cout << "Step " << i << ":\n";
        print_board(decode(path[i]));
        cout << '\n';
    }

    cout << "Cost of path: " << path.size() - 1 << "\n";
    cout << "Nodes expanded: " << result.nodes_expanded << "\n";
    cout << "Search depth: " << result.search_depth << "\n";
    cout << "Running time: " << result.runtime_ms << " ms\n";
    cout << "-----------------------------\n\n";
}

int main() {
    init_factorial();

    vector<vector<int>> board(3, vector<int>(3));
    cout << "Enter initial board (3x3, 0 is blank):\n";
    for (auto &v : board)
        for (int &i : v)
            cin >> i;

    int encoded_init_state = encode(board);
    int encoded_goal_state = encode(goal);

    // BFS
    auto start = high_resolution_clock::now();
    SearchResult bfs_result = bfs(encoded_init_state, encoded_goal_state);
    auto end = high_resolution_clock::now();
    bfs_result.runtime_ms = duration_cast<milliseconds>(end - start).count();

    // DFS
    start = high_resolution_clock::now();
    SearchResult dfs_result = dfs(encoded_init_state, encoded_goal_state);
    end = high_resolution_clock::now();
    dfs_result.runtime_ms = duration_cast<milliseconds>(end - start).count();

    // A* Manhattan
    start = high_resolution_clock::now();
    SearchResult astar_manhattan = a_star(encoded_init_state, encoded_goal_state, heuristic_manhattan);
    end = high_resolution_clock::now();
    astar_manhattan.runtime_ms = duration_cast<milliseconds>(end - start).count();

    // A* Euclidean
    start = high_resolution_clock::now();
    SearchResult astar_euclidean = a_star(encoded_init_state, encoded_goal_state, heuristic_euclidean);
    end = high_resolution_clock::now();
    astar_euclidean.runtime_ms = duration_cast<milliseconds>(end - start).count();

    // Print analyses
    print_analysis("Breadth-First Search (BFS)", bfs_result, encoded_goal_state);
    print_analysis("Depth-First Search (DFS)", dfs_result, encoded_goal_state);
    print_analysis("A* (Manhattan Heuristic)", astar_manhattan, encoded_goal_state);
    print_analysis("A* (Euclidean Heuristic)", astar_euclidean, encoded_goal_state);

    return 0;
}
