#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <sstream>
#include "puzzle_utils.h"
#include "bfs.h"
#include "dfs.h"
#include "iddfs.h"
#include "a_star.h"
#include "search_result.h"

using namespace std;
using namespace std::chrono;

string board_to_json(const vector<vector<int>>& board) {
    stringstream ss;
    ss << "[";
    for (int i = 0; i < 3; i++) {
        ss << "[";
        for (int j = 0; j < 3; j++) {
            ss << board[i][j];
            if (j < 2) ss << ",";
        }
        ss << "]";
        if (i < 2) ss << ",";
    }
    ss << "]";
    return ss.str();
}

void output_json_result(const string &algorithm, const SearchResult &result, int goal_state) {
    if (result.parent[goal_state] == -1) {
        cout << "{\"error\":\"No solution found\",\"algorithm\":\"" << algorithm << "\"}\n";
        return;
    }

    // Reconstruct path
    int current = goal_state;
    vector<int> path;
    while (current != -1) {
        path.push_back(current);
        current = result.parent[current];
    }
    reverse(path.begin(), path.end());

    // Output JSON
    cout << "{\n";
    cout << "  \"algorithm\":\"" << algorithm << "\",\n";
    cout << "  \"cost\":" << (path.size() - 1) << ",\n";
    cout << "  \"nodes_expanded\":" << result.nodes_expanded << ",\n";
    cout << "  \"search_depth\":" << result.search_depth << ",\n";
    cout << "  \"runtime_ms\":" << result.runtime_ms << ",\n";
    cout << "  \"path\":[\n";
    
    for (int i = 0; i < path.size(); i++) {
        vector<vector<int>> board = decode(path[i]);
        cout << "    " << board_to_json(board);
        if (i < path.size() - 1) cout << ",";
        cout << "\n";
    }
    
    cout << "  ]\n";
    cout << "}\n";
}

int main(int argc, char* argv[]) {
    if (argc < 11) {
        cerr << "Usage: " << argv[0] << " <algorithm> <9 numbers for board>\n";
        cerr << "Algorithms: bfs, dfs, iddfs, astar_manhattan, astar_euclidean\n";
        return 1;
    }

    init_factorial();

    string algorithm = argv[1];
    vector<vector<int>> board(3, vector<int>(3));
    
    // Read board from command line arguments
    int idx = 2;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            board[i][j] = atoi(argv[idx++]);
        }
    }

    int encoded_init_state = encode(board);
    int encoded_goal_state = encode(goal);

    SearchResult result;
    auto start = high_resolution_clock::now();

    if (algorithm == "bfs") {
        result = bfs(encoded_init_state, encoded_goal_state);
    } else if (algorithm == "dfs") {
        result = dfs(encoded_init_state, encoded_goal_state);
    } else if (algorithm == "iddfs") {
        result = iddfs(encoded_init_state, encoded_goal_state);
    } else if (algorithm == "astar_manhattan") {
        result = a_star(encoded_init_state, encoded_goal_state, heuristic_manhattan);
    } else if (algorithm == "astar_euclidean") {
        result = a_star(encoded_init_state, encoded_goal_state, heuristic_euclidean);
    } else {
        cerr << "{\"error\":\"Unknown algorithm: " << algorithm << "\"}\n";
        return 1;
    }

    auto end = high_resolution_clock::now();
    result.runtime_ms = duration_cast<milliseconds>(end - start).count();

    output_json_result(algorithm, result, encoded_goal_state);

    return 0;
}