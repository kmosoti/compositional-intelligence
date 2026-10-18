//! Minimal metric helpers. Results are not project performance claims.
#![forbid(unsafe_code)]

/// Fraction of successes, or None for an empty sample.
pub fn success_rate(outcomes: &[bool]) -> Option<f64> {
    if outcomes.is_empty() {
        return None;
    }
    let wins = outcomes.iter().filter(|&&ok| ok).count();
    Some(wins as f64 / outcomes.len() as f64)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn counts_successes() {
        assert_eq!(success_rate(&[true, false, true]), Some(2.0 / 3.0));
        assert_eq!(success_rate(&[]), None);
    }
}
