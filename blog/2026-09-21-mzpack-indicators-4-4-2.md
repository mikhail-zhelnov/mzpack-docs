---
title: "MZpack Indicators w/ Divergence 4.4.2"
authors: [mzpack]
tags: [indicators]
---

This release brings user-defined price aggregation to mzMarketDepth, prints the values of a truncated top cluster in mzFootprint in full, and fixes a set of Historical DOM visibility and colouring problems.

<!-- truncate -->

## Price aggregation (mzMarketDepth)

On fast instruments like GC, price runs through several ticks in a single print, and liquidity read tick by tick is hard to follow. "Ticks per level" merges N consecutive ticks into one zone, at a resolution the market actually moves in. The merge happens in the model rather than at draw time, so everything fed by the order book — thresholds, colour scales, the pop-up and the liquidity migration markers — keeps working on the merged scale without a special case.

### New

- **"Ticks per level"** — user-defined aggregation of DOM price levels, in the Common group. 1 is the previous behaviour and the default; any value is allowed. It works across the whole indicator: Realtime DOM, Cumulative, per-level Imbalance, Historical DOM and Liquidity Migration. Zones sit on an absolute price grid anchored at 0, not on the moving best bid or offer, so their boundaries stay put when the book moves or the chart is scrolled and rescaled. Bid zones are keyed by their lowest price and Ask zones by their highest, which keeps the single zone straddling the spread from collapsing into one block flipping sides on every quote. The name, the description and the type repeat the existing "Ticks per level" of mzFootprint and mzVolumeProfile (#78).

### Improvements

- **"Depth of market" keeps counting ticks, not zones** — depth is capped before the merge. Side totals therefore do not move with "Ticks per level": the Imbalance line, Overall liquidity, the Totals liquidity-migration plot and the Quantative Depth metrics are identical at every setting. The ladder shows depth / "Ticks per level" rows — at the default depth of 100 and 5 ticks per level, 20 zones per side.
- **Zones at both edges of the book are clipped to the depth window** — the aggregation grid is absolute, so an edge zone used to run past it. Only the spread side was cut: the deepest level covered up to "Ticks per level" − 1 ticks the DOM said nothing about, and historical bricks were not clipped at all and overlapped the opposite side of the book.
- **Realtime DOM "Imbalance ratio"** now compares a zone against the average zone of its side, as it previously compared a level against the average level. The number keeps its meaning and needs no retuning.
- **Absolute volume settings apply to the merged zone volume** — "Display volume" and "Extreme volume" in the Absolute filtering mode, "Volumes filter", "Added volume filter" and "Removed volume filter". They therefore filter out less at a "Ticks per level" above 1; raising them roughly in proportion to the setting restores the previous density. The Percentage, AdaptiveLess and AdaptiveMore modes derive from the volume range and rescale by themselves.
- **Liquidity migration is measured per zone** against the same zone one bar ago, so liquidity moved between ticks inside one zone no longer produces a marker — only the net change of the zone does.
- **Changing "Ticks per level" clears the accumulated Historical DOM**, which then rebuilds forward from the current order book. Blocks collected on the previous grid cannot be re-aggregated, because the raw market depth event stream is not retained. The liquidity and migration series are aggregation-invariant and are kept.
- **The pop-up of a merged Historical DOM level** reports the price range of the zone instead of a single price.

## New Features

- **mzFootprint: "Full top cluster values"** — the values of the topmost cluster of a bar are printed in full when price levels are aggregated. With "Ticks per level" above 1 the clusters of a bar are built upwards from its low, so the last one is as a rule shorter than the rest — it is cut off by the bar high — and its bid × ask did not fit the cell it was laid out into: at a fixed font size it was dropped outright and the top of the ladder came out blank, at an auto-scaled one it was centred in a cell too short for it and spilled out of it in both directions. The values of a truncated cluster are now laid out into a cluster of the full height anchored at the bottom of the cell, so they read exactly like every other row. This applies to the printed values only — the cluster fill, the imbalance and absorption markers and the bar itself keep the truncated height, so what the bar shows about price is unchanged and only the text reaches above the high. Bar statistics move up by the same amount to leave the values their room. The option is on by default, turning it off restores the previous behaviour, and it has no effect at "Ticks per level" 1, where no cluster is ever truncated (#130).

## Bug Fixes

- **mzMarketDepth: one very large level no longer hides all the others in the Historical DOM.**
- **mzMarketDepth: extremal levels are painted with their own colour in the Heatmap and GrayScaleHeatmap modes.**
- **mzMarketDepth: the Heatmap and GrayScaleHeatmap colour modes no longer wash every level out to a single colour.**
- **mzMarketDepth: the descriptions of "Display volume, %" and "Extreme volume, %" say what the percentage is a share of.**
- **mzMarketDepth: liquidity migration is drawn on levels filtered out by "Display volume".**
- **mzMarketDepth: a switched-off liquidity group no longer leaves its settings in the property grid.**

## Compatibility

- NinjaTrader 8.0.27+
