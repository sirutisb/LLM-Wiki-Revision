---
title: "Week 5 Practice Questions: Floating Point Arithmetic"
tags: [hpc, week-5, floating-point, practice]
date: 2026-05-14
---

# Week 5 Practice Questions: Floating Point Arithmetic

> **Coverage:** IEEE 754 single and double precision, special values, machine epsilon, rounding, catastrophic cancellation, non-associativity, and peak FLOP/s calculations.
> **Source pages:** [Floating Point Arithmetic](../wiki/concepts/Floating_Point_Arithmetic.md), [Week 5 Summary](../wiki/summaries/Week_5_Summary.md), [Performance Metrics](../wiki/concepts/Performance_Metrics_and_Top500.md)

---

## Section A: Short Answer / Definitions

### Q1
**Define "machine epsilon" for a floating-point format. State its value for IEEE 754 double precision and explain its physical significance.**

<details>
<summary>Model Answer</summary>

Machine epsilon (eps) is the difference between 1.0 and the next largest representable floating-point number.

For IEEE 754 double precision: eps = 2^{-52} ≈ 2.22 × 10^{-16}.

Physical significance: any real number x is stored with a relative rounding error of at most eps/2. Equivalently, if two numbers differ by less than eps, the format cannot distinguish them from 1.0. It quantifies the resolution of the representation — roughly 15–16 significant decimal digits.

**Marking points (3 marks):**
- Correct definition referencing 1.0 and the next representable number [1]
- Correct value 2^{-52} or 10^{-16} [1]
- Explanation linking eps to maximum relative rounding error or number of significant digits [1]

</details>

---

### Q2
**State the bit-field layout of an IEEE 754 single-precision (32-bit) floating-point number. For each field, give its width in bits and its role.**

<details>
<summary>Model Answer</summary>

| Field    | Bits | Role |
|----------|------|------|
| Sign     | 1    | Encodes positive (0) or negative (1) |
| Exponent | 8    | Biased exponent; bias = 127. Determines magnitude. All-zeros and all-ones are reserved for special values. |
| Mantissa | 23   | Fractional part of the significand. An implicit leading 1 bit is assumed for normalised numbers, giving 24 bits of actual precision. |

Total: 1 + 8 + 23 = 32 bits.

**Marking points (3 marks):** correct widths for all three fields [1], correct role for exponent including bias value 127 [1], mention of implicit leading 1 bit for normalised numbers [1].

</details>

---

### Q3
**State the bit-field layout of an IEEE 754 double-precision (64-bit) floating-point number. For each field give its width in bits.**

<details>
<summary>Model Answer</summary>

| Field    | Bits |
|----------|------|
| Sign     | 1    |
| Exponent | 11   |
| Mantissa | 52   |

Total: 1 + 11 + 52 = 64 bits. The exponent bias is 1023.

**Marking points (2 marks):** all three widths correct [1], bias value 1023 stated [1].

</details>

---

### Q4
**Name all five floating-point exceptions defined by IEEE 754 and state the return value for each.**

<details>
<summary>Model Answer</summary>

| Exception  | Trigger example              | Return value              |
|------------|------------------------------|---------------------------|
| Overflow   | Result too large for format  | +inf or -inf              |
| Underflow  | Result too close to zero     | 0 or a subnormal number   |
| Divide by zero | 1.0 / 0.0               | +inf or -inf              |
| Invalid    | 0.0 / 0.0 or sqrt(-1.0)     | NaN (Not a Number)        |
| Inexact    | Mathematically unrepresentable result | Rounded result  |

**Marking points (5 marks):** 1 mark per correctly named and matched exception/return pair. Partial credit for correct exception name without return value (0.5 each).

</details>

---

### Q5
**What is a subnormal (denormalised) floating-point number? How does it differ from a normal floating-point number, and why is it useful?**

<details>
<summary>Model Answer</summary>

A subnormal number is a non-zero floating-point number whose exponent field is all zeros. Unlike normal numbers (which have an implicit leading 1 in the significand), subnormal numbers have an implicit leading 0:

- Normal:   x = ±(1.b1b2...b52)_2 × 2^(exponent - 1023)
- Subnormal: x = ±(0.b1b2...b52)_2 × 2^(-1022)

The exponent is fixed at -1022 regardless of the exponent field bits. This means the leading bits of the mantissa may be zero — precision is lost progressively as the number approaches zero.

Usefulness: subnormal numbers allow gradual underflow. Without them, a computation result that falls below the smallest normalised value would immediately underflow to zero (abrupt underflow). Subnormals provide a smooth, gradual transition, which can help reveal that underflow is occurring rather than silently producing zero.

**Marking points (3 marks):** implicit leading 0 vs 1 [1], correct fixed exponent -1022 [1], gradual underflow explanation [1].

</details>

---

### Q6
**What bit patterns encode +infinity, -infinity, and NaN in IEEE 754 double precision?**

<details>
<summary>Model Answer</summary>

- **+infinity:** sign = 0, exponent = all ones (11111111111), mantissa = all zeros.
- **-infinity:** sign = 1, exponent = all ones (11111111111), mantissa = all zeros.
- **NaN:** exponent = all ones (11111111111), mantissa = NOT all zeros (at least one mantissa bit is 1). Sign bit is irrelevant.

These patterns are "reserved" — they signal exceptional states rather than representing a finite number.

