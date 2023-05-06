# Section 1.1.1 _Compiling and executing our program_

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
