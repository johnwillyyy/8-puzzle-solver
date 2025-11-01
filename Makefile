CXX = g++
TARGET = puzzle_solver
TARGET_JSON = puzzle_solver_json

all: $(TARGET) $(TARGET_JSON)

$(TARGET): main.cpp bfs.cpp dfs.cpp puzzle_utils.cpp a_star.cpp iddfs.cpp
	$(CXX) -o $(TARGET) main.cpp bfs.cpp dfs.cpp puzzle_utils.cpp a_star.cpp iddfs.cpp

$(TARGET_JSON): main_json.cpp bfs.cpp dfs.cpp puzzle_utils.cpp a_star.cpp iddfs.cpp
	$(CXX) -o $(TARGET_JSON) main_json.cpp bfs.cpp dfs.cpp puzzle_utils.cpp a_star.cpp iddfs.cpp

clean:
	rm -f $(TARGET) $(TARGET_JSON)