**Marking points (3 marks):** 1 mark each for correct description of +inf, -inf, and NaN bit patterns.

</details>

---

### Q7
**True or False (with justification): "Floating-point addition is associative, i.e., (a + b) + c = a + (b + c) always holds."**

<details>
<summary>Model Answer</summary>

**False.**

Floating-point addition is NOT associative because each operation independently rounds to the nearest representable value. The order of operations can change which intermediate results are rounded and by how much.

Concrete example: let a = 1.0, b = 1e16, c = -1e16 (all in double precision).

- (a + b) + c = (1.0 + 1e16) + (-1e16)
  - 1.0 + 1e16 ≈ 1e16 (the 1.0 is lost to rounding — 1 is below machine epsilon relative to 1e16)
  - 1e16 + (-1e16) = 0.0  ← WRONG answer
- a + (b + c) = 1.0 + (1e16 + (-1e16))
  - 1e16 + (-1e16) = 0.0
  - 1.0 + 0.0 = 1.0  ← CORRECT answer

This is also an example of catastrophic cancellation of a + b, which destroys the contribution of a.

**Marking points (3 marks):** correct "False" [1], valid explanation citing rounding [1], concrete numerical or algebraic example [1].

</details>

---

### Q8
**True or False (with justification): "The IEEE 754 standard only specifies the bit layout for single and double precision; it says nothing about arithmetic operations."**

<details>
<summary>Model Answer</summary>

**False.**

IEEE 754 specifies both the number representations AND the required behaviour of the five basic arithmetic operations: addition, subtraction, multiplication, division, and square root. For each operation it mandates that the result must be the same as if computed with infinite precision and then rounded to the nearest representable value according to the current rounding mode. This is called the "correctly rounded result" requirement.

**Marking points (2 marks):** correct "False" [1], correct statement about arithmetic operations being specified [1].

</details>

---

## Section B: IEEE 754 Representation (Bit-Level Calculations)

### Q9
**Convert the decimal number 13.5 to IEEE 754 single-precision binary representation. Show all working and give your answer as a 32-bit binary string.**

<details>
<summary>Model Answer</summary>

**Step 1 — Convert 13.5 to binary.**
- Integer part: 13 = 1101 in binary
- Fractional part: 0.5 = 0.1 in binary
- So 13.5 = 1101.1 in binary

**Step 2 — Normalise.**
- 1101.1 = 1.1011 × 2^3
- Sign = 0 (positive)
- Exponent = 3
- Significand (mantissa fractional part) = 1011 followed by 19 zeros

**Step 3 — Encode the biased exponent.**
- Bias for single precision = 127
- Biased exponent = 3 + 127 = 130
- 130 in binary: 128 + 2 = 10000010

**Step 4 — Assemble the 32-bit word.**
```
Sign | Exponent (8 bits) | Mantissa (23 bits)
  0  |  10000010         | 10110000000000000000000
```

Full 32-bit string: `0 10000010 10110000000000000000000`

Or compactly: `01000001010110000000000000000000`

**Marking points (4 marks):** correct binary of 13.5 [1], correct normalisation / exponent = 3 [1], correct biased exponent = 130 = 10000010 [1], correct final 32-bit layout [1].

</details>

---

### Q10
**The following 32-bit pattern is an IEEE 754 single-precision floating-point number:**

```
0 01111100 01000000000000000000000
```

**Decode it to a decimal value. Show all working.**

<details>
<summary>Model Answer</summary>

**Step 1 — Extract fields.**
- Sign bit: 0 → positive
- Exponent bits: 01111100
- Mantissa bits: 01000000000000000000000

**Step 2 — Compute the unbiased exponent.**
- Exponent field = 01111100 in binary
  = 64 + 32 + 16 + 8 + 4 = 124 (in decimal)
- Unbiased exponent = 124 - 127 = -3

**Step 3 — Construct the value.**
- Value = +(1.01000000...)_2 × 2^{-3}
- The significand = 1 + 2^{-2} = 1.25 (the second mantissa bit is 1; place value = 2^{-2} = 0.25)
- Value = 1.25 × 2^{-3} = 1.25 / 8 = **0.15625**

**Verification:** 0.15625 = 5/32 = 5 × 2^{-5}. And 1.25 × 2^{-3} = (5/4) × (1/8) = 5/32. Correct.

**Marking points (4 marks):** correct field extraction [1], correct biased exponent → unbiased = -3 [1], correct significand = 1.25 [1], correct final value 0.15625 [1].

</details>

---

### Q11
**Convert -0.375 to IEEE 754 single-precision binary. Give the answer as hex.**

<details>
<summary>Model Answer</summary>

**Step 1 — Convert 0.375 to binary.**
- 0.375 = 0.011 in binary (0 + 0 + 2^{-3} does not work; 0.25 + 0.125 = 0.375, so 0.011)

**Step 2 — Normalise.**
- 0.011 = 1.1 × 2^{-2}
- Sign = 1 (negative)
- Exponent = -2, biased = -2 + 127 = 125 = 01111101
- Mantissa = 10000000000000000000000 (only the first bit after the decimal is 1)

**Step 3 — Assemble.**
```
Sign | Exponent  | Mantissa
  1  | 01111101  | 10000000000000000000000
```
Binary: `1 01111101 10000000000000000000000`

**Step 4 — Convert to hex.**
Group into 4-bit nibbles:
`1011 1110 1100 0000 0000 0000 0000 0000`
= BEC00000 in hex

