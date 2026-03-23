# Prediction Market Analyzer (Skill)

[🇨🇳 简体中文](README-zh.md) | [🇬🇧 English](README.md)

An advanced, multi-language AI Skill designed to extract, analyze, and render security assessments and market logic for decentralized prediction markets (e.g., Kalshi, Polymarket). 

## 🌟 What is a "Skill"?
This repository contains a **Skill**—a modular, self-contained package that extends the capabilities of an AI Agent (like Claude, Gemini, etc.). It acts as a specialized procedural "onboarding guide", equipping the general-purpose AI with specific knowledge, scripts, and workflows.

## 🚀 Features

- **Multi-Platform Interception**: Automatically listens for URLs or keywords from platforms like Polymarket and Kalshi.
- **Dynamic Security Analysis**: Executes live data fetching via an Ansuz Security endpoint to evaluate deep metrics like liquidity manipulation, smart contract vulnerability, and betting rule pitfalls.
- **Smart UI Rendering**: Translates dry API numbers into an intuitive, flat, multi-lingual "Action Brief" (🟢 Safe / 🟡 Caution / 🔴 Danger).
- **Stealth Mode for Failures**: Employs elegant error-handling (silent failures for implicit mentions) to ensure it never disrupts the user's primary conversation.

## 📦 How to Use

If your AI system supports `.skill` packaging, simply install this package into your agent's workspace. 

The essential payload is contained directly in the root (under `SKILL.md` and `scripts/`). The AI will autonomously parse the instructions and hook into your conversations when prediction markets are discussed.

---
*Built with [skill-creator](https://github.com/nextlevelbuilder/skill-creator) workflows.*
