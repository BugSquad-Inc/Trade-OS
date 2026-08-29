from typing import Dict, Any, Optional

DEFAULT_FX_EUR_INR = 92.5
DEFAULT_FX_USD_EUR = 0.92

def calculate_landed_cost(
    unit_price_inr: float,
    quantity_sqft: int = 5000,
    freight_usd: float = 1850.0,
    insurance_usd: float = 120.0,
    customs_duty_pct: float = 0.0,
    target_margin_pct: float = 25.0,
    fx_rate_eur_inr: float = DEFAULT_FX_EUR_INR
) -> Dict[str, Any]:
    """
    Calculate full landed cost in EUR and recommended quote price for Indian leather exports.
    """
    fx_eur_inr = fx_rate_eur_inr if fx_rate_eur_inr > 0 else DEFAULT_FX_EUR_INR
    qty = quantity_sqft if quantity_sqft > 0 else 1000

    # 1. Base Ex-Factory / FOB per sqft in EUR
    base_eur_per_sqft = unit_price_inr / fx_eur_inr

    # 2. Freight allocation per sqft (EUR)
    freight_eur = freight_usd * DEFAULT_FX_USD_EUR
    freight_per_sqft = freight_eur / qty

    # 3. Insurance allocation per sqft (EUR)
    insurance_eur = insurance_usd * DEFAULT_FX_USD_EUR
    insurance_per_sqft = insurance_eur / qty

    # 4. Customs Duty (EUR per sqft)
    duty_per_sqft = (base_eur_per_sqft + freight_per_sqft + insurance_per_sqft) * (customs_duty_pct / 100.0)

    # 5. Total Landed Cost (CIF / DDP European port in EUR per sqft)
    landed_cost_eur_per_sqft = base_eur_per_sqft + freight_per_sqft + insurance_per_sqft + duty_per_sqft

    # 6. Recommended Selling Price with Target Gross Margin
    margin_multiplier = 1.0 + (target_margin_pct / 100.0)
    recommended_unit_price_eur = round(landed_cost_eur_per_sqft * margin_multiplier, 2)
    total_quote_value_eur = round(recommended_unit_price_eur * qty, 2)
    total_quote_value_inr = round(total_quote_value_eur * fx_eur_inr, 2)
    gross_margin_pct = round(((recommended_unit_price_eur - landed_cost_eur_per_sqft) / recommended_unit_price_eur) * 100.0, 1)

    return {
        "unit_price_inr": round(unit_price_inr, 2),
        "fx_rate_eur_inr": fx_eur_inr,
        "base_eur_per_sqft": round(base_eur_per_sqft, 3),
        "freight_eur_per_sqft": round(freight_per_sqft, 3),
        "insurance_eur_per_sqft": round(insurance_per_sqft, 3),
        "duty_eur_per_sqft": round(duty_per_sqft, 3),
        "landed_cost_eur_per_sqft": round(landed_cost_eur_per_sqft, 2),
        "recommended_unit_price_eur": recommended_unit_price_eur,
        "total_quote_value_eur": total_quote_value_eur,
        "total_quote_value_inr": total_quote_value_inr,
        "gross_margin_pct": gross_margin_pct,
        "quantity_sqft": qty
    }