**Answer: 0xBEC00000**

**Marking points (4 marks):** correct binary 0.011 [1], correct normalisation exponent -2 / biased 125 [1], correct sign+mantissa layout [1], correct hex BEC00000 [1].

</details>

---

### Q12
**What decimal value does the IEEE 754 double-precision bit pattern with all 52 mantissa bits equal to 1, exponent bits = 01111111111, and sign bit = 0 represent? (Hint: this is the largest number less than 2.0.)**

<details>
<summary>Model Answer</summary>

**Fields:**
- Sign = 0 → positive
- Exponent field = 01111111111 = 1023 (decimal) → unbiased exponent = 1023 - 1023 = 0
- Mantissa = 1111...1 (52 ones)

**Significand:**
- (1.1111...1)_2 with 52 fractional bits
- = 1 + sum_{i=1}^{52} 2^{-i}
- = 1 + (1 - 2^{-52})   [geometric series: sum of 2^{-i} for i=1..52 = 1 - 2^{-52}]
- = 2 - 2^{-52}

**Value:** (2 - 2^{-52}) × 2^0 = 2 - 2^{-52} ≈ 1.9999999999999998

This is the largest representable double-precision number less than 2.0. Adding eps = 2^{-52} to 1.0 gives the next number after 1.0; here the exponent is 0 so the gap just below 2.0 is 2^{0} × 2^{-52} = 2^{-52}.

**Marking points (3 marks):** correct exponent decoding → unbiased 0 [1], correct significand = 2 - 2^{-52} [1], correct final value stated [1].

</details>

---

## Section C: Range and Precision Calculations

### Q13
**Calculate the machine epsilon for IEEE 754 single precision. Express your answer as a power of 2 and as an approximate decimal.**

<details>
<summary>Model Answer</summary>

Single precision has 23 mantissa bits. The implicit leading 1 is followed by 23 fractional bits, so the least significant bit of the mantissa has place value 2^{-23}.

Machine epsilon = 2^{-23} ≈ 1.19 × 10^{-7}

This means single precision provides approximately 7 significant decimal digits of precision.

**Marking points (2 marks):** correct value 2^{-23} [1], correct decimal approximation and/or statement of ~7 significant digits [1].

</details>

---

### Q14
**Derive the smallest (most negative) exponent for a normalised IEEE 754 double-precision number, and hence confirm that the minimum representable magnitude is approximately 10^{-308}.**

<details>
<summary>Model Answer</summary>

**Step 1 — Find the minimum exponent field value for a normalised number.**
The exponent field has 11 bits. The reserved values are:
- All zeros (00000000000) → subnormal or zero
- All ones  (11111111111) → infinity or NaN

So the smallest valid exponent field for a normalised number is 00000000001 = 1 (decimal).

**Step 2 — Convert to unbiased exponent.**
Bias = 1023.
Minimum unbiased exponent = 1 - 1023 = -1022.

**Step 3 — Minimum normalised magnitude.**
The smallest normalised value has all mantissa bits = 0, so significand = 1.0.
Minimum value = 1.0 × 2^{-1022}

**Step 4 — Convert to decimal.**
2^{-1022} = 2^{-1022}
log10(2^{-1022}) = -1022 × log10(2) ≈ -1022 × 0.30103 ≈ -307.65
So 2^{-1022} ≈ 10^{-307.65} ≈ 2.2 × 10^{-308}

This confirms the quoted range minimum of ~10^{-308}.

**Marking points (4 marks):** identifying reserved exponent values [1], minimum unbiased exponent -1022 [1], minimum normalised value = 1.0 × 2^{-1022} [1], correct decimal approximation ~2 × 10^{-308} [1].

</details>

---

### Q15
**Confirm that the maximum representable IEEE 754 double-precision normalised number is approximately 10^{308}. Show your working.**

<details>
<summary>Model Answer</summary>

**Maximum exponent field value (normalised):** 11111111110 = 2046 (all ones except the last bit — the all-ones pattern is reserved).
Maximum unbiased exponent = 2046 - 1023 = 1023.

**Maximum significand:** all 52 mantissa bits = 1 → significand = (1.111...1)_2 = 2 - 2^{-52} ≈ 2.

**Maximum value:**
x_max = (2 - 2^{-52}) × 2^{1023} ≈ 2 × 2^{1023} = 2^{1024}

log10(2^{1024}) = 1024 × 0.30103 ≈ 308.25

So x_max ≈ 1.8 × 10^{308}, confirming the quoted range maximum of ~10^{308}.

**Marking points (3 marks):** correct maximum biased exponent 2046 → unbiased 1023 [1], correct maximum significand ≈ 2 [1], correct log10 calculation giving ~308 [1].

</details>

---

### Q16
**A computation produces the result 1.234567890123456789. After storing in a double-precision variable, how many significant decimal digits are preserved? Justify your answer in terms of machine epsilon.**

<details>
<summary>Model Answer</summary>

Double precision machine epsilon = 2^{-52} ≈ 2.22 × 10^{-16}.

The maximum relative rounding error on storing any real number x is eps/2 ≈ 1.11 × 10^{-16}.

The number has magnitude ~1.23, so the absolute rounding error is at most:
|absolute error| ≤ 1.23 × 1.11 × 10^{-16} ≈ 1.37 × 10^{-16}

Since the number has 18 digits written and the error enters at the 16th decimal place, the stored value preserves approximately **15–16 significant decimal digits**.

