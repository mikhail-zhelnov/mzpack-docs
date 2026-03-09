---
sidebar_position: 2
title: "Installation"
description: "Step-by-step guide to installing MZpack indicators and strategies on NinjaTrader 8"
---

# Installation

MZpack is distributed as an installer that places the DLL file into the correct NinjaTrader 8 directory automatically.

## Download

Download the latest MZpack installer from [mzpack.pro](https://mzpack.pro).

Available editions:

| Edition | Description |
|---|---|
| **MZpack Indicators** | All 6 order flow indicators (requires license) |
| **MZpack Strategies** | Strategy framework and API for algorithmic trading (requires license) |
| **MZpack FREE** | Free edition with limited indicator features |
| **MZpack TRIAL** | Full-featured 30-day trial |

## Install

1. Close NinjaTrader 8 if it is running
2. Run the MZpack installer
3. Follow the setup wizard — it will place the DLL in the correct NinjaTrader directory
4. Launch NinjaTrader 8

:::note
If NinjaTrader was open during installation, you must restart it for MZpack to load.
:::

## Verify Installation

1. Open a chart in NinjaTrader 8
2. Right-click on the chart and select **Indicators**
3. Type `mz` in the search box
4. You should see the MZpack indicators listed:
   - **mzFootprint** — Order flow footprint charts
   - **mzVolumeProfile** — Volume profile / TPO analysis
   - **mzVolumeDelta** — Volume delta analysis
   - **mzBigTrade** — Large trade detection
   - **mzMarketDepth** — Level 2 market depth visualization
   - **mzDeltaDivergence** — Delta-price divergence signals

If the indicators appear in the list, installation is complete.

## Update

To update MZpack to a newer version:

1. Close NinjaTrader 8
2. Run the updated installer
3. Restart NinjaTrader 8

Your license and settings are preserved across updates.

## Uninstall

1. Close NinjaTrader 8
2. Open **Settings → Apps → Installed apps** (Windows 11) or **Control Panel → Programs and Features** (Windows 10)
3. Find **MZpack** in the list, click **Uninstall**, and follow the prompts
4. Restart NinjaTrader 8
