<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:0E4C63,100:22C3D8&height=200&section=header&text=Emir%20Furkan%20Sar%C4%B1&fontSize=46&fontColor=E6EDF3&animation=fadeIn&fontAlignY=36&desc=Embedded%20Systems%20%C2%B7%20AI%20Agent%20Tooling&descAlignY=58&descSize=18" alt="Emir Furkan Sarı" width="100%" />

<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&pause=1200&color=22C3D8&center=true&vCenter=true&width=640&lines=I+build+systems+where+AI+agents+do+real+work;Hermes+Agent+%C2%B7+Oh+My+Pi+%C2%B7+Tern;Multi-agent+orchestration+%C2%B7+LLM+memory+%C2%B7+agent+daemons;STM32+firmware+%C2%B7+secure+RF+OTA+%C2%B7+bootloaders" alt="AI agent tooling and embedded firmware" /></a>

[![Website](https://img.shields.io/badge/emirfurkansari.com-0D1117?style=for-the-badge&logo=googlechrome&logoColor=22C3D8)](https://www.emirfurkansari.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0D1117?style=for-the-badge&logo=linkedin&logoColor=0A66C2)](https://www.linkedin.com/in/emirfurkansar%C4%B1/)
[![Email](https://img.shields.io/badge/contact@emirfurkansari.com-0D1117?style=for-the-badge&logo=gmail&logoColor=D14836)](mailto:contact@emirfurkansari.com)
<img src="https://komarev.com/ghpvc/?username=Emirfs&style=for-the-badge&color=0E4C63&label=PROFILE+VIEWS" alt="Profile views" />

</div>

## About me

I design **AI agent systems** and build them on top of real engineering work in **embedded firmware**.
My current tooling centers on **Hermes Agent**, **Oh My Pi** and **Tern**: native agent interfaces,
terminal plugins, multi-provider workflows and persistent LLM memory.
I also build an autonomous GitHub agent daemon and workflows that build, flash and debug STM32 firmware on real hardware.

This page is the portfolio view of that work. Public repositories are linked; private ones are marked.

<div align="center">
<img src="./assets/agents-terminal.svg" alt="Illustrative animation of AI agents working on a firmware project (not captured output)" width="100%" />
<br><sub>Illustrative animation, not captured terminal output.</sub>
</div>

## AI & agent systems

<table>
<tr>
<td width="50%" valign="top">

### [hermes-tern](https://github.com/Emirfs/hermes-tern)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white) ![Public](https://img.shields.io/badge/public-238636?style=flat-square)

Hermes Agent in Tern's native UI. `hermes tern` renders conversations, tool calls, approvals and subagents as real UI components, with resumable sessions, live background-job charts and linked pull requests.

</td>
<td width="50%" valign="top">

### [tern-plugins](https://github.com/Emirfs/tern-plugins)
![Luau](https://img.shields.io/badge/Luau-00A2FF?style=flat-square&logo=lua&logoColor=white) ![Public](https://img.shields.io/badge/public-238636?style=flat-square)

Tern plugins and Oh My Pi extensions: cross-profile account limits, pane profile labels, independent split columns, switchable UI mods, active-account status and versioned artifacts beside the chat.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [conclave](https://github.com/Emirfs/conclave)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white) ![Public](https://img.shields.io/badge/public-238636?style=flat-square)

Local, daemon-first workspace for multiple AI coding providers. Claude Code, Codex, Antigravity and Ollama sessions live as cards on an infinite canvas. Cards relay, review and debate each other's answers, and work keeps running after the UI closes.

</td>
<td width="50%" valign="top">

### ghd
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Private](https://img.shields.io/badge/private-6E7681?style=flat-square)

Autonomous agent daemon that watches my GitHub repository fleet. It connects local AI CLIs to controlled GitHub work: implementing issues, reviewing PRs, fixing review findings, syncing docs and proposing conflict resolutions.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [mnemo](https://github.com/Emirfs/mnemo)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Public](https://img.shields.io/badge/public-238636?style=flat-square)

Persistent, portable, cross-AI memory over a plain Markdown vault. Push-based auto-recall injects relevant past work into the model's context without being asked. Backed by a private vault of my own engineering notes.

</td>
<td width="50%" valign="top">

### [WID — Works In Debug](https://github.com/Emirfs/WID)
![Claude Code](https://img.shields.io/badge/Claude_Code-D97757?style=flat-square&logo=claude&logoColor=white) ![Public](https://img.shields.io/badge/public-238636?style=flat-square)

Claude Code agent system for STM32 development. Agents build, flash and debug on real hardware. My RF firmware-update work, including [FirmwareUpdate_RF](https://github.com/Emirfs/FirmwareUpdate_RF), was developed and tested with it.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [multi-ai-manager](https://github.com/Emirfs/multi-ai-manager)
![Electron](https://img.shields.io/badge/Electron-47848F?style=flat-square&logo=electron&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) ![Public](https://img.shields.io/badge/public-238636?style=flat-square)

Desktop control panel for Claude, Codex, Gemini, Ollama and Mistral CLIs. Task queue with dependencies, approvals, shared memory, agent profiles, and token and cost estimates.

</td>
<td width="50%" valign="top">

### [opus-5-5-playbook](https://github.com/Emirfs/opus-5-5-playbook)
![Markdown](https://img.shields.io/badge/Rules_%26_Skills-0D1117?style=flat-square&logo=markdown&logoColor=white) ![Public](https://img.shields.io/badge/public-238636?style=flat-square)

Agent rule and prompting skill for Claude Opus 5.5, derived from the official guide. Works with Oh My Pi, Claude Code and Cursor.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### [ai-news-hub — Neural Pulse](https://github.com/Emirfs/ai-news-hub)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Public](https://img.shields.io/badge/public-238636?style=flat-square)

Autonomous AI and frontier-tech journal. Hourly dispatches, trending open-source models and multi-language briefings, produced without manual editing.

</td>
</tr>
</table>

## AI usage

Recorded usage by model vendor, including **Hermes Agent** and every **Oh My Pi** profile. Refreshed every 3 hours.

<div align="center">
<img src="https://raw.githubusercontent.com/Emirfs/Emirfs/main/assets/ai-usage.svg?v=20261118" alt="Recorded AI token usage by model vendor, from Tokscale submissions of all local agent logs" width="100%" />
</div>

<details>
<summary>Sources &amp; counting</summary>

- [Tokscale submissions](https://tokscale.ai/u/Emirfs) from my machine every 3 hours, scanning every Oh My Pi profile and the session backup of retired ones.
- Submitted day totals never decrease, so usage stays counted after its local logs are deleted.
- Tokens include cache reads. Cost is the estimated list-price equivalent, not actual spend; some records are unpriced or lack usage events.
- The workflow re-renders the card from the Tokscale API every 3 hours.

</details>

## AI harnesses

<div align="center">

[![Hermes Agent](https://img.shields.io/badge/Hermes_Agent-0D1117?style=for-the-badge&logoColor=E6EDF3)](https://github.com/NousResearch/hermes-agent)
[![Oh My Pi](https://img.shields.io/badge/Oh_My_Pi-0D1117?style=for-the-badge&logoColor=E6EDF3)](https://github.com/can1357/oh-my-pi)
[![Claude Code](https://img.shields.io/badge/Claude_Code-0D1117?style=for-the-badge&logo=claude&logoColor=D97757)](https://code.claude.com/docs/en/overview)
[![Codex CLI](https://img.shields.io/badge/Codex_CLI-0D1117?style=for-the-badge&logo=openai&logoColor=10A37F)](https://github.com/openai/codex)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-0D1117?style=for-the-badge&logo=googlegemini&logoColor=4E8CF7)](https://github.com/google-gemini/gemini-cli)
[![OpenCode](https://img.shields.io/badge/OpenCode-0D1117?style=for-the-badge)](https://github.com/anomalyco/opencode)
[![Antigravity](https://img.shields.io/badge/Antigravity-0D1117?style=for-the-badge)](https://antigravity.google/)

**Workspace:** [Tern](https://stencil.so/tern) · **Local models:** [Ollama](https://ollama.com/)

</div>

## GitHub activity

<div align="center">
<img src="https://streak-stats.demolab.com?user=Emirfs&theme=github-dark-blue&hide_border=true&background=0D1117" alt="GitHub contribution streak" />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Emirfs/Emirfs/output/snake.svg" />
  <img src="https://raw.githubusercontent.com/Emirfs/Emirfs/output/snake.svg" alt="Contribution snake" width="100%" />
</picture>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:22C3D8,50:0E4C63,100:0D1117&height=110&section=footer" alt="" width="100%" />
</div>