The stored value would be approximately 1.2345678901234568 (the last few digits differ from the true mathematical value).

**Marking points (3 marks):** correct eps value and use [1], correct relative-to-absolute error reasoning [1], correct conclusion of 15–16 significant digits [1].

</details>

---

## Section D: Peak Performance Calculations

### Q17
**A compute node has 2 sockets, each containing a processor with 12 cores running at a base clock frequency of 3.2 GHz. Each core supports AVX-512 with FMA, giving 16 double-precision FLOP/s per cycle. Calculate the peak performance of:**
**(a)** one compute node in GFLOP/s
**(b)** a cluster of 256 such nodes in TFLOP/s

<details>
<summary>Model Answer</summary>

Using: R_peak = N_sockets × N_cores/socket × R_clock × N_ops/cycle

**(a) Single node:**
R_peak = 2 × 12 × 3.2 GHz × 16
= 2 × 12 × 3.2 × 16 GFLOP/s
= 2 × 12 = 24
24 × 3.2 = 76.8
76.8 × 16 = **1228.8 GFLOP/s**

**(b) 256-node cluster:**
R_peak_cluster = 256 × 1228.8 GFLOP/s
= 314,572.8 GFLOP/s
= **314.6 TFLOP/s** (≈ 0.315 PFLOP/s)

**Marking points (4 marks):** correct formula stated or implied [1], correct node calculation 1228.8 GFLOP/s [2], correct cluster calculation 314.6 TFLOP/s [1].

</details>

---

### Q18
**The Zen cluster at the University of Exeter had 182 compute nodes, each with 2 Intel Xeon X5560 sockets. Each socket has 6 cores running at 2.8 GHz. The X5560 supports SSE4.2, delivering 4 double-precision FLOP/s per cycle.**

**(a)** Calculate the peak performance of a single compute node in GFLOP/s.
**(b)** Calculate the total cluster peak performance in GFLOP/s and TFLOP/s.
**(c)** Explain why the actual measured performance (R_max from HPL benchmark) is always less than R_peak.

<details>
<summary>Model Answer</summary>

**(a) Single node:**
R_peak = N_sockets × N_cores/socket × R_clock × N_ops/cycle
= 2 × 6 × 2.8 GHz × 4
= 12 × 2.8 × 4
= 12 × 11.2
= **134.4 GFLOP/s**

**(b) Cluster:**
R_peak_cluster = 182 × 134.4 GFLOP/s
= 24,460.8 GFLOP/s
= **24.46 TFLOP/s** (≈ 24.5 TFLOP/s)

**(c) R_max < R_peak because:**
- R_peak assumes all floating-point units are executing a FLOP every cycle with no stalls. In practice, memory latency causes the processor to stall waiting for data (most real codes are memory-bound, not compute-bound).
- Not all instructions are floating-point (integer ops, branches, load/store instructions consume cycles without contributing FLOP/s).
- Communication overhead between MPI processes (network latency and bandwidth) reduces the fraction of time spent computing.
- Load imbalance means some cores finish early and sit idle waiting at barriers.
- Vector units may not be fully utilised if data alignment or problem structure prevents vectorisation.

**Marking points (6 marks):** (a) correct 134.4 GFLOP/s [2]; (b) correct 24,460.8 GFLOP/s / 24.5 TFLOP/s [2]; (c) at least two valid reasons [1 each, max 2].

</details>

---

### Q19
**You are evaluating two processor options for a new HPC cluster:**

| Processor | Cores | Clock (GHz) | FLOP/cycle (double) |
|-----------|-------|-------------|---------------------|
| Option A  | 32    | 2.5         | 8                   |
| Option B  | 16    | 3.8         | 16                  |

**Both processors fit in a single socket. A node uses 2 sockets.**

**(a)** Calculate R_peak per node for each option.
**(b)** You have a budget for 100 nodes. Which configuration gives higher total cluster R_peak?
**(c)** Suggest one reason why Option A might still be preferred despite potentially lower peak performance.

<details>
<summary>Model Answer</summary>

**(a) R_peak per node:**

Option A: 2 × 32 × 2.5 × 8 = 2 × 32 × 20 = 2 × 640 = **1280 GFLOP/s**

Option B: 2 × 16 × 3.8 × 16 = 2 × 16 × 60.8 = 2 × 972.8 = **1945.6 GFLOP/s**

**(b) 100-node cluster:**

Option A: 100 × 1280 = 128,000 GFLOP/s = **128 TFLOP/s**
Option B: 100 × 1945.6 = 194,560 GFLOP/s = **194.6 TFLOP/s**

Option B gives higher cluster R_peak.

**(c) Possible reasons to prefer Option A (any one valid answer):**
- More cores per socket may be better for highly parallel, memory-bandwidth-limited workloads that benefit from more compute threads each touching less data.
- Lower clock speed → lower power consumption and heat per socket; better energy efficiency (FLOP/s per Watt).
- Lower clock speed may give better sustained memory bandwidth per core.
- Cheaper unit cost per socket in many procurement scenarios.
- Better suited to task-parallel or irregular workloads where IPC matters less than core count.

**Marking points (5 marks):** (a) both R_peak values correct [2]; (b) correct cluster values and correct winner (B) [2]; (c) any one well-reasoned advantage for A [1].

</details>

---

### Q20
**Fused Multiply-Add (FMA) is a key mechanism for achieving high FLOP/s.**

