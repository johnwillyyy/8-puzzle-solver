#ifndef SEARCH_RESULT_H
#define SEARCH_RESULT_H

#include <vector>

struct SearchResult {
    std::vector<int> parent;
    int nodes_expanded;
    int search_depth;
    long long runtime_ms; // running time in milliseconds
};

#endif
