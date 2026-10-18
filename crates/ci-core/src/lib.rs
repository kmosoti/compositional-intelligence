//! Preliminary evidence and hypothesis types. Not a cognition implementation.
#![forbid(unsafe_code)]

/// Stable identifiers used across alternative representations.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct EvidenceId(pub u64);

/// Distinguish observed inputs from interpretations and speculation.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClaimKind {
    Observation,
    Inference,
    Hypothesis,
    Prediction,
}

/// A typed claim referring to its supporting evidence.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Claim {
    pub id: u64,
    pub kind: ClaimKind,
    pub text: String,
    pub support: Vec<EvidenceId>,
}

impl Claim {
    pub fn new(id: u64, kind: ClaimKind, text: String, support: Vec<EvidenceId>) -> Self {
        Self { id, kind, text, support }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn preserves_provenance_and_claim_kind() {
        let c = Claim::new(7, ClaimKind::Hypothesis, "Possible relation".to_owned(), vec![EvidenceId(5)]);
        assert_eq!(c.kind, ClaimKind::Hypothesis);
        assert_eq!(c.support, vec![EvidenceId(5)]);
    }
}
