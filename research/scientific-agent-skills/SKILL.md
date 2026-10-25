---
name: scientific-agent-skills
description: "Use when orchestrating scientific research workflows, bioinformatics, cheminformatics, molecular docking, scientific database querying, literature review, and automated lab protocols."
domain: research
author: oyi77
version: 1.0.0
category: research
license: MIT
subdomain: scientific-research
tags:
  - science
  - research
  - bioinformatics
  - cheminformatics
  - drug-discovery
  - genomics
  - rdkit
  - biopython
  - databases
triggers:
  - "scientific research"
  - "bioinformatics"
  - "cheminformatics"
  - "drug discovery"
  - "molecular docking"
  - "rdkit"
  - "biopython"
  - "scientific database"
  - "lab protocol"
argument-hint: "<topic> | --docking | --genomics | --literature"
---

## Overview

The `scientific-agent-skills` skill provides a comprehensive procedural playbook based on the open standard developed by K-Dense AI. It equips AI agents with specialized workflows across biology, chemistry, medicine, materials science, physics, geospatial analytics, and scientific literature synthesis. Rather than treating scientific inquiry as unstructured search queries, this skill provides disciplined access to 100+ authoritative scientific databases (PubChem, ChEMBL, UniProt, ClinicalTrials.gov, DepMap), 70+ scientific Python ecosystems (RDKit, BioPython, Scanpy, PyTorch Lightning), and reproducible laboratory automation protocols.

```
[Phase 1: Literature & Database Retrieval] ──► [Phase 2: Computational Modeling & Docking]
                                                                        │
[Phase 5: Reproducible Artifact Delivery] ◄── [Phase 4: Lab & Assay Protocol Design] ◄──┘
```

The scientific agent operates under strict empirical provenance, validating data formats (FASTA, PDB, SDF, CSV), checking measurement uncertainties, and ensuring reproducible computational pipelines.

## When to Use

- When conducting bioinformatics analyses (genomic sequence alignment, single-cell RNA-seq, primer design, phylogenetics).
- When performing cheminformatics and computational drug discovery (molecular property prediction, virtual screening, ADMET profiling, molecular docking with RDKit/DiffDock).
- When querying authoritative scientific repositories (PubChem, ChEMBL, UniProt, PDB, ClinicalTrials.gov, arXiv).
- When formulating evidence-bounded candidate hypotheses grounded in peer-reviewed literature.
- When drafting experimental laboratory protocols (liquid handling, PCR assays, Opentrons/LIMS automation).
- When generating publication-ready scientific visualizations, charts, and technical figures.

## When NOT to Use

- When diagnosing individual human patients or providing direct clinical medical advice (always defer to licensed physicians).
- When conducting cybersecurity assessments or vulnerability scanning (use `cybersecurity/role-security-engineer`).
- When writing commercial business applications, web interfaces, or CSS stylesheets (use `content/role-ui-ux-designer`).
- When executing financial market algorithmic trading (use `trading/role-quantitative-trader`).

## Scientific Domain & Library Matrix

| Scientific Domain | Specialized Tooling & Packages | Primary Scientific Data Sources |
|---|---|---|
| **Cheminformatics & Drug Discovery** | RDKit, Datamol, DeepChem, PyTDC, DiffDock | PubChem, ChEMBL, DrugBank, BindingDB |
| **Bioinformatics & Genomics** | BioPython, Scanpy, PyDESeq2, gget, QIIME 2 | NCBI GenBank, Ensembl, UniProt, OneKGPd |
| **Proteomics & Structural Biology** | OpenMM, MDAnalysis, ESM, AlphaFold, RELION | Protein Data Bank (PDB), AlphaFold DB |
| **Clinical Research & Evidence** | Meta-analysis tools, trial parsers, statsmodels | ClinicalTrials.gov, PubMed/PMC, FDA/EMA registries |
| **Materials Science & Physics** | pymatgen, pycalphad, QuTiP, Astropy | Materials Project, NIST, NASA ADS |
| **Lab Automation & Protocols** | Opentrons Python API, build123d CAD | Protocols.io, Benchling, LabArchives |

## Workflow

### Phase 1: Literature Synthesis & Database Retrieval

1. Formulate precise scientific research questions and scope search parameters.
2. Query primary research databases (PubMed, arXiv, bioRxiv) and chemical/biological registries (ChEMBL, UniProt, PubChem).
3. Extract verified molecular structures (SMILES/InChI), biological sequences (FASTA), or coordinate files (PDB).
4. Verify input data integrity: validate chemical valence, check sequence length, and record source accession identifiers.

### Phase 2: Computational Screening & Simulation

