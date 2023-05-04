# 1.1.1 Compiling and executing our program

## Exercise 1.1
> Review the documentation for your compiler and determine what file naming convention it uses. Compile and run the `main` program from page 2.

I'm going to use the [GNU Compiler Collection](https://gcc.gnu.org/). Filenames will be named in `snake_case` convetion, e.g. `my_main.cpp` Here is a [GCC coding convetions reference](https://gcc.gnu.org/codingconventions.html).

`main.cpp`
```cpp
int main()
{
return 0;
}
```
## Exercise 1.2
> Change the program to return `-1`. A return value of `-1` is often treated as an indicator that the program failed. Recompile and rerun your program to see how your system treats a failure indicator from `main`.

`main.cpp`
```cpp
int main()
{
return 0;
}
```
# 1.2 A first look at input/output

## Exercise 1.3

> Write a program to print `Hello, World` on the standard output.

`main.cpp`
```cpp
#include <iostream>

int main() {
std::cout << "Hello, World" << std::endl;

return 0;
}
```
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
<< " is " << a autogen_docs.sh output.md src test b << std::endl;

return 0;
}
```
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
std::cout << a autogen_docs.sh output.md src test b;
std::cout << std::endl;

return 0;
}
```
## Exercise 1.6

> Explain whether the following program fragment is legal.
> ```cpp
> std::cout << "The sum of " << v1;
> << " and " << v2;
> << " is " << v1 + v2 << std::endl;
> ```
> If the program is legal, what does it do? If the program is not legal, why not? How would you fix it?

