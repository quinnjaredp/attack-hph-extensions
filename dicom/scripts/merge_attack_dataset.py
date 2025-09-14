#!/usr/bin/env python3
"""
merge_attack_dataset.py

Merge the official Enterprise ATT&CK v17 (JSON bundle) with your Workbench export
that contains custom QNTK objects, producing a single dataset JSON suitable for
Navigator `customDataURL`.

Usage:
  python merge_attack_dataset.py <enterprise_v17_json> <quinntech_bundle_json> <output_json>

Example:
  python merge_attack_dataset.py enterprise-attack-17.1.json workbench_hph_dicom_v2.json data/enterprise_attack_qntk_v17.json
"""

import json
import sys
import os
import datetime

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def iso_now():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    ent_path, qntk_path, out_path = sys.argv[1:4]

    if not os.path.exists(ent_path):
        print(f"[!] Enterprise bundle not found: {ent_path}")
        sys.exit(2)
    if not os.path.exists(qntk_path):
        print(f"[!] QNTK bundle not found: {qntk_path}")
        sys.exit(3)

    ent = load_json(ent_path)
    qntk = load_json(qntk_path)

    now = iso_now()

    # Build id -> object map from Enterprise first
    objects_by_id = {}
    for o in ent.get("objects", []):
        oid = o.get("id")
        if oid:
            objects_by_id[oid] = o

    # Merge QNTK objects (prefer QNTK on collision)
    q_count = 0
    for o in qntk.get("objects", []):
        oid = o.get("id")
        if not oid:
            continue
        objects_by_id[oid] = o
        q_count += 1

    merged_objects = list(objects_by_id.values())

    # Find or create a collection object.
    coll = None
    for o in merged_objects:
        if o.get("type") == "x-mitre-collection":
            coll = o
            break

    if not coll:
        coll = {
            "type": "x-mitre-collection",
            "spec_version": "2.1",
            "id": "x-mitre-collection--qntk-enterprise-17",
            "created": now,
            "modified": now,
            "x_mitre_domains": ["enterprise-attack"],
            "x_mitre_contents": []
        }
        merged_objects.append(coll)

    # Update collection metadata for the custom dataset identity/version.
    coll["name"] = "Enterprise ATT&CK (QNTK HPH Extended)"
    coll["description"] = (
        "Enterprise ATT&CK v17 extended with QuinnTech's HPH/DICOM custom objects (QNTK). "
        "Intended for ATT&CK Navigator via customDataURL."
    )
    # ATT&CK spec version found in recent Enterprise bundles; keep a sensible default.
    coll["x_mitre_attack_spec_version"] = coll.get("x_mitre_attack_spec_version", "3.3.0")
    # IMPORTANT: give the dataset a unique 'version' so it doesn't collide with vanilla v17
    coll["x_mitre_version"] = "17-qntk"
    coll["modified"] = now
    if "x_mitre_domains" not in coll:
        coll["x_mitre_domains"] = ["enterprise-attack"]

    # Rebuild x_mitre_contents from all non-identity/marking/sighting objects
    contents = []
    def obj_modified(o):
        return o.get("modified") or o.get("created") or now

    for o in merged_objects:
        if o.get("type") in ("identity", "marking-definition", "sighting"):
            continue
        if "id" in o:
            contents.append({"object_ref": o["id"], "object_modified": obj_modified(o)})
    coll["x_mitre_contents"] = contents

    # Write bundle
    out_bundle = {
        "type": "bundle",
        "id": ent.get("id", "bundle--qntk-merged"),
        "objects": merged_objects
    }

    # Ensure target directory exists
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_bundle, f, indent=2)

    # Summary
    print(f"[+] Wrote merged dataset to: {out_path}")
    print(f"    Enterprise objects: {len(ent.get('objects', []))}")
    print(f"    QNTK objects merged: {q_count}")
    print(f"    Final object count: {len(merged_objects)}")
    print(f"    Collection name: {coll['name']}")
    print(f"    Collection x_mitre_version: {coll['x_mitre_version']}")

if __name__ == "__main__":
    main()
