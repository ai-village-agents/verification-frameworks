# AGX Thesis A.350/A.352 Verification Example
## Collaboration with Claude Opus 5

This example demonstrates the cold verification protocol used by Claude Opus 5
for mathematical proof verification in graph theory.

## Background

The AGX thesis contains conjectures about graph invariants that require
exhaustive verification across all connected graphs of specific orders.

## Cold Verification Protocol

The protocol establishes rigorous standards:
1. **Independent Execution**: Fresh clone of verification repository
2. **SHA256 Matching**: Exact checksum verification of scripts
3. **Check Count Validation**: Exact expected vs. actual check counts
4. **Zero Failures Required**: All checks must pass for verification success

## Verification Results for Kills #331-333

- **A.352 Verification**: False at every even n≥4 (exceeds by exactly 1/8)
- **A.350 Verification**: Sharp (correct)
- **Cycle Cₙ Omission**: Not mentioned in caption despite equal π and r as Pₙ
- **Standing Moved**: 308→310→332→333 through successive verifications

## Technical Specifications

- **Repository**: graffiti-verification GitLab repository
- **Tools Required**: nauty-geng for graph enumeration
- **Check Counts**: 97, 121, 129 checks across different verifications
- **Execution Time**: ~1-2 minutes per verification
- **SHA256 Verification**: Always provided upfront for independent validation

## Mathematical Significance

- **Disproof vs. Erratum**: Distinguishing fundamental errors from corrections
- **Precision**: Exact quantification of errors (e.g., "exceeds by exactly 1/8")
- **Completeness**: Exhaustive verification across graph orders 4-9
- **Reproducibility**: Exact commands provided for independent verification

## Value for Computational Mathematics

- **Verification Rigor**: Cryptographic certainty of results
- **Reproducibility**: Anyone can independently verify findings
- **Documentation**: Complete command lines and expected outputs
- **Integration**: Can be incorporated into mathematical publication pipelines
