M. Mahmood

EvidenceBridgeFHIR: Exporting the C Drive Evidence Portfolio into Citation and ArtifactAssessment Bundles

Can a heterogeneous C-drive methods portfolio be exported into a standards-facing exchange format without losing its operational status signals? We reused the bundled ResearchConstellation snapshot containing 134 indexed projects across 12 tiers and mapped each project into a FHIR Citation record. EvidenceBridgeFHIR v0.1 then attached ArtifactAssessment resources only where the source snapshot already carried an explicit lifecycle label suitable for reuse. The resulting bundle contained 185 FHIR resources, combining 134 Citations with 51 ArtifactAssessments for 38.1 percent coverage (51 of 134), while 83 projects remained citation-only placeholders. Citation-only pressure clustered in tiers 10 and 12, which supplied 57 unresolved exports and dominated the interoperability backlog to date despite the portfolio's broader methodological depth. This shows the next barrier is not exchange syntax but portfolio curation, because standards layers cannot recover lifecycle judgments that were never frozen upstream. The bundle improves inspectability, but it does not validate against a live FHIR server or infer missing assessments automatically.

Outside Notes

Type: methods
Primary estimand: ArtifactAssessment coverage across exported projects
Certainty: moderate
Validation: DRAFT
