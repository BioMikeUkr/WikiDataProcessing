#include <iostream>
#include <fstream>
#include <regex>
#include <unordered_map>

int main(int argc, char* argv[]) {
    std::regex pattern(R"(Q\d+)");
    std::string line;
    std::ifstream file(argv[1]);

    if (!file.is_open()) {
        std::cerr << "Error opening file!" << std::endl;
        return 1;
    }

    std::ofstream outFile(argv[2]);
    if (!outFile.is_open()) {
        std::cerr << "Error opening output file!" << std::endl;
        return 1;
    }

    int idx = 0;
    bool first_entry = true;
    outFile << "{\n";

    while (std::getline(file, line)) {
        std::smatch match;
        if (std::regex_search(line, match, pattern)) {
            if (!first_entry) {
                outFile << ",\n";
            }
            first_entry = false;

            outFile << "  \"" << match.str() << "\": " << idx;
        }
        idx++;
    }
    outFile << "\n}\n";

    file.close();
    outFile.close();
    std::cout << "Process completed successfully!" << std::endl;

    return 0;
}
