#include "puzzle_utils.h"
#include "a_star.h"
#include <queue>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <cmath>  // for sqrt, pow

// ---------------- Heuristics ----------------

int heuristic_euclidean(int state) {
    std::vector<std::vector<int>> s = decode(state);

    std::pair<int,int> pos[9];
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            pos[goal[i][j]] = {i, j};

    double dist = 0.0;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            int tile = s[i][j];
            if (tile == 0) continue; // usually skip the blank
            auto [gx, gy] = pos[tile];
            dist += std::sqrt(std::pow(i - gx, 2) + std::pow(j - gy, 2));
        }
    }

    return static_cast<int>(dist);
}

int heuristic_manhattan(int state) {
    std::vector<std::vector<int>> s = decode(state);

    std::pair<int,int> pos[9];
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            pos[goal[i][j]] = {i, j};

    int dist = 0;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++) {
            int tile = s[i][j];
            if (tile == 0) continue;
            auto [gx, gy] = pos[tile];
            dist += abs(i - gx) + abs(j - gy);
        }

    return dist;
}

// ---------------- A* Algorithm ----------------

SearchResult a_star(int initial_state, int goal_state, int (*heuristic_fn)(int)) {
    using Node = std::pair<int, int>; // {f-cost, state}
    auto cmp = [](const Node& a, const Node& b) {
        return a.first > b.first; // smaller f comes first
    };

    std::priority_queue<Node, std::vector<Node>, decltype(cmp)> frontier(cmp);
    std::unordered_map<int, int> g_cost;
    std::vector<bool> visited(MAX_STATES, false);
    std::vector<int> parent(MAX_STATES, -1);

    int nodes_expanded = 0;
    int search_depth = 0;

    frontier.push({0, initial_state});
    g_cost[initial_state] = 0;

    while (!frontier.empty()) {
        int state = frontier.top().second;
        frontier.pop();
        nodes_expanded++;

        if (state == goal_state) {
            SearchResult res;
            res.parent = parent;
            res.nodes_expanded = nodes_expanded;
            res.search_depth = search_depth;
            return res;
        }

        for (int nb : get_neighbours(state)) {
            int new_g = g_cost[state] + 1;
            if (!g_cost.count(nb) || new_g < g_cost[nb]) {
                g_cost[nb] = new_g;
                int f = new_g + heuristic_fn(nb);
                frontier.push({f, nb});
                parent[nb] = state;
                search_depth = std::max(search_depth, new_g);
            }
        }
    }

    SearchResult failed;
    failed.parent = parent;
    failed.nodes_expanded = nodes_expanded;
    failed.search_depth = search_depth;
    return failed;
}
