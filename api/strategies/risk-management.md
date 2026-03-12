---
sidebar_position: 16
title: "Risk Management"
description: "Reference for RiskManagement — session-level guard that enforces daily profit, loss, drawdown, and trade count limits."
---

# Risk Management

`RiskManagement` is a session-level guard that blocks entry independently of signal results. It enforces daily caps on profit, loss, drawdown, and trade count. Limits reset automatically on each new trading day.

**Namespace:** `MZpack.NT8.Algo`
**Inheritance:** `RiskManagement`
**Source:** `[INSTALL PATH]/API/RiskManagement.cs`

## Properties

### Daily Profit Limit

| Property | Type | Default | Description |
|---|---|---|---|
| `DailyProfitLimitEnable` | `bool` | `false` | Enable daily profit limit |
| `DailyProfitLimit` | `double` | — | Maximum daily profit in `Currency` |

### Daily Loss Limit

| Property | Type | Default | Description |
|---|---|---|---|
| `DailyLossLimitEnable` | `bool` | `false` | Enable daily loss limit |
| `DailyLossLimit` | `double` | — | Maximum daily loss in `Currency` |

### Daily Max Drawdown

| Property | Type | Default | Description |
|---|---|---|---|
| `DailyMaxDrawdownEnable` | `bool` | `false` | Enable daily max drawdown |
| `DailyMaxDrawdown` | `double` | — | Maximum drawdown from daily peak in `Currency` |

### Daily Trades Limit

| Property | Type | Default | Description |
|---|---|---|---|
| `DailyTradesLimitEnable` | `bool` | `false` | Enable daily trades limit |
| `DailyTradesLimit` | `int` | — | Maximum number of trades per day |

### General

| Property | Type | Default | Description |
|---|---|---|---|
| `Currency` | `Currency` | `UsDollar` | Account currency for limit calculations |
| `EntryName` | `string` | — | Entry name used to count trades |

## Methods

| Method | Description |
|---|---|
| `IsEnabled()` | Returns `true` if any limit is enabled |
| `IsRiskReached()` | Returns `true` if any enabled limit has been reached |
| `OnAccountItemUpdate(Account account, AccountItem item, double value)` | Monitors realized and unrealized PnL; closes all positions when a limit is hit |
| `OnOrderUpdate(Order order, OrderState state)` | Increments the daily trade count when an order with matching `EntryName` is filled |
| `OnMarketData(DateTime time)` | Resets all tracking on a new trading day |

## Limit Logic

| Limit | Triggered When |
|---|---|
| Daily Profit | `realizedPnL + unrealizedPnL >= DailyProfitLimit` |
| Daily Loss | `realizedPnL + unrealizedPnL <= -DailyLossLimit` |
| Max Drawdown | `CashValue - maxCashValue <= -DailyMaxDrawdown` |
| Daily Trades | `dailyTrades >= DailyTradesLimit` |

When any limit is reached, `RiskManagement` calls `Strategy.Positions.CancelClose(false, "Risk Management", ...)` to close all open positions and prevent new entries.

## Daily Reset

On each new trading day (detected in `OnMarketData`), all counters and flags reset:

- `dailyTrades` resets to 0
- `maxCashValue` updates to the current cash value
- All `reached` flags clear

## See Also

- [Pipeline](pipeline.md) — execution order of components
- [Entry](entry.md) — order submission
- [Algo.Strategy](algo-strategy.md) — parent strategy class
