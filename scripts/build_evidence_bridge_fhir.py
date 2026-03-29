from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = PROJECT_ROOT / "data-source" / "portfolio-data.snapshot.json"
DATA_JSON = PROJECT_ROOT / "data.json"
DATA_JS = PROJECT_ROOT / "data.js"
FHIR_BUNDLE_JSON = PROJECT_ROOT / "citation-bundle.json"


STATUS_WORKFLOW = {
    "Active": "triaged",
    "Submission ready": "triaged",
    "Submitted": "submitted",
    "Review": "waiting-for-input",
    "Accepted": "resolved-no-change",
    "Published": "published",
    "Shipped": "published",
    "Maintained": "applied",
    "Paused": "deferred",
    "Archived": "applied",
}

STATUS_DISPOSITION = {
    "Active": "persuasive",
    "Submission ready": "persuasive",
    "Submitted": "persuasive",
    "Review": "persuasive-with-modification",
    "Accepted": "persuasive",
    "Published": "persuasive",
    "Shipped": "persuasive",
    "Maintained": "persuasive",
    "Paused": "not-persuasive-with-modification",
    "Archived": "not-persuasive",
}


def slugify(value: str) -> str:
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", value.lower()))


def load_payload(source_path: Path) -> dict[str, object]:
    return json.loads(source_path.read_text(encoding="utf-8"))


def build_citation(project: dict[str, object], version_date: str) -> dict[str, object]:
    citation_id = f"citation-{slugify(project['id'] + '-' + project['name'])}"
    return {
        "resourceType": "Citation",
        "id": citation_id,
        "status": "active",
        "date": version_date,
        "publisher": "Mahmood Ahmad",
        "title": project["name"],
        "summary": [
            {
                "style": {"text": "plain"},
                "text": (
                    f"{project['name']} is indexed in {project['tierName']} as a {project['type']} "
                    f"within the bundled ResearchConstellation portfolio snapshot."
                ),
            }
        ],
        "classification": [
            {
                "type": {"text": "Portfolio tier"},
                "classifier": [{"text": project["tierShortName"]}],
            },
            {
                "type": {"text": "Project type"},
                "classifier": [{"text": project["type"]}],
            },
        ],
        "currentState": [{"text": project["statusLabel"]}],
        "note": [{"text": project["detail"]}],
        "citedArtifact": {
            "title": project["name"],
            "abstract": {"text": project["detail"]},
            "classification": [
                {
                    "type": {"text": "Portfolio tier"},
                    "classifier": [{"text": project["tierName"]}],
                }
            ],
        },
    }


def build_assessment(project: dict[str, object], citation_id: str, version_date: str) -> dict[str, object]:
    assessment_id = f"assessment-{slugify(project['id'] + '-' + project['name'])}"
    status_label = project["statusLabel"]
    return {
        "resourceType": "ArtifactAssessment",
        "id": assessment_id,
        "title": f"{project['name']} lifecycle assessment",
        "date": version_date,
        "artifactReference": {"reference": f"Citation/{citation_id}"},
        "content": [
            {
                "informationType": "classifier",
                "summary": (
                    f"Explicit lifecycle status carried through from the source snapshot: {status_label}."
                ),
                "classifier": [{"text": status_label}],
                "freeToShare": True,
            }
        ],
        "workflowStatus": STATUS_WORKFLOW.get(status_label, "triaged"),
        "disposition": STATUS_DISPOSITION.get(status_label, "persuasive"),
    }


