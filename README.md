# Evolving a Smiley Face with a Genetic Algorithm

[English](README.md) | [Turkish](README.tr.md)

A small experiment that evolves a hand-drawn smiley face sketch (two eyes and a dotted smile) on a 28x28 pixel white image from scratch, using a genetic algorithm.

![Evolution stages](evrim.png)

## How it works

| Component | Choice |
|---|---|
| Individual | 784-bit array (28x28 pixels, 1 = black, 0 = white) |
| Initialization | Random noise |
| Fitness | Number of pixels matching the target (max 784) |
| Selection | Tournament selection (size 3) |
| Crossover | Uniform crossover |
| Mutation | Bit flip with probability 1/784 per gene |
| Elitism | The best 2 individuals are copied unchanged to the next generation |
| Population | 200 individuals |

The target image is defined with coordinates in the `hedef_olustur()` function: two eyes (a ring with a dot in the center) and a dotted smile arranged along a parabola.

## Result

With a fixed seed (`seed=42`), the algorithm reaches **784/784 pixels at generation 102**.

![Fitness curve](uygunluk.png)

## Usage

```bash
pip install numpy matplotlib
python ga_smiley.py
```

Running it prints the final generation and the best fitness to the console, and generates:

- `evrim.png`: the target next to the best individual at selected generations (0, 25, 50, 100, ...)
- `uygunluk.png`: best fitness per generation

## Notes

Because fitness is computed by comparing directly against the target image, this problem is easy for a genetic algorithm (similar to OneMax). A more interesting variant would represent each individual with a few parameters, such as eye positions, radii and the curvature of the smile.

## Files

- `ga_smiley.py`: algorithm and visualization
- `evrim.png`, `uygunluk.png`: example outputs
- `README.tr.md`: Turkish version of this README
