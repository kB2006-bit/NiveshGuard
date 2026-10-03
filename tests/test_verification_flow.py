import requests
import uuid

BASE_URL = "http://localhost:8000/api/v1"

def test_verification_flow():
    print("Starting Verification Flow test...")

    # 1. Test Source Retrieval
    sources_resp = requests.get(f"{BASE_URL}/verification/sources")
    if sources_resp.status_code != 200:
        print(f"Failed to get sources: {sources_resp.text}")
        return

    sources = sources_resp.json()
    print(f"Retrieved {len(sources)} active sources")
    assert len(sources) > 0, "Registry should be seeded with sources"

    # 2. Test Claim Mapping
    claims = [
        "Registered with SEBI",
        "Approved by RBI",
        "Check on cybercrime portal",
        "Random unverified claim"
    ]
    map_resp = requests.post(f"{BASE_URL}/verification/map", json=claims)
    if map_resp.status_code != 200:
        print(f"Failed to map claims: {map_resp.text}")
        return

    mapping = map_resp.json()
    print(f"Mapped {len(mapping)} claims")

    # Verify SEBI mapping
    sebi_match = next((m for m in mapping if "SEBI" in m["claim"]), None)
    assert sebi_match is not None, "SEBI claim should be mapped"
    assert sebi_match["status"] == "verifiable", "SEBI should be verifiable"
    assert "sebi" in sebi_match["source"]["source_id"], "Should map to SEBI source"

    # Verify manual verification for random claim
    manual_match = next((m for m in mapping if "Random" in m["claim"]), None)
    assert manual_match is not None, "Random claim should be processed"
    assert manual_match["status"] == "manual_verification_required", "Should require manual verification"

    print("✅ Verification Flow verified successfully!")

if __name__ == "__main__":
    try:
        test_verification_flow()
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
