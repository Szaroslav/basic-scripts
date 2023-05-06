#include <iostream>

int main() {
    std::cout << "/*";                  // correct
    std::cout << "*/";                  // correct
    std::cout << /* "*/" */;            // incorrect
    std::cout << /* "*/" /* "/*" */;    // correct

    return 0;
}