# EvidenceBridgeFHIR

EvidenceBridgeFHIR is a new interoperability project built from the bundled `ResearchConstellation` snapshot.

## Why this exists

The portfolio now has a live atlas and a packaging layer, but it still lacks a standards-facing export that other systems could ingest without reading custom JSON.

EvidenceBridgeFHIR addresses that gap by exporting:

- one FHIR `Citation` resource for every tracked project
- one `ArtifactAssessment` resource for every project carrying an explicit lifecycle label
- a static dashboard that shows where the export is complete and where it still degrades into citation-only placeholders

## Outputs

- `citation-bundle.json` - the generated FHIR collection bundle
- `data.json` and `data.js` - dashboard payloads
- `index.html` - static bundle review dashboard
- `e156-submission/` - paper, protocol, metadata, and reader page

## Rebuild

Run:

`python C:\Users\user\EvidenceBridgeFHIR\scripts\build_evidence_bridge_fhir.py`

For a custom source file:

`python C:\Users\user\EvidenceBridgeFHIR\scripts\build_evidence_bridge_fhir.py --source path\to\portfolio-data.json`

## Standards basis

This project is informed by HL7 FHIR R5 `Citation` and `ArtifactAssessment` resources, but kept deliberately static so the output remains easy to inspect, version, and serve from GitHub Pages.
