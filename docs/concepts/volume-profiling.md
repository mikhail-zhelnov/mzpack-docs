---
sidebar_position: 2
title: "Volume Profiling"
description: "Volume profiling concepts — how horizontal volume distribution reveals fair value, support/resistance, and areas of high and low liquidity"
---

# Volume Profiling

Standard charts show volume vertically — total volume per bar, spread across time. Volume profiling rotates this view 90 degrees, distributing volume *horizontally* across price levels. Instead of asking "how much traded during this bar?" it asks "how much traded at this price?" The result is a histogram that reveals where the market transacted the most and where it passed through quickly — a map of accepted and rejected prices.

## Volume at Price

A volume profile aggregates all trades within a time period and groups them by the price level at which they occurred. Each price level becomes a horizontal bar (called a **ladder**) whose length represents total volume at that price.

Longer ladders mean more contracts changed hands — the market found agreement at that price. Shorter ladders mean fewer contracts — the market moved through quickly, finding little agreement. This simple visual immediately highlights where the market considers price "fair" and where it does not.

## Point of Control (POC)

The **Point of Control** is the price level with the highest volume in the profile — the single price where the most trade facilitation occurred. It represents the market's consensus fair value for the period.

- Price tends to gravitate toward the POC during balanced markets
- A POC that migrates higher or lower across sessions indicates a shifting perception of fair value
- The **developing POC** updates in real time as the profile builds, showing where fair value is forming within the current session

## Value Area

The **Value Area (VA)** is the price range containing a specified percentage (default 68%) of the total profile volume. It represents one standard deviation of volume around the POC — the range where the market accepted price.

| Element | Definition |
|---|---|
| **Value Area High (VAH)** | The upper boundary — price above this level was rejected by most volume |
| **Value Area Low (VAL)** | The lower boundary — price below this level was rejected by most volume |
| **VA width** | VAH minus VAL — a narrow VA means tight consensus; a wide VA means broad acceptance |

The 68% default mirrors one standard deviation in a normal distribution. Some traders use 70% for a rounder number — the concept remains the same.

### Value Area as Support and Resistance

Prior session Value Area levels are among the most-watched reference points in profile-based trading:

- **Price opens above prior VA** — bullish bias; prior VAH becomes support
- **Price opens below prior VA** — bearish bias; prior VAL becomes resistance
- **Price opens inside prior VA** — balanced; expect rotation between VAH and VAL
- **Price breaks through VAH** — potential acceptance at higher prices
- **Price breaks through VAL** — potential acceptance at lower prices

## High Volume and Low Volume Nodes

Beyond POC and VA, the shape of the profile itself reveals important structure:

- **High Volume Node (HVN)** — a price area with a concentration of volume. Price tends to slow down and consolidate at HVNs because the market previously found agreement there. HVNs act as magnets — when price approaches one, it often stalls or rotates.
- **Low Volume Node (LVN)** — a price area with little volume. Price tends to move quickly through LVNs because the market previously rejected those levels. LVNs act as barriers — price either blows through them fast or reverses at their edges.

The alternation of HVNs and LVNs defines the profile's shape. A profile with a single dominant HVN and thin tails indicates a balanced session. A profile with two HVNs separated by an LVN shows a double distribution — the market found two separate areas of value within the period.

## VWAP

**Volume Weighted Average Price (VWAP)** is the average price weighted by volume — the true mean price at which contracts traded. While POC is the *mode* (most frequent price), VWAP is the *mean* (average price).

VWAP is calculated as:

**VWAP** = cumulative (price x volume) / cumulative volume

VWAP and its standard deviation bands provide a statistical framework:

| Level | Meaning |
|---|---|
| **VWAP** | The volume-weighted mean price — institutional benchmark for "fair" execution |
| **+1 / -1 standard deviation** | Contains ~68% of volume — the statistical value area |
| **+2 / -2 standard deviations** | Contains ~95% of volume — extremes within the distribution |

