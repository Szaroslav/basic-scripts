# 1.2 A first look at input/output

## Exercise 1.4

> Our program used the addition operator, `+`, to add two numbers. Write a program that uses the multiplication operator, `*`, to print the product instead.

`main.cpp`
```cpp
#include <iostream>

int main() {
    std::cout << "Enter two numbers:" << std::endl;
    int a = 0, b = 0;
    std::cin >> a >> b;

    std::cout << "The multiplication of " << a << " and " << b
              << " is " << a * b << std::endl;
    
    return 0;
}
```