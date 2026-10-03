import requests
import uuid

BASE_URL = "http://localhost:8000/api/v1"

def test_incident_evidence_flow():
    print("Starting Incident/Evidence Pack flow test...")

    # 1. Create an Incident
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    inc_payload = {"user_id": user_id, "user_notes": "Testing incident mode"}
    inc_resp = requests.post(f"{BASE_URL}/incidents/", params=inc_payload)

    if inc_resp.status_code != 200:
        print(f"Failed to create incident: {inc_resp.text}")
        return

    incident_id = inc_resp.json()["incident_id"]
    print(f"Incident created: {incident_id}")

    # 2. Create an Evidence Pack
    pack_payload = {"description": "Initial evidence collection"}
    pack_resp = requests.post(f"{BASE_URL}/incidents/{incident_id}/evidence-pack", params=pack_payload)

    if pack_resp.status_code != 200:
        print(f"Failed to create evidence pack: {pack_resp.text}")
        return

    pack_id = pack_resp.json()["pack_id"]
    print(f"Evidence pack created: {pack_id}")

    # 3. Add Evidence Item
    item_payload = {
        "file_name": "screenshot_1.png",
        "file_path": "/uploads/evidence/screenshot_1.png",
        "file_type": "screenshot",
        "metadata": '{"browser": "chrome", "url": "http://fraudsite.com"}'
    }
    item_resp = requests.post(f"{BASE_URL}/incidents/evidence-packs/{pack_id}/items", params=item_payload)

    if item_resp.status_code != 200:
        print(f"Failed to add evidence item: {item_resp.text}")
        return

    print(f"Evidence item added: {item_resp.json()['item_id']}")

    # 4. Verify evidence retrieval
    ev_resp = requests.get(f"{BASE_URL}/incidents/{incident_id}/evidence")

    if ev_resp.status_code != 200:
        print(f"Failed to retrieve evidence: {ev_resp.text}")
        return

    evidence = ev_resp.json()
    print(f"Retrieved evidence: {evidence}")

    # Assertions
    assert len(evidence) > 0, "Should have at least one evidence pack"
    assert evidence[0]["pack_id"] == pack_id, "Pack ID mismatch"
    assert len(evidence[0]["items"]) > 0, "Should have at least one item"

    print("✅ Incident/Evidence Pack flow verified successfully!")

if __name__ == "__main__":
    try:
        test_incident_evidence_flow()
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
