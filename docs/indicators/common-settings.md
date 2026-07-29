---
sidebar_position: 8
title: "Common Settings"
description: "Settings shared by all MZpack indicators for NinjaTrader 8 — General, Orderflow, and Levels parameter groups"
---

# Common Settings

Every MZpack indicator inherits three parameter groups from the shared indicator core. They appear in the NinjaTrader properties grid of **mzFootprint**, **mzVolumeProfile**, **mzVolumeDelta**, **mzDeltaDivergence**, **mzBigTrade**, and **mzMarketDepth** alike, so they are documented once here rather than repeated on every page.

Indicator-specific settings are covered on each indicator's own page.

## General

Chart-level behaviour, instrument handling, and on-chart informational elements.

| Setting | Default | Description |
|---|---|---|
| **Show price line** | false | Draw a horizontal line at the current price. Requires **Calculate** to be `OnEachTick` — the indicator resets this to false and shows a message in other modes |
| **Price line** | DimGray, dotted, 1px | Style of the price line |
| **Working time** | false | Restrict the indicator to the time window defined by **Start time** and **Stop time**. Changing this on a loaded chart prompts a script reload |
| **Start time** | 08:30:00 | Beginning of the working-time window (**Working time** must be enabled) |
| **Stop time** | 15:30:00 | End of the working-time window (**Working time** must be enabled) |
| **Crypto force instrument** | false | Treat the instrument as a crypto pair, enabling fractional volume handling. Changing this on a loaded chart prompts a script reload |
| **Non-Crypto volumes divider** | 1 | Divide all displayed volumes of non-crypto instruments by this value, range: 1–∞. Useful for instruments quoted in very large volume units |
| **Crypto decimal places** | 2 | Decimal places used when displaying crypto volumes, range: 1–8 |
| **Smooth render** | false | Enable anti-aliased rendering. Improves appearance at some cost to performance |
| **Hint** | true | Show hint messages on the chart |
| **Warning** | true | Show warning messages on the chart, such as missing Tick Replay |
| **Version** | false | Show MZpack version information on the chart |
| **Small toolbar buttons** | false | Use compact MZpack toolbar buttons. Changing this on a loaded chart prompts a script reload |
| **Log** | true | Write detailed error information to the NinjaScript Output window |

:::note
**Optimize render performance**, **Maximal render time, ms**, and **Refresh delay, ms** also belong to the General group, but each indicator decides whether to expose them. They are documented on the pages of the indicators that do — see [mzFootprint](./mzFootprint.md), [mzVolumeProfile](./mzVolumeProfile.md), [mzBigTrade](./mzBigTrade.md), and [mzMarketDepth](./mzMarketDepth.md).
:::

## Orderflow

How raw tick data is turned into order flow. These settings drive every bid/ask calculation in the indicator.

| Setting | Default | Description |
|---|---|---|
| **Calculation mode** | BidAsk | How trades are classified as buying or selling — `BidAsk`, `UpDownTick`, or `Hybrid`. See [Order Flow Calculation Modes](./overview.md#order-flow-calculation-modes). Changing this on a loaded chart prompts a script reload |
| **Spread trades** | Split | How trades that span the bid/ask spread are handled — `Split` divides the volume between both sides, `LastKnownSide` assigns it to the previously traded side, `Ignore` discards it |
| **Reconstruct tape: enable** | true | Reconstruct individual tick trades into aggregated trades using timestamps and Level 1 (best bid/ask) events. Required for iceberg detection, DOM pressure, and DOM support |
| **Reconstruct tape: timestamps only** | false | Reconstruct using timestamps alone — Level 1 events are ignored, including for live data, and trades sharing a timestamp are merged. Enable to get an exact match between reconstructed historical and reconstructed live data |

:::tip
Timestamps-only mode is the setting to use when [backtesting](../strategies/backtesting.md), because it makes historical and live reconstruction agree. Note that features relying on Level 1 events are unavailable while it is enabled.
:::

## Levels

Interactive horizontal support and resistance levels that can be placed directly on the chart, each with its own alert. Levels are unavailable in the FREE edition.

| Setting | Default | Description |
|---|---|---|
| **Enable** | false | Enable the Levels feature. Must be on before levels can be added to the chart |
| **Support level** | LightGreen, 10px, 25% opacity | Line style for levels acting as support (below price) |
| **Resistance level** | Red, 10px, 25% opacity | Line style for levels acting as resistance (above price) |
| **Value position** | AboveRight | Where the level's price and label are drawn — `Left`, `Right`, `AboveLeft`, `AboveRight`, or `None` |
| **Value/Label color** | LightGray | Color of the level's price value and label text |
| **Value/Label font** | Arial, 10pt | Font of the level's price value and label text |
| **Alert** | true | Enable sound alerts for levels |
| **Alert on** | LevelCross | Event that fires the alert — `LevelTouch` when price reaches the level, `LevelCross` when price crosses it |
| **Rearm** | true | Re-arm the alert after it fires so the same level can alert again |
| **Rearm interval, sec** | 3 | Seconds to wait before a fired alert re-arms, range: 0–∞ |
| **Sound** | crossed.wav | WAV file played when a level alert fires. See [Sound Files](../getting-started/sound-files.md) |
| **Add/remove: Mouse Left +** | LeftShift | Modifier key held with a left click to add or remove a level |
| **Modify: Mouse Left +** | LeftAlt | Modifier key held with a left click to open a level's settings |
| **Drag with Mouse** | true | Allow levels to be repositioned by dragging them with the left mouse button |

### Per-Level Settings

Each level on the chart has its own settings, opened from the level dialog rather than the indicator properties grid. Open it with a left click while holding the **Modify** key.

| Setting | Description |
|---|---|
| **Price** | The level's price. Editing it moves the level and re-arms its alert |
| **Label** | Free-text label drawn next to the level |
| **Color** | Line style for this individual level, overriding the group default |
| **Alarmed** | Read-only timestamp of when this level last alerted, or `Never` |
| **Alert** | Enable the alert for this level |
| **Alert on** | Event that fires this level's alert — `LevelTouch` or `LevelCross` |
| **Direction** | Which crossing direction triggers the alert — `Up`, `Down`, or `UpDown` |
| **Rearm** | Re-arm this level's alert after it fires |
| **Rearm interval, sec** | Seconds before this level's alert re-arms, range: 0–∞ |
| **Sound** | WAV file played for this level |
