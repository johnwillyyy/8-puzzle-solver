#ifndef PUZZLE_UTILS_H
#define PUZZLE_UTILS_H

#include <vector>

const int N = 9;
const int MAX_STATES = 400000;

extern int fact[N];
extern std::vector<std::vector<int>> goal;

void init_factorial();
int encode(const std::vector<std::vector<int>>& grid);
std::vector<std::vector<int>> decode(int code);
void print_board(const std::vector<std::vector<int>>& board);
std::vector<int> get_neighbours(int state);

#endif