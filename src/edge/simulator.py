import json
from datetime import datetime

from edge.crypto_utils import CryptoManager

class AIWitnessSimulator:
    def __init__(self, device_id):
        self.device_id = device_id
        self.model_version = "v1.2"
        self.crypto = CryptoManager()
        self.private_key = self.crypto.generate_key_pair()

    def create_event_bundle(self, radar_dist):
        """Olay anında 5 temel veriyi paketler."""
        # AI Karar Mantığı (Basit)
        decision = "DUR" if radar_dist < 1.0 else "ILERLE"
        
        bundle = {
            "device_id": self.device_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "radar_meters": radar_dist,
            "ai_version": self.model_version,
            "ai_decision": decision,
            "camera_hash": self.crypto.generate_sha256_hash("sample_image_data")
        }
        
        # Paketi imzala ve hash'le
        bundle_str = json.dumps(bundle, sort_keys=True)
        bundle_hash = self.crypto.generate_sha256_hash(bundle_str)
        signature = self.crypto.sign_data(self.private_key, bundle_hash)
        
        return {"data": bundle, "hash": bundle_hash, "signature": signature}

# Test Kullanımı
if __name__ == "__main__":
    sim = AIWitnessSimulator("ROBOT-01")
    event = sim.create_event_bundle(radar_dist=0.7)
    print(json.dumps(event, indent=2))