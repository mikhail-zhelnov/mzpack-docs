---
sidebar_position: 7
title: "Strategy Pipeline"
description: "Runtime execution order of pattern components — signals, filters, actions, entry, exit, trail, and risk management."
---

# Strategy Pipeline

This page explains the runtime execution order of components inside a `Pattern`. Each component is described in detail on its own page — see [See Also](#see-also) below.

## Execution Flow

On every bar update (or tick, depending on `SignalCalculate`), the pattern evaluates its components in a fixed order:

```
OnBarUpdate()
 └── Pattern.Evaluate()
       ├── [1] Signals / Decision Tree  → Long | Short | None
       ├── [2] Filter                   → pass | block
       ├── [3] Action                   → side effect (pre-entry)
       ├── [4] Entry                    → submit order + set stop
       └── [5] Exit / Trail             → manage open position
                 │
                 └── Risk Management    → session-level guard (max loss, max trades)
```

## Component Responsibilities

| Component | Class(es) | Responsibility |
|---|---|---|
| Signal / Decision Tree | `Signal`, `LogicalNode`, `RangeNode` | Determine trade direction from market data |
| Filter | `ValueInRangeFilter` | Gate signal by an external condition (value in range) |
| Action | `Action`, `RollingProfileAction` | Side effect before or after entry |
| Entry | `Entry`, `BarStopLossEntry`, `SignalStopLossEntry`, `FiboRetracementEntry` | Order submission and initial stop placement |
| Exit | `BarCloseTarget` | Fixed profit target |
| Trail | `Trail`, `BarHiLoTrail` | Dynamic stop management after activation |
| Risk Management | `RiskManagement` | Max loss, max drawdown, max profit, and max trades per session |

## Key Rules

Signals are evaluated first. If the decision tree returns `None`, the remaining components are not invoked — the pattern short-circuits and waits for the next bar or tick.

Action executes before Entry. It is typically used for cancelling pending limit orders, logging, or updating rolling profile state before a new order is submitted.

Risk Management is the last barrier. It blocks Entry independently of the signal result, enforcing session-level caps on loss, drawdown, profit, and trade count.

## See Also

- [Action](action.md) — side effects before/after entry
- [Entry](entry.md) — order submission (Market, Limit, StopLimit)
- [Exit](exit.md) — profit target and exit signals
- [Trail](trail.md) — trailing stop management
- [Filter](filter.md) — signal gating by external conditions
- [Decision Tree](decision-tree.md) — AND/OR/CONJUNCTION signal combination
- [Risk Management](risk-management.md) — session-level trading limits
