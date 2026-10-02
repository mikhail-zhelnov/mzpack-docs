---
sidebar_position: 1
title: "MZpack AI Skill"
description: "Portable Agent Skill for creating NinjaTrader 8 strategies with the MZpack Strategies API."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MZpack AI Skill

## What Is MZpack AI Skill

MZpack AI Skill is a portable, versioned Agent Skill that gives AI agents the correct context for creating NinjaTrader 8 strategies with the MZpack Strategies API.

It includes the API surface, 16 worked examples, three buildable templates, and common pitfalls. It requires MZpack Strategies or Full Suite: the corpus does not compile with the Indicators-only package.

## Compatibility

| Component | Version or Requirement |
| --- | --- |
| MZpack AI Skill | 1.0.2 |
| Strategies API | 2.4.17 |
| Platform | NinjaTrader 8 |
| Runtime | .NET Framework 4.8 |
| Language | C# 7.3 |
| Build | MSBuild |

## Installation

Download the [MZpack AI Skill ZIP](https://github.com/mikhail-zhelnov/mzpack-strategy-corpus/releases/latest/download/mzpack-ai-skill.zip) and extract its contents into your agent's skill directory. After extraction, `SKILL.md` must be directly inside the `mzpack-strategies` directory.

<Tabs>
<TabItem value="codex" label="Codex" default>

```powershell
$skillZip = Join-Path $env:TEMP 'mzpack-ai-skill.zip'
Invoke-WebRequest -Uri 'https://github.com/mikhail-zhelnov/mzpack-strategy-corpus/releases/latest/download/mzpack-ai-skill.zip' -OutFile $skillZip
New-Item -ItemType Directory -Force .codex\skills\mzpack-strategies | Out-Null
Expand-Archive -Path $skillZip -DestinationPath .codex\skills\mzpack-strategies -Force
```

</TabItem>
<TabItem value="claude-code" label="Claude Code">

```powershell
$skillZip = Join-Path $env:TEMP 'mzpack-ai-skill.zip'
Invoke-WebRequest -Uri 'https://github.com/mikhail-zhelnov/mzpack-strategy-corpus/releases/latest/download/mzpack-ai-skill.zip' -OutFile $skillZip
New-Item -ItemType Directory -Force .claude\skills\mzpack-strategies | Out-Null
Expand-Archive -Path $skillZip -DestinationPath .claude\skills\mzpack-strategies -Force
```

</TabItem>
<TabItem value="cursor" label="Cursor">

```powershell
$skillZip = Join-Path $env:TEMP 'mzpack-ai-skill.zip'
Invoke-WebRequest -Uri 'https://github.com/mikhail-zhelnov/mzpack-strategy-corpus/releases/latest/download/mzpack-ai-skill.zip' -OutFile $skillZip
New-Item -ItemType Directory -Force .cursor\skills\mzpack-strategies | Out-Null
Expand-Archive -Path $skillZip -DestinationPath .cursor\skills\mzpack-strategies -Force
```

</TabItem>
</Tabs>

## First Step

After installation, open your agent and give it this task:

```text
add a delta divergence signal to this strategy, following AGENTS.md
```

## What Is Included

| Path | Contents |
| --- | --- |
| `AGENTS.md` | Start here. How an MZpack strategy is put together: host, algo class, signals, the signal tree, entries, risk, the signal probe, build, and deploy. |
| `docs/api-surface.md` | Types, members, and enums for `MZpack.NT8.Algo` in one place. |
| `docs/pitfalls.md` | Reasons code can compile but do nothing; read this before debugging. |
| `docs/catalog.md` | Which sample to open for a given pattern. |
| `samples/` | 16 worked examples, one technique per example, each with a README. |
| `templates/` | Three buildable templates: plain strategy, Pattern Dashboard, and Control Panel. |
| `Directory.Build.props` | Central paths to NinjaTrader and MZpack; edit once or set environment variables. |

<details>
<summary>Build and Configuration</summary>

MSBuild is required. It is already on `PATH` in Developer PowerShell for Visual Studio:

```powershell
msbuild templates\StrategyTemplate\StrategyTemplate.csproj
```

- Build the template, not the corpus root: `samples/` is intentionally not part of a project, and there is nothing to build at the root.
- Close NinjaTrader before building. Otherwise it holds assemblies in `bin\Custom`, and a successful build will not add the strategy to the list.
- For a standard installation, `Directory.Build.props` already contains the required paths. For custom paths, edit that file or set `NINJATRADER_INSTALL`, `NINJATRADER_USER`, and `MZPACK_DLL` as environment variables, then restart your shell or Visual Studio.

</details>

## Links

- [Download the latest MZpack AI Skill ZIP](https://github.com/mikhail-zhelnov/mzpack-strategy-corpus/releases/latest/download/mzpack-ai-skill.zip)
