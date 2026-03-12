---
sidebar_position: 3
title: "Sound Files"
description: "Alert sound files installed by MZpack and how to add custom sounds in NinjaTrader 8"
---

# Sound Files

MZpack indicators use WAV sound files to play audible alerts when configured thresholds are crossed. Alerts appear in the NinjaTrader **Alert Log** window.

## Sound File Location

All alert sound files are stored in:

```
C:\Program Files\NinjaTrader 8\sounds\
```

The MZpack installer places the following files in this folder automatically.

## Pre-installed Sound Files

| Sound file | Used by | Purpose |
|---|---|---|
| `absorption.wav` | [mzFootprint](../indicators/mzFootprint.md) | Absorption alert |
| `absorption_resistance_zone.wav` | [mzFootprint](../indicators/mzFootprint.md) | Absorption resistance S/R zone alert |
| `absorption_support_zone.wav` | [mzFootprint](../indicators/mzFootprint.md) | Absorption support S/R zone alert |
| `aggressive.wav` | [mzBigTrade](../indicators/mzBigTrade.md) | Aggressive trade alert |
| `beep.wav` | — | General purpose |
| `bigtrade.wav` | [mzBigTrade](../indicators/mzBigTrade.md) | Buy/Sell trade alerts |
| `buy.wav` | [mzBigTrade](../indicators/mzBigTrade.md) | Buy trade alert |
| `crossed.wav` | [mzVolumeProfile](../indicators/mzVolumeProfile.md) | Level crossing alert |
| `ding.wav` | [mzMarketDepth](../indicators/mzMarketDepth.md) | Extreme volume alert |
| `dong.wav` | — | General purpose |
| `iceberg.wav` | [mzVolumeDelta](../indicators/mzVolumeDelta.md) | Iceberg alert |
| `imbalance.wav` | [mzFootprint](../indicators/mzFootprint.md) | Imbalance alert |
| `imbalance_resistance_zone.wav` | [mzFootprint](../indicators/mzFootprint.md) | Imbalance resistance S/R zone alert |
| `imbalance_support_zone.wav` | [mzFootprint](../indicators/mzFootprint.md) | Imbalance support S/R zone alert |
| `mzpack_alert1.wav` | [mzVolumeDelta](../indicators/mzVolumeDelta.md) | Bar Delta alert |
| `mzpack_alert2.wav` | [mzVolumeDelta](../indicators/mzVolumeDelta.md), [mzDeltaDivergence](../indicators/mzDeltaDivergence.md) | Volume alert, Divergence alert |
| `mzpack_alert3.wav` | — | General purpose |
| `mzpack_alert4.wav` | — | General purpose |
| `mzpack_alert5.wav` | — | General purpose |
| `mzpack_alert6.wav` | — | General purpose |
| `mzpack_alert7.wav` | — | General purpose |
| `mzpack_alert8.wav` | — | General purpose |
| `pushing_ask.wav` | [mzMarketDepth](../indicators/mzMarketDepth.md) | Ask-side pushing alert |
| `pushing_bid.wav` | [mzMarketDepth](../indicators/mzMarketDepth.md) | Bid-side pushing alert |
| `sell.wav` | [mzBigTrade](../indicators/mzBigTrade.md) | Sell trade alert |
| `strong_buy.wav` | [mzBigTrade](../indicators/mzBigTrade.md) | Strong buy trade alert |
| `strong_sell.wav` | [mzBigTrade](../indicators/mzBigTrade.md) | Strong sell trade alert |
| `sweep.wav` | [mzBigTrade](../indicators/mzBigTrade.md) | Sweep trade alert |
| `touched.wav` | [mzVolumeProfile](../indicators/mzVolumeProfile.md) | Level touched alert |

## Custom Sound Files

To use your own alert sounds:

1. Place a `.wav` file in `C:\Program Files\NinjaTrader 8\sounds\`.
2. In the indicator's alert **Sound** property, type the filename (e.g., `my_alert.wav`).

The file must be in standard WAV format. MP3 and other audio formats are not supported.