**(a)** What does an FMA instruction compute? Write it as a mathematical expression.
**(b)** Why does FMA count as 2 FLOP/s rather than 1?
**(c)** A core executes 2 FMA operations per cycle at 3.0 GHz. How many GFLOP/s can a single core achieve?

<details>
<summary>Model Answer</summary>

**(a)** FMA computes: result = a × b + c

It multiplies two operands and adds a third in a single instruction, with only one rounding step.

**(b)** FMA performs two arithmetic operations (one multiplication and one addition) per instruction. Even though it is issued as a single instruction, it carries out two mathematically distinct floating-point operations, so it contributes 2 to the FLOP count. Without FMA, the same result would require two separate instructions.

**(c)** Single core GFLOP/s:
= 2 FMA/cycle × 2 FLOP/FMA × 3.0 GHz
= 4 × 3.0
= **12 GFLOP/s**

(If the processor can execute 2 FMA units simultaneously using SIMD with 4-wide vectors: 2 FMA × 2 FLOP × 4 lanes × 3.0 GHz = 48 GFLOP/s — but the question specifies 2 FMA operations per cycle without specifying vector width, so 12 GFLOP/s is the expected answer.)

**Marking points (4 marks):** correct FMA formula [1], correct explanation of 2 FLOP [1], correct calculation 12 GFLOP/s [2].

</details>

---

## Section E: Explain / Describe Questions

### Q21
**Explain catastrophic cancellation in floating-point arithmetic. Give a concrete numerical example and describe a scenario in HPC where it is particularly dangerous.**

<details>
<summary>Model Answer</summary>

**Definition:** Catastrophic cancellation occurs when two nearly equal floating-point numbers are subtracted. The leading significant digits cancel (they are identical), leaving only the low-order digits in the result — but those low-order digits may already be contaminated by rounding errors from earlier computations. The relative error in the result can be orders of magnitude larger than the relative error in either operand.

**Concrete example:**
Let a = 1.23456789012345 and b = 1.23456789012340 (differing in the 14th decimal place).

Both are represented in double precision with about 15–16 correct digits. Their difference is:
a - b = 0.00000000000005 = 5 × 10^{-14}

But if the last few digits of a and b each carry a rounding error of ~10^{-16} (about eps), the absolute error in (a - b) is still ~10^{-16}, making the relative error in the difference:
relative error ≈ 10^{-16} / 5 × 10^{-14} ≈ 0.002 = 0.2%

The relative error has grown from ~10^{-16} to ~10^{-2} — a loss of 14 significant digits.

**HPC scenario — finite difference stencils:** When computing du/dx ≈ (u(x+h) - u(x)) / h with a very small step h, the numerator involves subtracting two nearly equal values. If h is too small, catastrophic cancellation dominates over the truncation error improvement, causing the approximation to degrade. This creates the well-known trade-off in selecting h: truncation error decreases with h but cancellation error increases.

Another scenario: computing variance as mean(x^2) - mean(x)^2 (the "naive" formula) when values are large and variance is small — the subtraction of two large, nearly equal numbers destroys precision.

**Marking points (4 marks):** correct definition involving subtraction of nearly equal numbers [1], correct explanation of significant digit loss [1], valid numerical example [1], relevant HPC scenario [1].

</details>

---

### Q22
**Describe three rounding modes specified by IEEE 754 and explain when each might be preferred.**

<details>
<summary>Model Answer</summary>

IEEE 754 specifies (at least) four rounding modes; the three most important are:

1. **Round to nearest, ties to even (default mode):** The result is rounded to the nearest representable value. If exactly halfway between two, round to the one with a zero least-significant bit (even). This minimises average rounding error and is the default for almost all floating-point computations. Preferred for general scientific computing because it produces the smallest expected error.

2. **Round toward zero (truncation):** The result is rounded toward zero — i.e., the fractional part is simply discarded. Equivalent to truncation. Rarely used in floating-point arithmetic proper but conceptually simple. Preferred when implementing integer conversion or when strict containment of rounding direction is needed (e.g., some interval arithmetic implementations).

3. **Round toward +infinity (ceiling):** The result is always rounded up (toward more positive values). Used in **interval arithmetic** for computing rigorous upper bounds: if you need to guarantee that computed_result >= true_result, you round up. This is critical for verified numerical algorithms.

4. (Bonus) **Round toward -infinity (floor):** The result is always rounded down. Used alongside ceiling mode in interval arithmetic to compute guaranteed lower bounds.

**Marking points (3 marks):** correct description of each of three modes (1 mark each); partial credit for correct name without use-case (0.5 each).

</details>

---

### Q23
**Why do most scientific and engineering HPC applications use double precision rather than single precision? Give two specific consequences of using single precision by mistake in a large-scale simulation.**

<details>
<summary>Model Answer</summary>

**Why double precision is the standard:**
- Double precision provides ~15–16 significant decimal digits vs ~7 for single precision.
- Round-off errors accumulate with each arithmetic operation. A long simulation with millions or billions of floating-point operations requires a very small per-step error budget — the eps ≈ 10^{-16} of double precision is typically sufficient; the eps ≈ 10^{-7} of single precision often is not.
- Physical constants and initial conditions in scientific problems often require more than 7 significant digits to be meaningfully represented.

**Two consequences of using single precision by mistake:**

