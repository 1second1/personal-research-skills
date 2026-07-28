## Research Question

On the selected segmentation dataset and fixed training budget, does adding the lightweight attention block improve Dice score over the baseline without exceeding the memory budget?

## Motivation

The question tests whether the added complexity produces a measurable benefit under the project's resource constraint.

## Hypothesis

The attention variant improves Dice while remaining within the memory budget.

## Variables

- Independent: model variant.
- Dependent: Dice score and peak GPU memory.
- Controls: dataset split, seed, optimizer, epochs, and input resolution.

## Assumptions

- The split is representative of the intended task.

## Boundaries

Results apply only to the selected dataset, implementation, and training budget.

## Falsification

Reject the hypothesis if Dice does not improve or the memory budget is exceeded across the predefined repeated runs.

## Next Actions

1. Freeze the baseline configuration and record its metrics.
2. Implement the attention variant and record the diff.
3. Run the same seeds and compare a fixed metric table.