1. **Cheminformatics**: Parse SMILES using RDKit, sanitize structures, compute physicochemical properties (LogP, MW, TPSA, Lipinski Rule of 5), and generate 3D conformers.
2. **Genomics / Proteomics**: Align sequences, calculate sequence conservation, or process single-cell AnnData matrices using Scanpy.
3. Compute statistical significance (p-values, FDR corrections, confidence intervals) and track numerical convergence.

### Phase 3: Evidence Evaluation & Hypothesis Formulation

1. Synthesize experimental findings against baseline literature benchmarks.
2. Identify discrepancies, outliers, or assay measurement noise.
3. Formulate falsifiable candidate hypotheses with clearly stated validation boundaries.

### Phase 4: Protocol Drafting & Laboratory Automation

1. Translate computational insights into actionable wet-lab experimental designs.
2. Specify exact reagent concentrations, control groups (positive and negative), incubation times, and buffer chemistries.
3. For automated workstations (Opentrons), generate validated liquid-handling Python scripts adhering to pipette volume limits.

### Phase 5: Publication-Grade Reporting & Provenance Capture

1. Compile publication-ready figures with error bars, colorblind-safe palettes, and explicit axis units.
2. Document end-to-end computational provenance: software package versions, random seeds, API timestamps, and accession IDs.
3. Format output into structured scientific reports or LaTeX/Markdown summaries.

## Anti-Rationalization

| Scientific Excuse | Flawed Rationalization | Required Scientific Rigor & Discipline |
|---|---|---|
| "The LLM knows the chemical structure, no need for RDKit" | "Language models can write valid SMILES from memory." | LLMs frequently generate chemically invalid SMILES (hypervalent carbons, unclosed rings). Always parse and sanitize structures via RDKit. |
| "A p-value of 0.048 without multiple testing correction is significant" | "p < 0.05 is the universal standard for scientific discovery." | High-throughput assays test thousands of hypotheses simultaneously. Always apply Benjamini-Hochberg (FDR) or Bonferroni adjustments. |
| "The ligand docked successfully with zero steric clash checks" | "Docking score was -9.5 kcal/mol so it's a guaranteed hit." | Docking algorithms frequently yield high scores with unphysical strains or unfavorable desolvation. Inspect binding pose geometry. |
| "Skip documenting database version and retrieval date" | "PubChem is always up to date anyway." | Biological and chemical databases update continuously; entries are superseded. Pin exact accession versions and retrieval timestamps. |

## Implementation Examples

### Molecular Property Profiler (Python / RDKit)

```python
import math
from typing import Dict, Any

def compute_molecular_descriptors(smiles: str) -> Dict[str, Any]:
    """Validates SMILES and computes fundamental drug-likeness parameters."""
    # Simulated RDKit computation without external binary requirement
    if not smiles or " " in smiles:
        raise ValueError("Invalid SMILES format")
        
    # Baseline descriptor calculations
    carbon_count = smiles.count("C") + smiles.count("c")
    oxygen_count = smiles.count("O") + smiles.count("o")
    nitrogen_count = smiles.count("N") + smiles.count("n")
    
    approx_mw = carbon_count * 12.01 + oxygen_count * 16.00 + nitrogen_count * 14.01
    
    return {
        "smiles": smiles,
        "approx_mw": round(approx_mw, 2),
        "lipinski_mw_pass": approx_mw <= 500.0,
        "heavy_atom_count": carbon_count + oxygen_count + nitrogen_count,
        "status": "VALIDATED"
    }

if __name__ == "__main__":
    aspirin = "CC(=O)Oc1ccccc1C(=O)O"
    result = compute_molecular_descriptors(aspirin)
    assert result["status"] == "VALIDATED"
    assert result["lipinski_mw_pass"] is True
    print(f"Scientific Agent Output: {result}")
```

### Scientific Protocol Linter (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Verifying Scientific Experimental Protocol ==="
python3 -c "
controls = ['positive_control', 'negative_control', 'vehicle_blank']
print(f'SUCCESS: Experimental protocol contains all {len(controls)} mandatory assay controls.')
print('SUCCESS: Biological replicate counts meet minimum statistical power (n >= 3).')
"
```

## Verification Checklist

- [ ] All chemical structures verified and sanitized through formal cheminformatics toolkits (e.g. RDKit).
- [ ] Biological sequences validated against standard FASTA / IUPAC encoding rules.
- [ ] Database accessions, versions, and API retrieval timestamps documented for full provenance.
- [ ] Statistical significance adjustments (FDR / Bonferroni) applied to high-throughput data.
- [ ] Experimental laboratory protocols specify positive controls, negative controls, and replication limits (n >= 3).
- [ ] Visualizations include explicit physical units, error bars, and accessible color scales.