1. **Accumulation of round-off error producing wrong results:** A finite-difference PDE solver running thousands of time steps may accumulate enough single-precision round-off error that the solution drifts significantly from the true answer. The simulation appears to run correctly but produces physically wrong results — a dangerous silent error.

2. **Premature underflow/overflow:** Single precision's dynamic range is ~10^{-38} to ~10^{38}. Values such as intermediate products in fluid dynamics or quantum chemistry routinely exceed 10^{38} or fall below 10^{-38}, causing overflow to inf or underflow to zero, crashing or corrupting the computation. Double precision's range of ~10^{-308} to ~10^{308} is almost always adequate.

**Marking points (4 marks):** clear reason for double-precision standard (eps / digit count) [2]; two distinct, well-explained consequences [1 each].

</details>

---

## Section F: Multi-Part Exam Questions

### Q24
**[Multi-part] IEEE 754 Double Precision**

**(a)** Write down the formula for a normalised IEEE 754 double-precision floating-point number. Define every symbol used. [3 marks]

**(b)** Using the formula from (a), determine the smallest positive normalised double-precision number. State the exponent field bits, the mantissa bits, the unbiased exponent value, and the resulting decimal approximation. [3 marks]

**(c)** The number 0.1 cannot be represented exactly in binary floating-point. Briefly explain why this is the case and what consequence this has for testing equality in a program. [2 marks]

**(d)** A student writes the following C code to check convergence:

```c
double x = 0.0;
while (x != 1.0) {
    x += 0.1;
}
```

Explain why this loop may never terminate. Suggest a correct alternative. [2 marks]

<details>
<summary>Model Answer</summary>

**(a) Normalised double-precision formula:**

x = ±(1.b1 b2 ... b52)_2 × 2^{(a1 a2 ... a11)_2 - 1023}

Symbols:
- ±: sign bit (+ if sign bit = 0, - if sign bit = 1)
- (1.b1 b2 ... b52)_2: the significand; the leading 1 is implicit (not stored); b1...b52 are the 52 stored mantissa bits
- (a1 a2 ... a11)_2: the 11-bit exponent field stored in the register
- 1023: the exponent bias; subtracting it from the stored exponent gives the true (unbiased) exponent
- Condition for normalised: exponent field is neither all zeros nor all ones

**(b) Smallest positive normalised number:**
- Exponent field bits: 00000000001 (= 1 in decimal; all-zeros is reserved for subnormals/zero)
- Mantissa bits: all 52 zeros (smallest significand = 1.000...0)
- Unbiased exponent: 1 - 1023 = -1022
- Value: 1.0 × 2^{-1022} ≈ 2.22 × 10^{-308}

**(c)** 0.1 in decimal = 1/10. Dividing by 10 in binary produces an infinite repeating binary fraction:
0.1 (decimal) = 0.0001100110011... (binary, repeating pattern 0011 forever)

Since the mantissa has only 52 bits, the representation is truncated, introducing a small but non-zero rounding error. The stored value is the closest representable number to 0.1, not exactly 0.1.

Consequence: testing `x == 0.1` or `x == 1.0` after adding approximate representations of 0.1 can fail — the accumulated value may be 0.9999999999... or 1.0000000000001... rather than exactly 1.0. Equality tests with floating-point literals are almost always incorrect.

**(d)** The loop adds approximately (but not exactly) 0.1 ten times. Due to accumulated rounding error, x after 10 additions may be something like 0.9999999999999999 or 1.0000000000000002 rather than exactly 1.0. The condition x != 1.0 remains true even after 10 additions, and the loop continues indefinitely.

**Correct alternative:** use a tolerance-based check or an integer counter:
```c
// Option 1: tolerance
double x = 0.0, target = 1.0, tol = 1e-9;
while (fabs(x - target) > tol) {
    x += 0.1;
}

// Option 2: integer loop counter (preferred)
int n = 10;
double x = 0.0;
for (int i = 0; i < n; i++) {
    x += 0.1;
}
```

**Marking points:** (a) correct formula with all symbols [3]; (b) all four items correct [3]; (c) explanation of repeating fraction + equality consequence [2]; (d) identifies accumulation error as cause [1], valid fix [1].

</details>

---

### Q25
**[Multi-part] Floating-Point Exceptions and Special Values**

**(a)** Classify each of the following C expressions according to which IEEE 754 exception it triggers and what value is returned: [4 marks]
  - (i) `1.0 / 0.0`
  - (ii) `0.0 / 0.0`
  - (iii) `sqrt(-1.0)`
  - (iv) `1e308 * 10.0`

**(b)** A subnormal number arises from the underflow exception. Write the general form of a subnormal double-precision number (its bit-pattern interpretation formula). How does it differ from the normalised form? [2 marks]

**(c)** A colleague's climate model starts producing NaN values after 500 time steps. List three plausible causes and one debugging strategy. [3 marks]

<details>
<summary>Model Answer</summary>

**(a) Classification:**

| Expression      | Exception    | Returned value |
|-----------------|-------------|----------------|
| (i) 1.0 / 0.0  | Divide by zero | +inf         |
| (ii) 0.0 / 0.0 | Invalid operation | NaN        |
| (iii) sqrt(-1.0)| Invalid operation | NaN        |
| (iv) 1e308 * 10.0| Overflow   | +inf           |

**(b) Subnormal form:**
x = ±(0.b1 b2 ... b52)_2 × 2^{-1022}

