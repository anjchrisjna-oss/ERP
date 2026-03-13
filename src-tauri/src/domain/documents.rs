#[derive(Debug, Clone, Copy, PartialEq)]
pub enum DocumentType {
    Quote,
    Order,
    DeliveryNote,
    Invoice,
}

#[derive(Debug, Clone, PartialEq)]
pub struct DocumentSeries {
    pub doc_type: DocumentType,
    pub code: String,
    pub prefix: String,
    pub next_number: i64,
}

impl DocumentSeries {
    pub fn issue_number(&mut self) -> String {
        let number = self.next_number;
        self.next_number += 1;
        format!("{}-{:06}", self.prefix, number)
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Fulfillment {
    pub ordered: f64,
    pub delivered: f64,
    pub invoiced: f64,
}

impl Fulfillment {
    pub fn can_deliver(&self, qty: f64) -> bool {
        self.delivered + qty <= self.ordered
    }

    pub fn can_invoice_from_delivery(&self, qty: f64) -> bool {
        self.invoiced + qty <= self.delivered
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn increments_series_number() {
        let mut s = DocumentSeries {
            doc_type: DocumentType::Invoice,
            code: "FAC2026".into(),
            prefix: "FAC-2026".into(),
            next_number: 7,
        };

        assert_eq!(s.issue_number(), "FAC-2026-000007");
        assert_eq!(s.issue_number(), "FAC-2026-000008");
        assert_eq!(s.next_number, 9);
    }

    #[test]
    fn blocks_over_delivery_or_over_invoice() {
        let f = Fulfillment {
            ordered: 10.0,
            delivered: 6.0,
            invoiced: 4.0,
        };

        assert!(f.can_deliver(4.0));
        assert!(!f.can_deliver(4.1));
        assert!(f.can_invoice_from_delivery(2.0));
        assert!(!f.can_invoice_from_delivery(2.1));
    }
}
