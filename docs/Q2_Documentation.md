# Question 2 – Expression Evaluator System Documentation

---

# 1. Overview

This program is a **mathematical expression interpreter** that reads expressions from a file, parses them into an abstract syntax tree (AST), evaluates them, and outputs structured results.

It supports:

- arithmetic operations
- operator precedence
- parentheses
- unary negation
- implicit multiplication

---

# 2. What the Program Represents

This system represents a simplified **compiler/interpreter pipeline**, consisting of:

### 1. Lexical Analysis (Tokenizer)

Breaks input into tokens

### 2. Syntax Analysis (Parser)

Builds an expression tree

### 3. Evaluation Engine

Computes final result from the tree

---

👉 Conceptually, it represents:

> A miniature mathematical interpreter similar to a programming language engine.

---

# 3. Core Idea

The program converts a string expression into a structured tree:

Example:
