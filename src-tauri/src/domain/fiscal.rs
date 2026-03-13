#[derive(Debug, Clone, Copy, PartialEq)]
pub struct VatBreakdown {
    pub base: f64,
    pub vat_amount: f64,
    pub total: f64,
}

pub fn line_totals(
    quantity: f64,
    unit_price: f64,
    discount_pct: f64,
    vat_rate_pct: f64,
) -> VatBreakdown {
    let gross = quantity * unit_price;
    let discount = gross * (discount_pct / 100.0);
    let base = round2(gross - discount);
    let vat_amount = round2(base * (vat_rate_pct / 100.0));
    let total = round2(base + vat_amount);

    VatBreakdown {
        base,
        vat_amount,
        total,
    }
}

pub fn round2(value: f64) -> f64 {
    (value * 100.0).round() / 100.0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn calculates_line_totals_with_discount_and_vat() {
        let res = line_totals(10.0, 12.0, 5.0, 21.0);
        assert_eq!(res.base, 114.0);
        assert_eq!(res.vat_amount, 23.94);
        assert_eq!(res.total, 137.94);
    }
}
