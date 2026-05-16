# Baum-Welch Algorithm

**Type:** algorithm
**Week:** 7
**Related:** [[hidden-markov-model]], [[forward-algorithm]], [[viterbi-algorithm]]
**Source:** [[lecture-w7]]

## Definition
The Baum-Welch algorithm is an expectation-maximisation (EM) algorithm used to find the unknown parameters of a Hidden Markov Model (HMM) given a set of observed emissions.

## Motivation
When we have a sequence of observations but don't know the underlying states or the transition/emission probabilities, we need a way to learn these parameters from data. Baum-Welch solves this unsupervised learning problem.

## How it works
It alternates between two steps:
- **E-step:** Calculate the expected number of times each state is visited and each transition is taken, using the Forward-Backward algorithm (based on current parameters).
- **M-step:** Update the transition and emission probabilities to maximise the likelihood of the observed sequence, given these expectations.

## Key derivation
Not required for exam.

## Parameters & intuition
- Iteratively improves the likelihood of the observation sequence.
- Guarantees convergence to a local maximum, but not necessarily a global maximum (sensitive to initialisation).

## Connections
- Applies the EM algorithm specifically to [[hidden-markov-model]]s.

## Exam notes
- **NOT EXAMINABLE**: For Week 7 (HMMs), only the Forward and Viterbi algorithms are examinable.
