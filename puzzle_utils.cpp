#include "puzzle_utils.h"
#include <vector>
#include <numeric>
#include <iostream>
#include <string>

// ANSI color codes
#define RESET   "\033[0m"
#define BG_BLUE "\033[44m"
#define BG_WHITE "\033[47m"
#define BG_GRAY "\033[100m"
#define TEXT_WHITE "\033[37m"
#define TEXT_BLACK "\033[30m"

int fact[N];
std::vector<std::vector<int>> goal = {
    {0, 1, 2},
    {3, 4, 5},
    {6, 7, 8}
};

void init_factorial() {
    fact[0] = 1;
    for (int i = 1; i < N; i++) 
        fact[i] = fact[i - 1] * i;
}

int encode(const std::vector<std::vector<int>>& grid) {
    std::vector<int> flat;
    for (auto& row : grid)
        for (auto x : row)
            flat.push_back(x);
    
    int code = 0;
    for (int i = 0; i < N; i++) {
        int smaller = 0;
        for (int j = i + 1; j < N; j++)
            if (flat[j] < flat[i]) smaller++;
        code += smaller * fact[N - i - 1];
    }
    return code;
}

std::vector<std::vector<int>> decode(int code) {
    std::vector<int> flat(N);
    std::vector<int> available(N);
    std::iota(available.begin(), available.end(), 0);

    for (int i = 0; i < N; i++) {
        int idx = code / fact[N - i - 1];
        code %= fact[N - i - 1];
        flat[i] = available[idx];
        available.erase(available.begin() + idx);
    }

    std::vector<std::vector<int>> grid(3, std::vector<int>(3));
    for (int i = 0; i < 9; i++)
        grid[i / 3][i % 3] = flat[i];
    return grid;
}

void print_board(const std::vector<std::vector<int>>& board) {
    int cell_width = 7;  // Width of each cell
    int cell_height = 3; // Height of each cell
    
    // Top border (blue background with spaces)
    std::cout << "|";
    std::cout << BG_BLUE << TEXT_WHITE;
    for (int i = 0; i < 3 * cell_width + 8; i++) {
        std::cout << " ";
    }
    std::cout << RESET;
    std::cout << "|";
    std::cout << "\n";
    for (int row = 0; row < 3; row++) {
        // Multiple lines for each row to make cells taller
        for (int line = 0; line < cell_height; line++) {
            std::cout << "|";
            std::cout << BG_BLUE << "  " << RESET; // Left border
            
            for (int col = 0; col < 3; col++) {
                // Choose cell background color
                if (board[row][col] == 0) {
                    std::cout << BG_GRAY << TEXT_WHITE;
                } else {
                    std::cout << BG_WHITE << TEXT_BLACK;
                }
                
                // Fill cell with spaces or number
                for (int i = 0; i < cell_width; i++) {
                    // Center the number in the middle line
                    if (line == cell_height / 2 && i == cell_width / 2 - 1) {
                        if (board[row][col] != 0) {
                            std::cout <<' '<< board[row][col];
                            i++; // Skip one space since we printed a digit
                        } else {
                            std::cout << " ";
                        }
                    } else {
                        std::cout << " ";
                    }
                }
                
                std::cout << RESET;
                
                // Right border or cell separator
                if (col < 2) {
                    std::cout << BG_BLUE << "  " << RESET;
                }
            }
            
            // Right border for the last cell
            std::cout << BG_BLUE << "  " << RESET;
            std::cout << "|";
            std::cout << "\n";
        }
        
        // Row separator (blue background)
        if (row < 2) {
            std::cout << "|";
            std::cout << BG_BLUE;
            for (int i = 0; i < 3 * cell_width + 8; i++) {
                std::cout << " ";
            }
            std::cout << RESET;
            std::cout << "|";
            std::cout << "\n";
        }
    }
    
    // Bottom border (blue background with spaces)
    std::cout << "|";
    std::cout << BG_BLUE;
    for (int i = 0; i < 3 * cell_width + 8; i++) {
        std::cout << " ";
    }
    std::cout << RESET;
    std::cout << "|";
    std::cout << "\n";
}


std::vector<int> get_neighbours(int state) {
    std::vector<int> neighbours;
    std::vector<std::vector<int>> board = decode(state);

    int dx[] = {1, -1, 0, 0};
    int dy[] = {0, 0, -1, 1};

    int x, y;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == 0) {
                x = i;
                y = j;
            }
        }
    }

    for (int k = 0; k < 4; k++) {
        int nx = x + dx[k];
        int ny = y + dy[k];
        if (nx >= 0 && nx < 3 && ny >= 0 && ny < 3) {
            std::swap(board[nx][ny], board[x][y]);
            neighbours.push_back(encode(board));
            std::swap(board[x][y], board[nx][ny]);
        }
    }

    return neighbours;
}