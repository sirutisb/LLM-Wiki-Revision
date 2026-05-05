---
title: "Week 5 Summary: Floating Point Arithmetic"
tags: [hpc, week-5, summary]
date: 2026-05-05
---

# Week 5 Summary: Floating Point Arithmetic

This week focuses on the representation of non-integer values using floating-point numbers in computing, specifically adhering to the IEEE 754 standard.

## Key Concepts Covered
*   **Floating Point Representation:** Understanding base, precision, significand (mantissa), and exponent.
*   **IEEE 754 Standard:** The standard for floating-point arithmetic, particularly focusing on single (32-bit) and double (64-bit) precision. Double precision is standard for scientific computing.
*   **Range and Accuracy:** Double precision has a range from roughly $10^{-308}$ to $10^{308}$. Its finite accuracy introduces a round-off error, quantified by the machine epsilon ($\approx 10^{-16}$).
*   **Floating Point Exceptions:** Understanding scenarios that cause issues, like Overflow, Underflow, Divide by zero, Invalid operations, and Inexact results.
*   **Exceptional Values:** How systems represent $\infty$, $-\infty$, NaN (Not a Number), and subnormal numbers (which allow for gradual underflow).
*   **Peak Performance ($R_{peak}$):** Calculating the theoretical maximum performance of a compute node or cluster based on clock frequency, core counts, and operations per cycle.