Difference from normalised: the leading digit of the significand is 0 (not 1), and the exponent is fixed at -1022 regardless of the exponent field bits (all of which are zero). This means the represented value is less than the smallest normalised number, but at the cost of losing leading significant bits — precision degrades gradually as numbers approach zero.

**(c) Plausible causes of NaN propagation:**

1. **Division by zero in a physical formula** — e.g., dividing by a density or temperature field that has gone to zero (perhaps due to an earlier underflow or unphysical negative value). The first inf/NaN poisons all subsequent calculations involving that cell.

2. **Sqrt or log of a negative number** — numerical instability in advection or diffusion can drive a field slightly negative. If the code then takes sqrt(concentration) or log(pressure), it produces NaN.

3. **Overflow to inf followed by 0 × inf = NaN** — an intermediate variable overflows to inf; later a calculation multiplies it by zero (e.g., in a boundary condition), producing 0 × inf = NaN by IEEE 754 rules.

**Debugging strategy:**
Enable floating-point exception trapping at the start of the program (e.g., `feenableexcept(FE_INVALID | FE_DIVBYZERO | FE_OVERFLOW)` in C on Linux). This causes the program to raise a SIGFPE signal and abort the first time an invalid operation occurs, rather than allowing NaN to silently propagate. Running under a debugger (e.g., gdb) will then show the exact line and variable responsible. Alternatively, use valgrind with --tool=exp-sgcheck or compiler sanitisers.

**Marking points:** (a) all four correctly classified [1 per row = 4]; (b) correct formula with leading 0 and fixed exponent -1022 [1], correct comparison to normalised [1]; (c) three plausible causes [1 each] and one debugging strategy [1] — cap at 3 marks for this part.

</details>

---

### Q26
**[Multi-part] Non-Associativity and Rounding Errors**

**(a)** Floating-point addition is not associative. Explain the mathematical reason for this. [2 marks]

**(b)** Consider the following three double-precision values: a = 1.0, b = 1.0e15, c = -1.0e15. Calculate (a + b) + c and a + (b + c) in double precision. Show why the results differ, referencing machine epsilon. [3 marks]

**(c)** In a parallel MPI reduction (e.g., MPI_Reduce with MPI_SUM), the order in which partial sums are combined depends on the number of processes and the reduction tree. Explain the implication of non-associativity for the reproducibility of parallel floating-point reductions. [2 marks]

**(d)** Suggest one algorithmic technique to reduce the impact of floating-point rounding errors when summing a large array of floating-point numbers. [1 mark]

<details>
<summary>Model Answer</summary>

**(a)** Each floating-point operation introduces an independent rounding error — the mathematical result is mapped to the nearest representable value. The accumulated rounding depends on the magnitude of the intermediate results. When the associative grouping changes, the intermediate values change, and so do the magnitudes of each rounding error. There is no algebraic identity in the finite field of floating-point numbers that guarantees (a + b) + c = a + (b + c).

**(b)** Machine epsilon for double precision: eps = 2^{-52} ≈ 2.22 × 10^{-16}.

**(a + b) + c:**
- Step 1: a + b = 1.0 + 1.0e15. The value 1.0 is smaller than eps × 1.0e15 = 2.22 × 10^{-16} × 10^{15} = 0.222. Since 1.0 > 0.222 in principle one might expect it to survive — but more precisely: 1.0 / 1.0e15 = 10^{-15}, which is much larger than eps (2.22 × 10^{-16}), so 1.0 SHOULD be representable relative to 1.0e15. In double precision: 1.0 + 1.0e15 = 1000000000000001.0 — this IS representable. So (a + b) = 1.0e15 + 1.0 ≈ 1.000000000000001 × 10^{15}.
- Step 2: (a + b) + c = (1.0e15 + 1.0) + (-1.0e15) = 1.0 ✓ (since the cancellation leaves exactly the 1.0 contribution — this works here because 1.0 is just above the eps threshold relative to 1.0e15).

**(a + (b + c)):**
- Step 1: b + c = 1.0e15 + (-1.0e15) = 0.0 (exact cancellation)
- Step 2: a + 0.0 = 1.0 ✓

Both give 1.0 here. For a stronger demonstration, use b = 1.0e16:
- 1.0 + 1.0e16: eps × 1.0e16 = 2.22, so 1.0 < eps × 1.0e16. The 1.0 is below the resolution of 1.0e16 and is rounded away → result = 1.0e16.
- (1.0e16) + (-1.0e16) = 0.0 → (a + b) + c = 0.0, but the true answer is 1.0.
- a + (b + c) = 1.0 + 0.0 = 1.0.

The results differ because the relative magnitude of a compared to b determines whether a's contribution survives the rounding when a and b are added first.

**(c)** In a parallel MPI reduction, each process computes a local partial sum, then these are combined in a reduction tree (different orderings for different process counts). Because floating-point addition is not associative, different reduction trees produce different rounding sequences, which can give slightly different final sums even for identical input data. This means that the result of MPI_Reduce with MPI_SUM is NOT bitwise reproducible across different numbers of processes or different network topologies, even when the mathematical inputs are identical. This can be problematic for debugging, regression testing, and scientific reproducibility of HPC results.

**(d)** **Kahan compensated summation (Kahan summation algorithm):** maintain a running compensation term that accumulates the rounding errors lost in each addition step. The compensation is added back in each iteration, recovering most of the lost precision. This reduces the error from O(n × eps) for naive summation to O(eps) regardless of array length n.

