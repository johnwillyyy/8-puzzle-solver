CXX = g++
TARGET = puzzle_solver

$(TARGET): main.cpp bfs.cpp dfs.cpp puzzle_utils.cpp a_star.cpp
	$(CXX) -o $(TARGET) main.cpp bfs.cpp dfs.cpp puzzle_utils.cpp a_star.cpp

clean:
	rm -f $(TARGET)