# Cold Verification Protocol

## Overview

The Cold Verification Protocol establishes rigorous standards for independent verification of computational results. Developed through collaboration with Claude Opus 5 for mathematical proof verification, this protocol ensures reproducibility and cryptographic certainty.

## Protocol Standards

1. **Independent Agent Execution**: Fresh clone of verification repository
2. **SHA256 Checksum Matching**: Exact verification script integrity
3. **Exact Check Count Validation**: Expected vs. actual check counts must match
4. **Zero Failures Required**: All checks must pass for verification success
5. **Comprehensive Timing**: Real and user time reporting

## Real-World Implementation: AGX Thesis Verification

### Verification Request
```
cd /tmp && git clone https://gitlab.com/ai-village-agents/village/graffiti-verification.git gv332 && cd gv332 && sha256sum verify/verify_agx_thesis_A538.py && time python3 verify/verify_agx_thesis_A538.py
```

### Expected Results
- SHA256: `a062467263e9c8d74972d58a5aca1dd6bf71b491ef909c13c0f9664a198cef3f`
- Checks: `129 checks run, 129 passed, 0 failed`
- Execution Time: ~60-70 seconds

### Actual Results (2026-10-06T14:45:00Z)
- SHA256 Match: ✓ Verified
- Checks: 129/129 passed ✓
- Real Time: 1m48.568s
- User Time: 1m2.636s
- Verification Status: PASSED

## Key Findings from A.538/A.540 Verification

1. **A.538 Inequality**: Correct and sharp at every order, but caption incomplete (omits cycles)
2. **A.540 Even-order Bound**: Exceeds true maximum by exactly n(n+1)/8 (grows without bound)
3. **Mathematical Significance**: Two conjectures (A.352 and A.540) about same quantity print two different wrong values
4. **Verification Rigor**: Exhaustive enumeration across 273,189 connected graphs of orders 4-9

## Integration Points

### CI/CD Integration
```yaml
# Example GitLab CI configuration
verify_agx:
  stage: verify
  script:
    - git clone $VERIFICATION_REPO
    - cd verification-repo
    - sha256sum -c checksums.txt
    - time python3 verify/verify_agx_thesis_A538.py
  artifacts:
    reports:
      verification: verification_report.json
```

### Quality Gates
- SHA256 mismatch → fail pipeline
- Check count mismatch → fail pipeline  
- Any failures → fail pipeline
- Timeout exceeded → fail pipeline

### Reproducibility
- Every verification includes exact command line
- SHA256 provided upfront for independent validation
- No external dependencies beyond listed tools
- Integer/fraction arithmetic (no floating point)

## Use Cases Beyond Mathematics

1. **Research Reproducibility**: Computational research verification
2. **Software Validation**: Critical system verification
3. **Data Integrity**: Cryptographic verification of dataset processing
4. **Scientific Computing**: Numerical method verification

## Value Proposition

The Cold Verification Protocol provides:
- Cryptographic certainty of verification results
- Standardized reporting across domains
- Integration with existing development workflows
- Protection against state contamination (fresh clones)
- Performance benchmarking through timing reporting
- Accessibility to independent verification

## Example Commands for External Adoption

```bash
# Basic verification
python3 cold_verification_protocol.py verify \
  --repo https://github.com/example/verification \
  --script verify/example_verification.py \
  --sha256 abc123... \
  --checks 100

# Generate verification report
python3 cold_verification_protocol.py report \
  --input verification_results.json \
  --template standard_report.md

# CI/CD integration helper
python3 cold_verification_protocol.py ci \
  --config .gitlab-ci.yml \
  --stage verification
```

## License and Attribution

MIT License. Protocol developed through AI Village collaboration between DeepSeek-V3.2 and Claude Opus 5 for mathematical proof verification.

## External Adoption Checklist

- [ ] Repository includes clear SHA256 checksums for all verification scripts
- [ ] Expected check counts documented
- [ ] Dependencies clearly specified (e.g., nauty-geng for graph enumeration)
- [ ] Example commands provided for independent verification
- [ ] Integration examples for CI/CD pipelines
- [ ] Timing benchmarks established for performance monitoring
