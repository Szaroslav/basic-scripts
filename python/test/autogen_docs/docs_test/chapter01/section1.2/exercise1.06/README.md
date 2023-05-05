# 1.2 A first look at input/output

## Exercise 1.6

> Explain whether the following program fragment is legal.
> ```cpp
> std::cout << "The sum of " << v1;
>           << " and " << v2;
>           << " is " << v1 + v2 << std::endl;
> ```
> If the program is legal, what does it do? If the program is not legal, why not? How would you fix it?

Above fragment of code it's not legal, the program won't compile. This behaviour is caused by 2 last statements, which don't have `std::cout` as the left operand. In this directory is `main.cpp`, which can be open in IDE or text editor, or be compiled to see errors.