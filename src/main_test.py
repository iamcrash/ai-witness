import sys
import os
import json
from edge.simulator import AIWitnessSimulator
from edge.crypto_utils import CryptoManager

# Python'un src klasörünü görmesini sağlıyoruz
sys.path.append(os.path.join(os.getcwd(), "src"))

from edge.simulator import AIWitnessSimulator
from edge.crypto_utils import CryptoManager

def run_system_check():
    print("=== AI-WITNESS SİSTEM KONTROLÜ BAŞLATILIYOR ===\n")

    # 1. Cihazı Başlat
    device_id = "ROBOT-01"
    sim = AIWitnessSimulator(device_id)
    print(f"[1] Cihaz Başlatıldı: {device_id}")

    # 2. Olay Simülasyonu (Kaza Anı)
    # Radar 0.7 metre (1 metrenin altında olduğu için DUR demeli)
    print("[2] Olay Simüle Ediliyor (Radar: 0.7m)...")
    event_packet = sim.create_event_bundle(radar_dist=0.7)
    
    data = event_packet["data"]
    bundle_hash = event_packet["hash"]
    signature = event_packet["signature"]

    print(f"    -> Üretilen Karar: {data['ai_decision']}")
    print(f"    -> Veri Hash'i: {bundle_hash}")

    # 3. Kriptografik Doğrulama (En Kritik Kısım)
    # Bu aşama, blokzincirde yapılacak olan işlemin simülasyonudur.
    print("\n[3] Kriptografik Doğrulama Yapılıyor...")
    
    # Cihazın kamuya açık anahtarını (Public Key) alıyoruz
    public_key = sim.private_key.public_key()
    
    is_valid = CryptoManager.verify_signature(
        public_key=public_key,
        signature_hex=signature,
        data=bundle_hash
    )

    if is_valid:
        print("✅ BAŞARILI: İmza geçerli! Veri kesinlikle bu cihazdan geldi ve değişmedi.")
    else:
        print("❌ HATA: İmza geçersiz! Veri manipüle edilmiş veya anahtar yanlış.")

    # 4. Veri Akışı Kontrolü
    print("\n[4] Nihai Veri Paketi:")
    print(json.dumps(event_packet, indent=2))

if __name__ == "__main__":
    run_system_check()