---
sidebar_position: 1
title: "MZpack AI Skill"
description: "Portable Agent Skill for creating NinjaTrader 8 strategies with the MZpack Strategies API."
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# MZpack AI Skill

## Что такое MZpack AI Skill

MZpack AI Skill — переносимый versioned Agent Skill, который даёт AI-агенту корректный контекст для создания стратегий NinjaTrader 8 на MZpack Strategies API.

В него входят API surface, 16 разобранных примеров, три собираемых шаблона и описание распространённых ошибок. Для работы требуется MZpack Strategies или Full Suite: с пакетом Indicators-only corpus не компилируется.

## Совместимость

| Компонент | Версия или требование |
| --- | --- |
| MZpack AI Skill | 1.0.2 |
| Strategies API | 2.4.17 |
| Платформа | NinjaTrader 8 |
| Runtime | .NET Framework 4.8 |
| Язык | C# 7.3 |
| Сборка | MSBuild |

## Установка

Из корня проекта стратегии установите фиксированный релиз `skill-v1.0.2` в каталог навыков вашего агента.

<Tabs>
<TabItem value="codex" label="Codex" default>

```powershell
git clone --branch skill-v1.0.2 --depth 1 https://github.com/mikhail-zhelnov/mzpack-strategy-corpus.git .codex\skills\mzpack-strategies
```

</TabItem>
<TabItem value="claude-code" label="Claude Code">

```powershell
New-Item -ItemType Directory -Force .claude\skills | Out-Null
git clone --branch skill-v1.0.2 --depth 1 https://github.com/mikhail-zhelnov/mzpack-strategy-corpus.git .claude\skills\mzpack-strategies
```

</TabItem>
<TabItem value="cursor" label="Cursor">

```powershell
New-Item -ItemType Directory -Force .cursor\skills | Out-Null
git clone --branch skill-v1.0.2 --depth 1 https://github.com/mikhail-zhelnov/mzpack-strategy-corpus.git .cursor\skills\mzpack-strategies
```

</TabItem>
</Tabs>

## Первый шаг

После установки откройте агента и дайте ему задачу:

```text
add a delta divergence signal to this strategy, following AGENTS.md
```

## Что находится внутри

| Путь | Содержание |
| --- | --- |
| `AGENTS.md` | С чего начать: устройство стратегии MZpack — host, algo class, signals, дерево сигналов, entries, risk, signal probe, сборка и deploy. |
| `docs/api-surface.md` | Типы, члены и перечисления `MZpack.NT8.Algo` в одном месте. |
| `docs/pitfalls.md` | Причины, по которым код компилируется, но ничего не делает; прочитайте перед отладкой. |
| `docs/catalog.md` | Какой пример открыть для нужного паттерна. |
| `samples/` | 16 разобранных примеров: по одной технике на пример, с README. |
| `templates/` | Три собираемых шаблона: plain strategy, Pattern Dashboard и Control Panel. |
| `Directory.Build.props` | Центральные пути к NinjaTrader и MZpack: измените один раз или задайте переменные окружения. |

<details>
<summary>Сборка и настройка</summary>

Для сборки нужен MSBuild. В Developer PowerShell for VS он уже находится в `PATH`:

```powershell
msbuild templates\StrategyTemplate\StrategyTemplate.csproj
```

- Собирайте шаблон, а не корень corpus: `samples/` намеренно не включён в проект, а в корне нечего собирать.
- Перед сборкой закройте NinjaTrader. Иначе он удерживает assemblies в `bin\Custom`, и успешная сборка не добавит стратегию в список.
- При стандартной установке `Directory.Build.props` уже содержит нужные пути. Для нестандартных путей измените этот файл либо задайте `NINJATRADER_INSTALL`, `NINJATRADER_USER` и `MZPACK_DLL` как переменные окружения; затем закройте и откройте shell или Visual Studio.

</details>

## Ссылки

- [Исходники фиксированного релиза](https://github.com/mikhail-zhelnov/mzpack-strategy-corpus/tree/skill-v1.0.2)
- [ZIP фиксированного релиза](https://github.com/mikhail-zhelnov/mzpack-strategy-corpus/archive/refs/tags/skill-v1.0.2.zip)
