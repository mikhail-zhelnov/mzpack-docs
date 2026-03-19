# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is documentation (user guide and API reference) for MZpack - a proprietary algorithmic trading indicator and strategy framework for **NinjaTrader 8**. It provides order flow analysis, volume profiling, machine learning integration, and automated strategy execution.

## Tech Stack of MZpack

- .NET Framework 4.8 (not .NET Core/5+)
- NinjaTrader 8 API (NinjaTrader.Cbi, NinjaTrader.NinjaScript, etc.)
- Windows only, MSBuild via Visual Studio 2022
- C# 13 with NinjaTrader 8.6.1+

## Tech Stack of this project

- Docusaurus v3, TypeScript

## Source of Truth
Always search for product information in `/home/mikhail/mzpack-docs/user-guide/ug.md` first before writing or editing documentation content.

## MZpack code repo

- /mikhail/mzpack/repo/MZpackBase
- /mikhail/mzpack/repo/MZpack.NT8

## MZpack API samples source code and extensions

- /mikhail/mzpack/repo/MZpack.NT8/Algo/Samples/Built-in
- /mikhail/mzpack/repo/MZpack.NT8/Algo/Extensions

## MZpack built-in strategies source code

- /mikhail/mzpack/repo/MZpack.NT8/Algo/Strategies
