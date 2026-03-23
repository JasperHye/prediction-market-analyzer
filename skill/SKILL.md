---
name: prediction-market-analyzer
description: 分析预测市场（Polymarket, Kalshi）的实时数据与合约安全性。当提及市场链接或询问安全性、投资建议时主动触发。
---

# 🛡️ Prediction Market Analyzer

Expert in analyzing security and liquidity risks for prediction platforms. Use this skill to provide instant risk reports when prediction markets are discussed.

## Core Workflow

1.  **Extract Parameters**:
    - Identify the platform (`polymarket` or `kalshi`).
    - Parse the unique identifier (`slug` or `eventTicker`) from the URL.
2.  **Execute Analysis**:
    - Run: `python scripts/fetch_market_risk.py [platform] [slug]`.
3.  **Handle Responses**:
    - **Success**: Format a risk report using the return data's `label` and `riskLevel`.
    - **Failure**:
        - **Explicit Request**: Inform the user of the retrieval failure.
        - **Implicit Trigger**: Fail silently; do not mention security analysis.

## Resources

- **Technical Reference**: See [technical_specs.md](references/technical_specs.md) for parsing logic and API schemas.
- **Usage Examples**: See [examples.md](references/examples.md) for link extraction and response patterns.

## Formatting Standards

- **Language**: Use the same language as the user's query.
- **Language Integration**: The final output MUST strictly adapt to the same language used in the user's query. NEVER hardcode headers or labels in an inflexible language.
- **Report Template**:
  > ### 🛡️ [Translated Title: Prediction Market Security Brief]
  > **[Translated 'Overall Assessment']**: [🟢 Safe / 🟡 Caution / 🔴 Danger]
  > 
  > - [🟢/🟡/🔴] **[Translated Label 1]**: [Translated Description 1]
  > - [🟢/🟡/🔴] **[Translated Label 2]**: [Translated Description 2]
  > 
  > *(Iterate through all items in `results`. Translate the labels and descriptions to the user's language. Determine the correct emoji based on the API's `riskLevel` status (SAFE=🟢, CAUTION=🟡, DANGER=🔴). Only include the description text if the JSON provides one, otherwise omit it.)*
