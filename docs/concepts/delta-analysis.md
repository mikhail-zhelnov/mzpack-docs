---
sidebar_position: 3
title: "Delta Analysis"
description: "Understanding delta analysis, cumulative delta, and delta divergence for trading decisions"
---

# Delta Analysis

Delta measures the net difference between buying and selling aggression — it is defined and calculated in [Order Flow](order-flow.md#delta). This page covers how to *interpret* delta in a trading context: what it tells you about market participants, how to read divergences, and how derived metrics like COT, ratio numbers, and delta rate add analytical depth.

## Reading Delta in Context

A positive or negative delta tells you which side was more aggressive, but its significance depends on *where* it occurs:

- **Large delta at a price extreme** — aggressive activity at the edge of a range. If price fails to continue, the aggression was absorbed by passive orders on the other side, suggesting a potential reversal.
- **Large delta mid-range** — aggressive activity in the body of a move. This typically confirms trend continuation — participants are pushing price through, not testing a boundary.
- **Delta with volume confirmation** — high delta accompanied by high volume shows genuine directional conviction. High delta on low volume may just reflect a thin market.
- **Delta against volume** — rising volume but shrinking delta means both sides are participating equally. Activity is increasing, but neither side is winning — a sign of balance or an approaching turning point.

Delta is most useful when read alongside price action and volume, not in isolation.

## Cumulative Delta

Cumulative delta is the running sum of bar deltas across a session. Where a single bar's delta shows a snapshot of aggression, cumulative delta reveals who has controlled the session overall.

**Trend confirmation:**
- Rising cumulative delta + rising price = buyers are in control, and price reflects it
- Falling cumulative delta + falling price = sellers are in control, and price reflects it

**Warning signals:**
- Flat or falling cumulative delta + rising price = price is advancing without sustained buyer commitment. The rally may lack the aggressive buying needed to continue.
- Flat or rising cumulative delta + falling price = price is dropping without sustained seller commitment. The decline may lack follow-through.

By default, cumulative delta resets at the start of each session, giving fresh context each trading day. This session reset prevents carryover from overnight activity from distorting the intraday picture. Continuous (non-resetting) accumulation is also available when you want to track multi-day flows.

## Delta Divergence

Delta divergence is the core reversal-warning concept in order flow analysis. It occurs when price and cumulative delta move in opposite directions between two swing points:

- **Price makes a new high, but cumulative delta is negative between those swings** — sellers are present despite higher prices. The uptrend is losing momentum because the new high was not driven by buyer aggression.
- **Price makes a new low, but cumulative delta is positive between those swings** — buyers are present despite lower prices. The downtrend is losing momentum because the new low was not driven by seller aggression.

**Important:** Divergence signals a *loss of momentum*, not an immediate reversal. It is a warning that the aggressive side driving the trend is weakening. Stronger divergence — a larger delta reading against the price direction — carries more weight as a warning. Divergence works best when combined with other context: support/resistance levels, volume profile nodes, or absorption patterns.

For automated divergence detection with configurable ZigZag breakpoints and deviation filters, see [mzDeltaDivergence](../indicators/mzDeltaDivergence.md).

## COT (Commitment of Traders)

COT measures the market's reaction to a new price extreme. It is the cumulative delta starting from the moment price makes a new high or low (or repeats the previous one):

- **COT High** — cumulative delta from the bar that prints a new high. It answers: after the market tested this new high, did buyers or sellers commit?
- **COT Low** — the same logic at new lows. It answers: after the market tested this new low, did buyers or sellers commit?

Think of the new extreme as a **market test** and COT as the **reaction** to that test:

- **Negative COT High while price holds at highs** — price reached a new high, but the cumulative delta since that high is negative (more sell aggression). Yet price is not falling. This means passive buy limit orders are absorbing the sell aggression — hidden support. The larger the absolute value of COT High, the more committed the passive buyers are.
- **Positive COT Low while price holds at lows** — price reached a new low, but the cumulative delta since that low is positive (more buy aggression). Yet price is not rising. This means passive sell limit orders are absorbing the buy aggression — hidden resistance. The larger the absolute value of COT Low, the more committed the passive sellers are.
- **Growing COT (absolute value)** over time indicates increasing commitment by the passive side. If COT continues to build while price stays near the extreme, the passive orders are substantial.

COT is displayed in the [mzFootprint bar statistics](../indicators/mzFootprint.md#cot-commitment-of-traders) panel.

## Ratio Numbers

Ratio numbers classify the activity at a bar's price extremes into three states: neutral, rejected, or defended. They measure whether the extreme price was accepted by the market or pushed back.

**Calculation:** For an up-bar, the ratio is bid volume above the bar low divided by bid volume at the bar low. For a down-bar, the ratio is ask volume below the bar high divided by ask volume at the bar high.

| Ratio Value | State | Meaning |
|---|---|---|
| 0.71–29.0 | **Neutral** | Normal trade facilitation — no strong signal at the extreme |
| > 29.0 | **Rejected** | The extreme price was rejected by the market |
| < 0.71 | **Defended** | The extreme price is being defended by limit orders |

**Interpreting rejected and defended states:**

- **Rejected below an up-bar** — lower prices were rejected. Traders moved away from the low quickly, with very little volume left at the extreme relative to the levels above it. Bullish implication: the market does not accept these lower prices.
- **Rejected above a down-bar** — higher prices were rejected. Traders moved away from the high quickly. Bearish implication: the market does not accept these higher prices.
- **Defended below an up-bar** — the low is being defended by limit orders. Significant bid volume remains at the bar low, preventing price from breaking lower. Bullish implication: passive buyers are supporting this level.
- **Defended above a down-bar** — the high is being defended by limit orders. Significant ask volume remains at the bar high, preventing price from breaking higher. Bearish implication: passive sellers are capping this level.

Ratio numbers appear in the [mzFootprint bar statistics](../indicators/mzFootprint.md#ratio-numbers) panel with configurable bounds and colors.

## Delta Rate

Delta rate measures how fast delta changes within a time or tick interval. Only the maximal (absolute) delta rate per bar is tracked — it captures the most intense burst of aggressive activity within that bar.

A high delta rate indicates **concentrated aggressive activity in a short window**. Common causes include:

- **Stop-loss cascade** — a cluster of stop orders triggers in rapid succession, producing a spike of one-sided aggression
- **Breakout** — price punches through a level with a burst of market orders
- **Reversal initiation** — a sudden wave of counter-trend aggression overwhelms the prevailing side

Delta rate distinguishes between gradual accumulation and aggressive bursts. Two bars may have similar total delta, but very different delta rates:

- **Low rate, steady delta** — gradual, sustained buying or selling over the bar's duration. Orderly participation.
- **High rate, spike delta** — the same delta concentrated in a brief moment. Urgent, reactive participation — often driven by stops or algorithmic triggers.

Delta rate is available in the [mzFootprint bar statistics](../indicators/mzFootprint.md#bar-statistics) panel.

## Unfinished Auction

An unfinished auction occurs at a bar's high or low when no trades were executed on the opposing side at that price:

- **Unfinished auction at a bar high** — no sell trades occurred at the highest price. The auction process did not complete — sellers never tested this level.
- **Unfinished auction at a bar low** — no buy trades occurred at the lowest price. The auction process did not complete — buyers never tested this level.

An unfinished auction suggests that price may revisit the level in the future to complete the two-sided auction. It is not a directional signal by itself, but it marks a price where the market's price discovery process was left incomplete.

## Delta Patterns

Several recurring delta patterns serve as building blocks for trading signals. The table below summarizes the core patterns conceptually — for signal implementations with entry/exit logic, filters, and combination rules, see [Built-in Strategies](../strategies/built-in-strategies.md).

| Pattern | Description |
|---|---|
| **Delta Divergence** | Price makes a new extreme while delta moves in the opposite direction — loss of momentum at swing points |
| **Delta Tail** | Negative delta across all price levels in a bar except the extreme, showing absorption at the bar's high or low |
| **Delta Surge / Drop** | Consecutive bars of increasing (or decreasing) delta — momentum building in one direction |
| **Delta Flip** | Sudden shift from positive to negative delta (or vice versa) between consecutive bars — abrupt change in aggression |
| **Delta Trap** | Delta reversal followed by renewed strength in the original direction — a false shift that traps the wrong side |
| **Delta Slingshot** | An extreme delta reading gets overrun by the opposite extreme within a lookback range — trend reversal from exhaustion |

These patterns are most effective when they align with structural context — support/resistance levels, volume profile nodes, or session extremes.

## Where to Go Next

- [mzVolumeDelta](../indicators/mzVolumeDelta.md) — delta histograms, candles, and cumulative delta display
- [mzDeltaDivergence](../indicators/mzDeltaDivergence.md) — automated delta-price divergence detection
- [mzFootprint](../indicators/mzFootprint.md) — footprint-level delta, COT, ratio numbers, and delta rate
- [Order Flow](order-flow.md) — foundational delta definitions and trade classification
- [Volume Profiling](volume-profiling.md) — delta as a profile type in volume distribution
