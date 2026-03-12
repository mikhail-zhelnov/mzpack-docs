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
| `mzpack_alert1.wav` | [mzVolumeDelta](../indicators/mzVolumeDelta.md) | Bar Delta alert |
| `mzpack_alert2.wav` | [mzVolumeDelta](../indicators/mzVolumeDelta.md), [mzDeltaDivergence](../indicators/mzDeltaDivergence.md) | Volume alert, Divergence alert |
| `mzpack_alert3.wav` | — | General purpose |
| `mzpack_alert4.wav` | — | General purpose |
| `mzpack_alert5.wav` | — | General purpose |
| `mzpack_alert6.wav` | — | General purpose |
| `mzpack_alert7.wav` | — | General purpose |
| `mzpack_alert8.wav` | — | General purpose |
| `bigtrade.wav` | [mzBigTrade](../indicators/mzBigTrade.md) | Buy/Sell trade alerts |
| `iceberg.wav` | [mzVolumeDelta](../indicators/mzVolumeDelta.md) | Iceberg alert |
| `ding.wav` | [mzMarketDepth](../indicators/mzMarketDepth.md) | Extreme volume alert |
| `crossed.wav` | [mzVolumeProfile](../indicators/mzVolumeProfile.md) | Level crossing alert |

## Custom Sound Files

To use your own alert sounds:

1. Place a `.wav` file in `C:\Program Files\NinjaTrader 8\sounds\`.
2. In the indicator's alert **Sound** property, type the filename (e.g., `my_alert.wav`).

The file must be in standard WAV format. MP3 and other audio formats are not supported.
