from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid

class MiMoMemory:
    def __init__(self, host="localhost", port=6333):
        # Connect to your Qdrant instance
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = "cleaning_history"
        
        # Initialize collection if it doesn't exist
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=3, distance=Distance.EUCLID), # [x, y, z]
            )

    def record_cleaning(self, position, sensor_data, mood):
        """Stores a cleaning 'snapshot' in Qdrant"""
        point_id = str(uuid.uuid4())
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=position, # Using GPS coordinates as the vector
                    payload={
                        "sensor_values": sensor_data,
                        "mood": mood,
                        "status": "cleaned"
                    }
                )
            ]
        )