"""
Honra Tech - Spec-Driven Development (SDD)
Implementation File: skeleton_agent.py
Fulfills Specification: mini-spec-sample.md (Cross-Border Treasury & FX Fee Auditor Agent)

Architecture:
- LangChain ReAct Reasoning Loop (create_agent)
- LLM: Google Gemini (gemini-3.6-flash)
- Strict Pydantic Data Contracts for Input Validation
- Production Tool Wrappers with Error Trapping (handle_tool_error=True)
"""

import os
import sys
from typing import Literal, Optional, Any, Dict
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv

from langchain_core.tools import tool, ToolException
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent


# =====================================================================
# 1. Pydantic Data Contracts & Schemas (Section 2 of Spec)
# =====================================================================

class TransferRequest(BaseModel):
    """Input contract conforming strictly to mini-spec-sample.md"""
    client_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full legal name of the corporate entity initiating transfer."
    )
    source_amount_usd: float = Field(
        ...,
        gt=0.0,
        description="Total source capital in USD to be transferred (must be > 0)."
    )
    target_currency: Literal["EUR", "GBP", "JPY", "CAD"] = Field(
        ...,
        description="Target currency code."
    )
    corporate_tier: Literal["Standard", "Gold", "Platinum"] = Field(
        default="Standard",
        description="Client corporate account classification tier."
    )
    urgency: Literal["standard", "expedited", "overnight"] = Field(
        default="standard",
        description="Settlement speed priority."
    )


# =====================================================================
# 2. Tool Implementations (Section 3 of Spec)
# =====================================================================

@tool
def fetch_live_fx_quote(target_currency: str) -> str:
    """
    Returns live mid-market exchange rate, spread in basis points, and current 24h market volatility index.
    Supported currencies: EUR, GBP, JPY, CAD.
    """
    currency_code = target_currency.strip().upper()
    rates_database = {
        "EUR": {"spot_rate": 0.9215, "spread_bps": 1.2, "volatility": "LOW"},
        "GBP": {"spot_rate": 0.7850, "spread_bps": 1.5, "volatility": "MODERATE"},
        "JPY": {"spot_rate": 154.20, "spread_bps": 2.8, "volatility": "HIGH"},
        "CAD": {"spot_rate": 1.3620, "spread_bps": 1.4, "volatility": "LOW"}
    }

    if currency_code not in rates_database:
        raise ToolException(
            f"UnsupportedCurrencyError: Currency '{currency_code}' is not supported. "
            f"Supported options: {list(rates_database.keys())}"
        )

    quote = rates_database[currency_code]
    return (
        f"FX Quote [{currency_code}] -> Spot Rate: {quote['spot_rate']} | "
        f"Spread: {quote['spread_bps']} bps | Volatility Rating: {quote['volatility']}"
    )

# Attach error trapping handler
fetch_live_fx_quote.handle_tool_error = True


@tool
def calculate_tiered_compliance_fee(amount_usd: float, corporate_tier: str, urgency: str) -> str:
    """
    Calculates exact compliance, wire, and clearing fees based on account tier and transfer urgency.
    """
    if amount_usd <= 0:
        raise ToolException("ValidationError: Transfer amount must be greater than zero.")

    tier_clean = corporate_tier.strip().capitalize()
    urgency_clean = urgency.strip().lower()

    # Tiered base percentage
    rate_table = {
        "Standard": 0.0035,  # 0.35%
        "Gold": 0.0020,      # 0.20%
        "Platinum": 0.0010   # 0.10%
    }
    pct = rate_table.get(tier_clean, 0.0035)
    base_fee = max(50.0, amount_usd * pct)  # Minimum fee of $50.00

    # Urgency surcharge
    surcharge_table = {
        "standard": 0.0,
        "expedited": 150.0,
        "overnight": 350.0
    }
    urgency_surcharge = surcharge_table.get(urgency_clean, 0.0)
    total_fee = base_fee + urgency_surcharge

    return (
        f"Fee Calculation -> Base Fee: ${base_fee:,.2f} USD ({pct*100:.2f}%) | "
        f"Urgency Surcharge: ${urgency_surcharge:,.2f} USD ({urgency_clean}) | "
        f"Total Fee: ${total_fee:,.2f} USD"
    )

# Attach error trapping handler
calculate_tiered_compliance_fee.handle_tool_error = True


# =====================================================================
# 3. Agent ReAct Prompt with Strict Guardrails (Section 4 & 5 of Spec)
# =====================================================================

