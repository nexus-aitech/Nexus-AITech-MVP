import random
import uuid
from datetime import datetime, timedelta

class FakeDataProvider:
    """
    Generates highly realistic and dynamic mock data for MVP modules in absence of real-time APIs.
    """

    @staticmethod
    def generate_cyber_threats():
        return {
            "threats_detected": random.randint(1, 20),
            "ips_blocked": random.randint(0, 10),
            "threat_types": random.sample([
                "DDoS", "Malware", "Phishing", "Ransomware", "Zero-Day", "SQL Injection"
            ], k=random.randint(1, 3)),
            "last_attack": datetime.utcnow().isoformat()
        }

    @staticmethod
    def generate_teacher_data():
        return {
            "sessions_today": random.randint(5, 30),
            "learning_index": round(random.uniform(0.65, 0.98), 3),
            "students_active": random.randint(10, 50),
            "top_subjects": random.sample([
                "Math", "Science", "AI Ethics", "Blockchain", "Robotics", "Cyber Law"
            ], k=2),
            "engagement_level": random.choice(["High", "Medium", "Low"])
        }

    @staticmethod
    def generate_metaverse_data():
        return {
            "users_online": random.randint(50, 300),
            "events_today": random.randint(1, 20),
            "active_worlds": random.sample([
                "CryptoCity", "QuantumPark", "HoloVerse", "EdgeZone", "EduVerse"
            ], k=2),
            "latest_event": {
                "event_id": str(uuid.uuid4()),
                "name": random.choice([
                    "AI Concert", "Decentralized Hackathon", "NFT Art Expo", "Cyber Battle"]),
                "timestamp": (datetime.utcnow() - timedelta(minutes=random.randint(1, 120))).isoformat()
            }
        }