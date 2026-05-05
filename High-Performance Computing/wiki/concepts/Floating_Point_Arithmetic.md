---
title: "Floating Point Arithmetic"
tags: [hpc, week-5, hardware, architecture]
date: 2026-05-05
---

# Floating Point Arithmetic

Because non-integer solutions are necessary for most scientific applications (like solving PDEs), high-performance computing heavily relies on floating-point representations of numbers.

## Representation Basics
A floating-point number is represented mathematically as:
$$ d.dddd \times \beta^e $$
*   **$d.dddd$**: The significand (or mantissa), which has $p$ digits.
*   **$\beta$**: The base.
*   **$e$**: The exponent.
*   **$p$**: The precision.

## IEEE 754 Standard
The IEEE 754 standard is the most widely adopted standard for floating-point arithmetic.
*   **Single Precision (float)**: 32-bit representation.
*   **Double Precision (double)**: 64-bit representation. This is the standard for scientific and engineering calculations.

### Double Precision Anatomy
A 64-bit double precision number consists of:
*   **1 bit** for the sign ($\pm$).
*   **11 bits** for the exponent.
*   **52 bits** for the mantissa.

A "normalised" double-precision floating-point number $x$ is represented as:
$$ x = \pm (1.b_1b_2...b_{52})_2 \times 2^{(a_1a_2...a_{11})_2 - 1023} $$

### Range and Accuracy
*   **Range**: For double precision, the representable range is roughly $10^{-308}$ to $10^{308}$.
*   **Machine Epsilon**: The difference between 1.0 and the next largest representable number. For double precision, this is $2^{-52} \approx 10^{-16}$.
*   **Round-off Error**: Because floating-point numbers have finite accuracy, numerical operations introduce round-off errors. If the numerical method's error is smaller than the round-off error, the solution is at "machine precision".

## Floating Point Exceptions
IEEE 754 specifies 5 floating-point exceptions:
1.  **Overflow**: Result is too large to be represented. Returns `inf` or `-inf`.
2.  **Underflow**: Result is too close to zero. Returns `0` or a **subnormal number** (exponent bits are all zero, which expands the range around zero and allows for gradual underflow but loses precision).
3.  **Divide by zero**: E.g., `1.0 / 0.0`. Returns `inf` or `-inf`.
4.  **Invalid**: E.g., `0.0 / 0.0` or $\sqrt{-1}$. Returns `NaN` (Not a Number).
5.  **Inexact**: Mathematically inexact; returns a rounded result.