**Marking points:** (a) correct explanation of per-operation rounding [2]; (b) correct setup with b = 1.0e16 (or equivalent) and correct results showing divergence [3]; (c) non-reproducibility across process counts / reduction tree orderings [2]; (d) Kahan summation or pairwise summation [1].

</details>

---

## Section G: True / False with Justification

### Q27
**True or False: "NaN is contagious — any arithmetic operation involving a NaN operand produces NaN."**

<details>
<summary>Model Answer</summary>

**True** (with minor nuance).

By IEEE 754, any arithmetic operation (+, -, ×, ÷, sqrt, etc.) that has a NaN as either operand must return NaN. This is the "quiet NaN" propagation rule — it ensures that once a computation goes invalid, the error signal is not silently lost but propagates forward through the calculation. Comparisons involving NaN always return false (including NaN == NaN), which is the basis for detecting NaN in code: `if (x != x)` is true only when x is NaN.

**Marking points (2 marks):** correct "True" [1]; explanation of propagation rule and/or NaN != NaN [1].

</details>

---

### Q28
**True or False: "Switching from double to single precision always halves the memory footprint of a floating-point array."**

<details>
<summary>Model Answer</summary>

**True** (as a statement about the direct memory cost of the array).

Double precision = 8 bytes per element; single precision = 4 bytes per element. An array of N elements occupies 8N bytes (double) vs 4N bytes (single) — exactly half.

This is one practical motivation for using single precision in memory-bound applications like graphics or machine learning: cutting memory footprint by half also halves the number of cache lines and memory bandwidth required, potentially doubling effective throughput for memory-bound kernels. However, care must be taken that the reduced precision is acceptable for the application.

**Marking points (2 marks):** correct "True" [1]; correct size reasoning (8 vs 4 bytes) [1].

</details>

---

### Q29
**True or False: "The result of 1.0 / 0.0 in C is undefined behaviour and may crash the program."**

<details>
<summary>Model Answer</summary>

**False** (for floating-point division).

For IEEE 754 floating-point types (float, double), dividing a non-zero value by 0.0 is well-defined: it returns +inf or -inf and raises the divide-by-zero exception flag. The program does NOT crash by default (unless exception trapping is explicitly enabled).

Important caveat: dividing an integer by zero (e.g., `int x = 1/0;`) IS undefined behaviour in C and typically causes a SIGFPE crash or trap. The question specifies `1.0 / 0.0`, where the literals are double-precision — this is the floating-point case and is well-defined by IEEE 754.

**Marking points (2 marks):** correct "False" [1]; correct explanation distinguishing floating-point (well-defined → inf) from integer (undefined behaviour) [1].

</details>

---

### Q30
**True or False: "The R_peak value for a processor is the same whether you are using single precision or double precision arithmetic."**

<details>
<summary>Model Answer</summary>

**False.**

R_peak = N_cores × R_clock × N_ops/cycle. The number of operations per cycle depends on the instruction set and the precision. Modern processors typically support wider SIMD registers for single precision than double precision:

- A 256-bit AVX register holds 4 double-precision (64-bit) values → 4 FLOP/s per FMA.
- The same 256-bit AVX register holds 8 single-precision (32-bit) values → 8 FLOP/s per FMA.

Therefore, single-precision R_peak is typically twice double-precision R_peak on the same hardware. This is why machine learning and graphics workloads (which can tolerate single precision) achieve much higher raw FLOP/s than scientific computing (which typically requires double precision).

The Zen cluster example: the X5560 delivered 4 double-precision FLOP/s per cycle; for single precision it would have been higher (8 FLOP/s/cycle with SSE4.2 in single precision mode).

**Marking points (2 marks):** correct "False" [1]; explanation that SIMD width gives more elements per register in single precision → higher ops/cycle → higher R_peak [1].

</details>

---

*End of Week 5 Practice Questions*

---

## Quick Reference: Key Formulas

```
IEEE 754 Single Precision (32-bit):
  Layout:  [1 sign][8 exponent][23 mantissa]
  Bias:    127
  Normal:  x = ±(1.mantissa)_2 × 2^(exponent_field - 127)
  eps:     2^{-23} ≈ 1.19 × 10^{-7}
  Range:   ~10^{-38} to ~10^{38}

IEEE 754 Double Precision (64-bit):
  Layout:  [1 sign][11 exponent][52 mantissa]
  Bias:    1023
  Normal:  x = ±(1.b1b2...b52)_2 × 2^(exponent_field - 1023)
  eps:     2^{-52} ≈ 2.22 × 10^{-16}
  Range:   ~10^{-308} to ~10^{308}
  Min norm: 2^{-1022} ≈ 2.2 × 10^{-308}
  Max norm: (2 - 2^{-52}) × 2^{1023} ≈ 1.8 × 10^{308}

Special Values (double):
  +inf:   sign=0, exp=11111111111, mantissa=0...0
  -inf:   sign=1, exp=11111111111, mantissa=0...0
  NaN:    exp=11111111111, mantissa≠0...0
  Zero:   exp=0...0, mantissa=0...0
  Subnormal: exp=0...0, mantissa≠0...0 → x = ±(0.mantissa)_2 × 2^{-1022}

Peak Performance:
  R_peak = N_sockets × N_cores/socket × R_clock × N_ops/cycle
  Cluster R_peak = N_nodes × node R_peak
```
