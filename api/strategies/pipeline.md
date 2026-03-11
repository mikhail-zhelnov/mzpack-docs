---
sidebar_position: 8
title: "Strategy Pipeline"
description: "Runtime execution order of pattern components — signals, filters, actions, entry, exit, trail, and risk management."
---

# Strategy Pipeline

This page explains the runtime execution order of components inside a `Pattern`. Each component is described in detail on its own page — see [See Also](#see-also) below.

## Execution Flow

On every bar update (or tick, depending on `SignalCalculate`), the pattern evaluates its components in this order:

```
OnBarUpdate()
 └── Pattern.Evaluate()
       ├── [1] Decision Tree            → Long | Short | None
       │     ├── Signal (condition)
       │     ├── Action : Signal        → side effect anywhere in tree
       │     ├── LogicalNode (AND/OR)
       │     └── Filter (gate)
       ├── [2] Entry                    → submit order + set stop
       └── [3] Exit / Trail             → manage open position
                 │
                 └── Risk Management    → session-level guard (max loss, max trades)
```

## Component Responsibilities

| Component | Class(es) | Responsibility |
|---|---|---|
| Signal / Decision Tree | `Signal`, `LogicalNode`, `RangeNode` | Determine trade direction from market data |
| Filter | `ValueInRangeFilter` | Gate signal by an external condition (value in range) |
| Action | `Action : Signal`, `RollingProfileAction` | Decision Tree node; executes a side effect at any position in the tree. Execution order is determined by tree structure |
| Entry | `Entry`, `BarStopLossEntry`, `SignalStopLossEntry`, `FiboRetracementEntry` | Order submission and initial stop placement |
| Exit | `BarCloseTarget` | Fixed profit target |
| Trail | `Trail`, `BarHiLoTrail` | Dynamic stop management after activation |
| Risk Management | `RiskManagement` | Max loss, max drawdown, max profit, and max trades per session |

## Key Rules

The decision tree is evaluated first. If it returns `None`, the remaining components are not invoked — the pattern short-circuits and waits for the next bar or tick.

Action inherits from `Signal` and is a Decision Tree node — it can appear at any position in the tree. Execution order is determined by tree structure, not by a fixed pipeline sequence.

Risk Management is the last barrier. It blocks Entry independently of the signal result, enforcing session-level caps on loss, drawdown, profit, and trade count.

## See Also

- [Action](action.md) — side effect node in the decision tree
- [Entry](entry.md) — order submission (Market, Limit, StopLimit)
- [Exit](exit.md) — profit target and exit signals
- [Trail](trail.md) — trailing stop management
- [Filter](filter.md) — signal gating by external conditions
- [Decision Tree](decision-tree.md) — AND/OR/CONJUNCTION signal combination
- [Risk Management](risk-management.md) — session-level trading limits