def build_bundle(payload: dict[str, object]) -> dict[str, object]:
    version_date = date.today().isoformat()
    entries: list[dict[str, object]] = []
    citation_count = 0
    assessment_count = 0

    for project in payload["portfolio"]:
        citation = build_citation(project, version_date)
        entries.append(
            {
                "fullUrl": f"urn:uuid:{citation['id']}",
                "resource": citation,
            }
        )
        citation_count += 1

        if project["statusExplicit"]:
            assessment = build_assessment(project, citation["id"], version_date)
            entries.append(
                {
                    "fullUrl": f"urn:uuid:{assessment['id']}",
                    "resource": assessment,
                }
            )
            assessment_count += 1

    return {
        "resourceType": "Bundle",
        "id": "evidence-bridge-fhir-bundle",
        "type": "collection",
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total": len(entries),
        "entry": entries,
        "summary": {
            "citationCount": citation_count,
            "assessmentCount": assessment_count,
            "citationOnlyCount": citation_count - assessment_count,
        },
    }


def build_dashboard_data(payload: dict[str, object], bundle: dict[str, object]) -> dict[str, object]:
    overview = payload["overview"]
    explicit_projects = [project for project in payload["portfolio"] if project["statusExplicit"]]
    citation_only = [project for project in payload["portfolio"] if not project["statusExplicit"]]
    status_counts = Counter(project["statusLabel"] for project in explicit_projects)
    tier_counts = Counter(project["tierShortName"] for project in citation_only)

    return {
        "project": {
            "name": "EvidenceBridgeFHIR",
            "version": "0.1.0",
            "generatedAt": bundle["timestamp"],
            "sourcePath": overview["sourcePath"],
            "designBasis": [
                "FHIR Citation export per indexed project",
                "ArtifactAssessment records for explicit lifecycle statuses",
                "Static browser dashboard for bundle review",
            ],
        },
        "metrics": {
            "trackedProjects": overview["trackedProjects"],
            "citationCount": bundle["summary"]["citationCount"],
            "assessmentCount": bundle["summary"]["assessmentCount"],
            "bundleEntryCount": bundle["total"],
            "citationOnlyCount": bundle["summary"]["citationOnlyCount"],
            "explicitCoveragePercent": overview["explicitCoveragePercent"],
        },
        "explicitStatusBreakdown": [
            {"status": status, "count": count}
            for status, count in sorted(status_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "citationOnlyByTier": [
            {"tier": tier, "count": count}
            for tier, count in sorted(tier_counts.items(), key=lambda item: (-item[1], item[0]))
        ],
        "citationOnlySample": [
            {
                "name": project["name"],
                "tier": project["tierShortName"],
                "type": project["type"],
                "path": project["path"],
            }
            for project in citation_only[:14]
        ],
        "assessmentSample": [
            {
                "name": project["name"],
                "tier": project["tierShortName"],
                "status": project["statusLabel"],
                "path": project["path"],
            }
            for project in explicit_projects[:14]
        ],
    }


def write_outputs(data: dict[str, object], bundle: dict[str, object]) -> None:
    DATA_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")
    DATA_JS.write_text("window.EVIDENCE_BRIDGE_FHIR_DATA = " + json.dumps(data, indent=2) + ";\n", encoding="utf-8")
    FHIR_BUNDLE_JSON.write_text(json.dumps(bundle, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build EvidenceBridgeFHIR artifacts.")
    parser.add_argument(
        "--source",
        help="Optional path to a portfolio-data.json file. Relative paths resolve from the repository root.",
    )
    args = parser.parse_args()

    source_path = Path(args.source) if args.source else DEFAULT_SOURCE
    if not source_path.is_absolute():
        source_path = PROJECT_ROOT / source_path
    if not source_path.exists():
        raise SystemExit(f"Source data not found: {source_path}")

    payload = load_payload(source_path)
    bundle = build_bundle(payload)
    data = build_dashboard_data(payload, bundle)
    write_outputs(data, bundle)
    metrics = data["metrics"]
    print(
        "Built EvidenceBridgeFHIR "
        f"({metrics['citationCount']} citations, "
        f"{metrics['assessmentCount']} assessments, "
        f"{metrics['bundleEntryCount']} bundle entries)."
    )


if __name__ == "__main__":
    main()