TREASURY_AGENT_PROMPT = """You are the Senior Cross-Border Treasury & FX Fee Auditor Agent at Honra Capital.
Your objective is to evaluate corporate capital transfers according to strict financial compliance rules.

You have access to two tools:
1. `fetch_live_fx_quote`: Retrieves spot FX exchange rate and volatility rating.
2. `calculate_tiered_compliance_fee`: Calculates tiered platform fee and urgency surcharge.

RULES OF ENGAGEMENT:
1. Tool Invocation Order: You MUST first invoke `fetch_live_fx_quote` for the target currency. Next, invoke `calculate_tiered_compliance_fee`.
2. Mathematical Integrity:
   - Net USD Converted = (source_amount_usd - Total Fee)
   - Gross Target Currency = (Net USD Converted) * (spot_rate)
   Do NOT estimate or round roughly; calculate precisely using the tool values.
3. Timing Advisory:
   - If Volatility Rating is HIGH: recommend staggering execution across 2 equal tranches to mitigate slippage.
   - If Volatility Rating is LOW or MODERATE: recommend immediate single-block execution.
4. Final Answer Formatting: Output MUST strictly match the exact Markdown format below with NO extraneous conversational banter.

Required Markdown Output Format:
### Treasury Transfer Audit & Settlement Recommendation

- **Client Name:** [Client Name] ([Corporate Tier] Tier)
- **Source Capital:** $[Amount] USD (Urgency: [Urgency])
- **Target Currency:** [Currency] @ Spot Rate [Rate]
- **Fee Breakdown:**
  - Base Fee: $[Amount] USD
  - Urgency Surcharge: $[Amount] USD
  - Total Settlement Fee: $[Amount] USD
- **Net Converted Total:** [Net Total] [Currency]
- **Risk & Timing Advisory:** [Stagger / Immediate Recommendation based on volatility]
- **Audit Certification:** Certified by Autonomous Treasury Agent [ID: HONRA-TR-2026]"""


# =====================================================================
# 4. Agent Assembly & Execution Factory
# =====================================================================

def build_treasury_agent(llm: Optional[ChatGoogleGenerativeAI] = None):
    """Builds and returns the configured ReAct Agent using modern create_agent."""
    if llm is None:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY is required to initialize agent.")
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            temperature=0.0,
            api_key=api_key
        )

    tools = [fetch_live_fx_quote, calculate_tiered_compliance_fee]
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=TREASURY_AGENT_PROMPT
    )
    return agent


def run_audit(payload: dict) -> str:
    """
    Validates input payload against TransferRequest contract and invokes Treasury Agent.
    """
    try:
        # Step 1: Strict Input Contract Validation
        validated_request = TransferRequest(**payload)
        print(f"[SDD Validation Passed] Client: {validated_request.client_name} | Amount: ${validated_request.source_amount_usd:,.2f}")
    except ValidationError as e:
        print(f"[SDD Contract Error] Payload violates input schema:\n{e}")
        return f"Error: Input payload schema violation:\n{e}"

    # Step 2: Format Agent Prompt Query
    query = (
        f"Audit and calculate cross-border settlement for client '{validated_request.client_name}'. "
        f"Source Capital: ${validated_request.source_amount_usd:,.2f} USD. "
        f"Target Currency: {validated_request.target_currency}. "
        f"Corporate Tier: {validated_request.corporate_tier}. "
        f"Urgency: {validated_request.urgency}."
    )

    # Step 3: Execute ReAct Agent Loop
    agent = build_treasury_agent()
    result = agent.invoke({"messages": [("user", query)]})
    messages = result.get("messages", [])
    last_msg = messages[-1] if messages else None

    if last_msg:
        if isinstance(last_msg.content, list):
            parts = [item.get("text", "") for item in last_msg.content if isinstance(item, dict) and "text" in item]
            return "".join(parts) if parts else str(last_msg.content)
        return str(last_msg.content)
    return "No output generated."


# =====================================================================
# 5. CLI Execution & Test Harness
# =====================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Honra Tech - Spec-Driven Development (SDD): Treasury Agent Skeleton")
    print("=" * 70)

    # Test Payload 1: High Volatility JPY Transfer with Expedited Urgency
    sample_payload = {
        "client_name": "Honra Sovereign Logistics Corp",
        "source_amount_usd": 750000.0,
        "target_currency": "JPY",
        "corporate_tier": "Platinum",
        "urgency": "expedited"
    }

    print("\n[Executing Sample Scenario from Spec]")
    output = run_audit(sample_payload)
    print("\n" + "=" * 70)
    print("FINAL AGENT OUTPUT DELIVERABLE:")
    print("=" * 70)
    print(output)
