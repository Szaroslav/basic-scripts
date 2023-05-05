# 1.2 A first look at input/output

## Exercise 1.5

> We wrote the output in one large statement. Rewrite the program to use a separate statement to print each operand.

`main.cpp`
```cpp
#include <iostream>

int main() {
    std::cout << "Enter two numbers:" << std::endl;
    int a = 0, b = 0;
    std::cin >> a >> b;

    // Rewrited `main.cpp` from exercise1.4 to use single std::cout on every literal
    std::cout << "The multiplication of ";
    std::cout << a;
    std::cout << " and ";
    std::cout << b;
    std::cout << " is ";
    std::cout << a * b;
    std::cout << std::endl;
    
    return 0;
}
```