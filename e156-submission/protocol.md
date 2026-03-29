Mahmood Ahmad
Tahir Heart Institute
author@example.com

Protocol: EvidenceBridgeFHIR - Static Portfolio Exchange Audit

This protocol describes a snapshot-first interoperability audit using the bundled `data-source/portfolio-data.snapshot.json` copied from `ResearchConstellation`. Eligible records are all 134 indexed project rows across the 12 portfolio tiers preserved in that snapshot. The primary estimand is ArtifactAssessment coverage across exported projects, defined as the proportion of Citation records that can be paired with a lifecycle assessment derived from an explicit source status. Secondary outputs will count bundle entries, citation-only placeholders, assessment counts by status label, and unresolved export pressure by tier. The build process will emit `citation-bundle.json`, `data.json`, `data.js`, and a static dashboard for browser review. Each project will be represented as a FHIR Citation resource, and projects with explicit lifecycle labels will additionally receive ArtifactAssessment resources carrying reusable status judgments. Anticipated limitations include no live FHIR server validation, no terminology binding checks, no inference of missing lifecycle states, and continued dependence on upstream status normalization.

Outside Notes

Type: protocol
Primary estimand: ArtifactAssessment coverage across exported projects
App: EvidenceBridgeFHIR v0.1
Code: repository root, scripts/build_evidence_bridge_fhir.py, citation-bundle.json, and data-source/portfolio-data.snapshot.json
Date: 2026-03-29
Validation: DRAFT

References

1. Citation - FHIR v5.0.0. HL7 FHIR Release 5; current published version.
2. ArtifactAssessment - FHIR v5.0.0. HL7 FHIR Release 5; current published version.
3. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement. BMJ. 2021;372:n71.

AI Disclosure

This protocol was drafted from versioned local artifacts and deterministic build logic. AI was used as a drafting and implementation assistant under author supervision, with the author retaining responsibility for scope, methods, and reporting choices.
