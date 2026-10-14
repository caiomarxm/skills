# Coding style

Apply these standards to code changed by the task.

- CRITICAL: Keep it simple. Do not build speculative needs (KISS and YAGNI).
- Optimize for readability. Code is written once and read many times.
- Good code should rhyme, and read like poetry. Make sure code with similar
  branches is consistent and follow the same patterns. Use newlines to group
  logical blocks of code together.
- Prefer functional code with strong types where the language and codebase
  support it.
- Try your best to keep only one level of nesting by using patterns like checks
  with early returns, module private functions with clear responsibilities, etc.
- In Python, prefer Pydantic for typed data models and list comprehensions over
  `map` or `reduce`. Use an explicit for loop whenever it will ease understanding.
- Prefer modular code with clear ownership and encapsulation. Aim for deep modules
  with clear interface, avoiding multiple shallow modules.
- Avoid unnecessary abstractions and complexity.
