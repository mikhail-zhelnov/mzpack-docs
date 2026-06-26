---
sidebar_position: 6
title: "Troubleshooting"
description: "Common issues and solutions for MZpack installation, licensing, and indicator configuration"
---

# Troubleshooting

Solutions to common issues with MZpack indicators for NinjaTrader 8.

## Download Issues

### Download fails or shows an error after entering license key

There are several possible causes:

1. **Typo or extra spaces in the license key** — use copy/paste to enter the key instead of typing it manually.
2. **Wrong product selected** — MZpack Indicators, MZpack Indicators w/ Divergence, and MZpack Single Indicators are different products. Make sure you select the one that matches your purchase.
3. **Expired subscription** — check your subscription status at [mzpack.pro](https://mzpack.pro) under **My Profile → Account → Orders**.
4. **Not logged in** — you must be logged in with the account used for purchase to see download links.

## Installation Issues

### Indicators don't appear in NinjaTrader after installation

Work through this checklist:

1. Was NinjaTrader 8 closed during installation? If not, close and restart it.
2. Open the Indicators dialog, type `mz` in the search box, and look under the **MZpack/NT8** folder.
3. If the indicators still don't appear, uninstall MZpack and reinstall.

See [Installation — Verify](getting-started/installation.md#verify-installation) for more details.

### NinjaTrader shows errors on startup after update

This usually happens when old and new versions conflict. To resolve:

1. Close NinjaTrader 8
2. Uninstall the old version via **Settings → Apps → Installed apps** (Windows 11) or **Control Panel → Programs and Features** (Windows 10)
3. Install the new version with the latest installer
4. Restart NinjaTrader 8

See [Installation — Update](getting-started/installation.md#update) for the standard update procedure.

## License Issues

### Activation fails

See [Licensing — Activation Fails](getting-started/licensing.md#activation-fails) for the full checklist, which covers internet connectivity, firewall settings, retry steps, and contacting support.

### Common license error messages

See [Licensing — Common License Errors](getting-started/licensing.md#common-license-errors) for a table of error messages with causes and solutions.

### License key not received after purchase

License keys are sent within the next business day, usually within 3–5 hours.

1. Check your spam, junk, and promotions folders.
2. Some mail servers block messages from unknown senders — adjust your spam policy or provide an alternative email address (e.g., Gmail).
3. If you still haven't received your key, contact support at [mzpack.pro](https://mzpack.pro).

## Data and Indicator Issues

### Footprint shows no data or all zeros

Common causes:

1. **Tick Replay not enabled** — MZpack processes historical data using NinjaTrader's Tick Replay feature. Enable it in your Data Series settings. See [Order Flow — Data Levels](concepts/order-flow.md#data-levels) for details.
2. **No tick data available** — make sure your data feed provides Level 1 (tick) data for the instrument you're charting.
3. **Calculation mode mismatch** — the default BidAsk mode requires bid/ask data in the tick stream. For instruments where this isn't available (e.g., Forex, crypto), use UpDownTick mode. For mixed scenarios, use Hybrid mode. See [Indicators Overview — Calculation Modes](indicators/overview.md#order-flow-calculation-modes) for guidance.

### Historical data looks different from real-time

Without Tick Replay enabled, historical bars lack the tick-by-tick detail needed for accurate order flow reconstruction. Enable Tick Replay in your Data Series settings for consistent results between historical and real-time data.

Some features — such as iceberg detection and DOM pressure — require live data because NinjaTrader does not provide historical Level 2 data. These features will always show data only for bars built in real time.

### File access errors or missing tick data (OneDrive / cloud-synced folders)

If you see errors like `System.IO.IOException: The process cannot access the file '...db\tick\...ncd' because it is being used by another process` or "Unable to save data," your NinjaTrader 8 data folder is most likely inside a OneDrive-synced folder.

By default NinjaTrader stores its database under `Documents\NinjaTrader 8`. If Windows has redirected your **Documents** folder into OneDrive, NinjaTrader deletes and rewrites `.ncd` files every time it saves market data — while OneDrive is holding the same files open for syncing. The two processes collide, the save fails, and tick data can be left incomplete or corrupted.

This is **not an MZpack issue**. NinjaTrader does not support running its database from cloud-synced folders (OneDrive, Dropbox, Google Drive) for this reason. It also directly affects backtesting: MZpack strategies require Tick Replay with downloaded tick data (see [Footprint shows no data](#footprint-shows-no-data-or-all-zeros) above), and if those `.ncd` files can't be saved, backtests may return no trades or unreliable results.

**How to fix it:**

1. **Recommended — move Documents out of OneDrive.** Open **OneDrive → Settings → Backup / Manage backup** and turn off backup for the **Documents** folder. Windows returns Documents to your local profile (`C:\Users\<you>\Documents`) and NinjaTrader runs locally.
2. **Or exclude only NinjaTrader from syncing.** If you want to keep Documents in OneDrive, open **OneDrive → Settings → Account → Choose folders** and uncheck `Documents\NinjaTrader 8`.

After either change, restart NinjaTrader, confirm it is reading from the local (non-OneDrive) folder, and re-download tick data for the instruments and dates you backtest, since some data may not have been saved while the conflict was active.

## Getting Help

If you can't resolve your issue with the steps above, contact support via the helpdesk at [mzpack.pro](https://mzpack.pro).

To help the support team diagnose your problem quickly, include:

- Indicator name and version
- NinjaTrader 8 version
- Your license key
- A screenshot of the issue or the NinjaTrader log file
