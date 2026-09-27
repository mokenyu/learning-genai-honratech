# Mini-Specification: Cross-Border Treasury & FX Fee Auditor Agent

**Version:** 1.0.0  
**Domain:** Enterprise Fintech & Sovereign Treasury Automation  
**Author:** Honra Tech GenAI Curriculum Engineering  
**Target Architecture:** LangChain ReAct Autonomous Agent (`gemini-3.6-flash`)

---

## 1. Objective & Scenario
An enterprise treasury team needs an autonomous agent to evaluate cross-border capital transfers. The agent ingests corporate transfer requests, checks foreign exchange (FX) spot and volatility rates, calculates mandatory tiered regulatory and transaction fees, and generates a certified audit advisory recommendation.

---

## 2. Input Contract (JSON / Pydantic Schema)
The agent accepts an input payload with the following strict contract:

```json
{
  "client_name": "string (min_length=2, max_length=100, e.g., 'Honra Global Logistics')",
  "source_amount_usd": "float (must be strictly > 0, e.g., 250000.00)",
  "target_currency": "string (enum: ['EUR', 'GBP', 'JPY', 'CAD'])",
  "corporate_tier": "string (enum: ['Standard', 'Gold', 'Platinum'], default='Standard')",
  "urgency": "string (enum: ['standard', 'expedited', 'overnight'], default='standard')"
}
```

---

## 3. Tool Specifications
The agent must only use the following registered tools to execute calculations:

### Tool 1: `fetch_live_fx_quote(target_currency: str) -> str`
- **Description:** Returns the live mid-market exchange rate, spread in basis points, and current 24h market volatility index.
- **Input Argument:** `target_currency` (string, uppercase).
- **Output:** Formatted string containing `spot_rate`, `spread_bps`, and `volatility_rating`.
- **Error Condition:** Raises `ToolException` if `target_currency` is not supported.

### Tool 2: `calculate_tiered_compliance_fee(amount_usd: float, corporate_tier: str, urgency: str) -> str`
- **Description:** Calculates the exact compliance, wire, and clearing fees based on account tier and transfer urgency.
- **Input Arguments:** `amount_usd` (float), `corporate_tier` (string), `urgency` (string).
- **Rules:**
  - Base fee: 0.35% for Standard, 0.20% for Gold, 0.10% for Platinum.
  - Urgency surcharge: `standard` = +$0, `expedited` = +$150, `overnight` = +$350.
  - Minimum fee: $50.00 regardless of percentage.
- **Output:** Formatted string with `base_fee_usd`, `urgency_surcharge_usd`, and `total_fee_usd`.

---

## 4. Business & Reasoning Rules
1. **Tool Invocation Order:** The agent must ALWAYS invoke `fetch_live_fx_quote` first, followed by `calculate_tiered_compliance_fee`. It must not estimate numbers mathematically without tool confirmation.
2. **Gross vs. Net Calculation:**
   $$\text{Net USD Converted} = \text{source\_amount\_usd} - \text{total\_fee\_usd}$$
   $$\text{Gross Target Currency} = \text{Net USD Converted} \times \text{spot\_rate}$$
3. **Execution Window Advisory:**
   - If `volatility_rating` is `HIGH`, recommend staggering execution in 2 equal tranches.
   - If `volatility_rating` is `LOW` or `MODERATE`, recommend executing immediately.
4. **Zero-Hallucination Policy:** If any tool fails or returns an error, the agent must report the error directly in the final answer without fabricating numerical rates.

---

## 5. Expected Output Contract
The agent's final answer must strictly adhere to the following Markdown format:

```markdown
### Treasury Transfer Audit & Settlement Recommendation

- **Client Name:** [Client Name] ([Corporate Tier] Tier)
- **Source Capital:** $[amount] USD (Urgency: [Urgency])
- **Target Currency:** [Currency] @ Spot Rate [Rate]
- **Fee Breakdown:**
  - Base Fee: $[Amount] USD
  - Urgency Surcharge: $[Amount] USD
  - Total Settlement Fee: $[Amount] USD
- **Net Converted Total:** [Net Total] [Currency]
- **Risk & Timing Advisory:** [Stagger / Immediate Recommendation based on volatility]
- **Audit Certification:** Certified by Autonomous Treasury Agent [Timestamp / ID]
```

---

## 6. Verification & Acceptance Criteria
- [ ] Accepts validated input payload without throwing schema validation errors.
- [ ] Calls both tools with correct parameters.
- [ ] Accurately subtracts fees from principal before FX conversion.
- [ ] Returns structured markdown matching the exact output template.
