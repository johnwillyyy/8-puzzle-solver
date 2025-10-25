CXX = g++
TARGET = puzzle_solver

$(TARGET): main.cpp bfs.cpp dfs.cpp puzzle_utils.cpp
	$(CXX) -o $(TARGET) main.cpp bfs.cpp dfs.cpp puzzle_utils.cpp

clean:
	rm -f $(TARGET)