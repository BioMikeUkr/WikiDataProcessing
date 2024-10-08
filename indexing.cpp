#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdint>
#include <limits>

std::vector<int64_t> buildLineIndex(const std::string& filePath) {
    std::vector<int64_t> lineOffsets;
    std::ifstream file(filePath, std::ios::binary);

    if (!file.is_open()) {
        std::cerr << "Error opening file: " << filePath << std::endl;
        return lineOffsets;
    }

    while (file) {
        int64_t offset = static_cast<int64_t>(file.tellg());
        if (offset == -1) {
            break;
        }
        lineOffsets.push_back(offset);

        file.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        if (file.eof()) {
            break;
        }
    }

    return lineOffsets;
}

void saveOffsets(const std::vector<int64_t>& lineOffsets, const std::string& fileName) {
    std::ofstream offsetsFile(fileName, std::ios::binary);

    for (const auto& offset : lineOffsets) {
        offsetsFile.write(reinterpret_cast<const char*>(&offset), sizeof(offset));
    }
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <input file> <index file>" << std::endl;
        return 1;
    }

    std::string filePath = argv[1];
    std::string indexFilePath = argv[2];

    std::vector<int64_t> lineIndex = buildLineIndex(filePath);

    if (lineIndex.empty()) {
        std::cerr << "Failed to create line index." << std::endl;
        return 1;
    }

    saveOffsets(lineIndex, indexFilePath);

    std::cout << "Line index saved to file: " << indexFilePath << std::endl;
    return 0;
}