- Price above VWAP means the average buyer is in profit; price below means the average buyer is underwater
- The deviation bands act as dynamic support and resistance that tighten in balanced markets and expand in trending ones
- **Dynamic VWAP** plots as a line that updates with each bar; **Last VWAP** draws a static horizontal line at the current VWAP value

## Naked Levels

A **naked level** is a POC, VAH, or VAL from a prior profile that price hasn't traded through yet. The concept applies to both Volume Profile and Market Profile levels.

- **Naked POC** — a prior session's fair value price that hasn't been revisited. The market left unfinished business at that level.
- **Naked VAH / VAL** — a prior value area boundary that hasn't been tested. Price often returns to these levels before continuing.

Naked levels act as magnets because they represent prices where significant volume traded but that haven't been retested by subsequent sessions. MZpack tracks naked levels automatically and removes them when price trades through.

## Level Modes

MZpack offers six ways to display POC and VAH/VAL levels, from static to dynamic:

| Mode | Behavior |
|---|---|
| **Off** | Level not displayed |
| **On** | Level drawn within the profile boundaries only |
| **Extended** | Level extends from the profile edge to the right side of the chart |
| **Naked** | Level extends rightward until price touches it, then disappears |
| **Developing** | Level updates in real time as the profile builds |
| **DevelopingNaked** | Developing level that disappears when price touches it |

**Developing** modes are useful for watching where fair value (POC) or the value area boundaries (VAH/VAL) are settling within the current session. **Naked** modes are useful for tracking unfinished levels from prior sessions.

## Profile Types

Volume Profile can display four different views of the same data, each emphasizing a different aspect of volume:

| Type | Shows | Use Case |
|---|---|---|
| **Volume** | Total volume at each price | Standard view — where did the most trading occur? |
| **BuySell** | Buy and sell volume as separate ladders | Where were buyers vs sellers concentrated? |
| **Delta** | Net difference (ask minus bid) at each price | Where was the buying or selling pressure strongest? |
| **VolumeDelta** | Total volume ladders colored by delta direction | Combined view — volume size plus directional bias |

The **BuySell** and **Delta** types require accurate trade classification — see [Order Flow — Trade Classification](order-flow.md#trade-classification) for how MZpack splits volume into buying and selling.

## Multi-Timeframe Profiling

A single profile shows one time period. The real power of volume profiling comes from layering multiple timeframes to see both the forest and the trees:

- **Session or Daily profile** — where is today's value developing?
- **Weekly profile** — where is this week's acceptance range?
- **Monthly or Quarterly profile** — where is the longer-term fair value?

When a daily POC aligns with a weekly VAH, that level carries more weight than either alone. When the daily value area is entirely above the weekly POC, the market is pushing higher within the larger context.

MZpack supports up to 3 independent **stacked profiles** displayed on the chart margin, each with its own time period, profile type, and level settings. This lets you see session, weekly, and monthly profiles simultaneously. See [mzVolumeProfile — Stacked Profiles](../indicators/mzVolumeProfile.md#stacked-profiles) for configuration.

## Composite Profiles

A **composite profile** aggregates volume across all loaded chart data into a single profile, revealing the big-picture volume distribution. Unlike session or daily profiles that reset, a composite profile accumulates continuously.

Composite profiles are useful for identifying:

- **Long-term POC** — the price the market has accepted most over the entire visible history
- **Long-term HVNs and LVNs** — major support/resistance zones and transition areas that may not be visible on individual session profiles
- **Current price relative to long-term value** — whether the market is trading at, above, or below its historical fair value

## Where to Go Next

- **[mzVolumeProfile](../indicators/mzVolumeProfile.md)** — configure Volume Profile display, levels, VWAP, and stacked profiles
- **[Market Profile (TPO)](market-profile.md)** — time-based profiling concepts and how they complement volume profiling
- **[Order Flow](order-flow.md)** — understanding the trades that build volume profiles
- **[Delta Analysis](delta-analysis.md)** — deeper dive into delta interpretation at the profile level
