---
sidebar_position: 4
title: "Market Profile (TPO)"
description: "Market Profile concepts — how time-based price analysis reveals market structure, value areas, and auction dynamics"
---

# Market Profile (TPO)

Market Profile organizes price data by *time* rather than just price and volume. Developed by J. Peter Steidlmayer at the CBOT in the 1980s, it shows how long price traded at each level, revealing where the market finds acceptance versus rejection. Instead of asking "how much traded here?" it asks "how long did the market stay here?" — a fundamentally different lens on market structure.

## Time Price Opportunity

The building block of Market Profile is the **Time Price Opportunity (TPO)**. One TPO represents one time period (default 30 minutes) during which a price level was visited. Each period is assigned a letter — A for the first period, B for the second, C for the third, and so on — or displayed as a block.

- **More TPOs at a price** = more time spent = the market *accepted* that price
- **Fewer TPOs at a price** = price quickly moved away = the market *rejected* that price

By stacking these letters horizontally at each price level, Market Profile builds a visual distribution of time across price — wide where the market lingered, narrow where it passed through quickly.

## Profile Structure

A complete Market Profile consists of several key structural elements:

| Element | Definition |
|---|---|
| **Point of Control (POC)** | The price level with the most TPOs — the "fairest price" where the most trade facilitation occurred |
| **Value Area (VA)** | The range containing 68% of all TPOs (one standard deviation) — where the market accepted price |
| **Value Area High (VAH)** | The upper boundary of the Value Area |
| **Value Area Low (VAL)** | The lower boundary of the Value Area |
| **Halfback** | The midpoint of the profile range: (High + Low) / 2 |
| **Single prints** | Price levels with only one TPO letter — low acceptance zones that often act as future price magnets |

The POC represents equilibrium — the price where the market spent the most time and where buyers and sellers found the most agreement. The Value Area defines the range of prices the market considered "fair" during the session.

## Initial Balance

The **Initial Balance (IB)** is the price range established during the opening period of the session — by default the first 60 minutes (configurable). IB High and IB Low define this opening range.

The Initial Balance sets the reference framework for the rest of the session:

- **Range extension beyond IB** signals directional conviction — one side has gained control and is pushing price outside the opening range
- **Narrow IB** suggests potential for a large range day — the market hasn't committed early, leaving room for a breakout
- **Wide IB** suggests potential for a balanced day — the market found its range early and may stay within it

## Profile Shapes and Day Types

The shape of a completed Market Profile tells you what kind of day the market had:

| Shape | Characteristics | Interpretation |
|---|---|---|
| **Normal (bell curve)** | Wide middle, thin tails | Balanced, range-bound day; trade facilitation dominates |
| **b-shape** | Wide bottom, thin top | Selling early, buying late (short covering rally); accumulation at lows |
| **P-shape** | Thin bottom, wide top | Buying early, selling late (long liquidation); distribution at highs |
| **D-shape (double distribution)** | Two wide areas separated by thin middle | A breakout occurred mid-session, creating two value areas |
| **Elongated/trend** | Thin profile throughout, no clear bell | Directional day; price moved away from the open with little rotation |

Recognizing these shapes in real time helps you understand whether the market is balancing or trending, and whether a directional move is likely to continue or reverse.

## Naked Levels

A **naked level** is a POC, VAH, or VAL from a prior session that price hasn't revisited. These levels act as magnets — the market tends to return to them because they represent unfinished business: price levels where value was established but not yet retested.

- A **naked POC** from two days ago means the market's fairest price from that session was never revisited
- A **naked VAH or VAL** marks an untested boundary of a prior value area

MZpack tracks naked levels automatically and cancels them when price trades through. Naked levels can be configured per profile using the T-index system — see [mzVolumeProfile — TPO Levels](../indicators/mzVolumeProfile.md#tpo-levels) for configuration details.

## TPO Count and Balance

The total **TPO count** is the number of letters in a profile — it reflects how many time periods the session covered and how much price rotated.

More useful is the split between **TPOs above POC** and **TPOs below POC**:

- **More TPOs above POC** — the market spent more time above fair value, suggesting upward acceptance or potential distribution
- **More TPOs below POC** — the market spent more time below fair value, suggesting downward acceptance or potential accumulation
- **Roughly equal** — balanced session, no directional time bias

This asymmetry provides a directional bias that complements volume-based analysis.

## Profile Time Periods

Market Profile can be built over different time periods to provide context at multiple scales:

| Period | Use Case |
|---|---|
| **Session / Daily** | Standard intraday reference — the most common Market Profile view |
| **Weekly** | Intermediate-term value areas and POC levels |
| **Monthly / Quarterly** | Higher-timeframe context for swing and position traders |
| **Composite** | Cumulative profile across all loaded data — shows the big picture |

MZpack supports 18+ profile creation modes beyond these standard periods, including volume-based, delta-based, tick-based, and custom multi-session profiles. See [mzVolumeProfile](../indicators/mzVolumeProfile.md) for the full list of profile modes.

## Market Profile vs Volume Profile

Market Profile and Volume Profile answer related but distinct questions:

| | Market Profile (TPO) | Volume Profile |
|---|---|---|
| **Measures** | *Time* at price | *Volume* at price |
| **Question** | Where did the market spend the most time? | Where did the most contracts trade? |
| **POC meaning** | Price with the most time periods | Price with the most volume |

The two often agree — prices with high volume tend to have high time as well. But **divergences between them are informative**:

- **High volume, low TPO count** — aggressive activity compressed into a short time; a spike or stop run rather than acceptance
- **Low volume, high TPO count** — quiet market sitting at a level; acceptance without conviction
- **TPO POC and VP POC at different prices** — time-based and volume-based fair value disagree, which can signal a developing imbalance

MZpack can display both TPO and Volume Profile simultaneously on the same chart, making these divergences easy to spot.

## Where to Go Next

- **[mzVolumeProfile](../indicators/mzVolumeProfile.md)** — configure TPO display, levels, Initial Balance, and profile modes
- **[Volume Profiling](volume-profiling.md)** — volume distribution concepts (POC, VA, VWAP)
- **[Order Flow](order-flow.md)** — understanding the trades that build profiles
