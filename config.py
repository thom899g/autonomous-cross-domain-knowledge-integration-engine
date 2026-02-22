"""
Configuration module for the Cross-Domain Knowledge Integration Engine.
Centralizes all configuration to ensure consistency and easy maintenance.
"""
import os
from typing import Dict, List, Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EngineConfig(BaseSettings):
    """Main configuration for the knowledge engine."""
    
    # Firebase Configuration
    firebase_credentials_path: str = Field(
        default="firebase-credentials.json",
        description="Path to Firebase service account JSON file"
    )
    firebase_project_id: str = Field(
        default=os.getenv("FIREBASE_PROJECT_ID", ""),
        description="Firebase project ID"
    )
    
    # Engine Configuration
    knowledge_update_interval_hours: int = Field(
        default=6,
        description="Hours between knowledge update cycles"
    )
    max_domains_per_cycle: int = Field(
        default=5,
        description="Maximum number of domains to process per cycle"
    )
    min_confidence_threshold: float = Field(
        default=0.7,
        description="Minimum confidence score for knowledge integration"
    )
    
    # Data Collection Configuration
    request_timeout_seconds: int = Field(
        default=30,
        description="Timeout for external API requests"
    )
    max_retries: int = Field(
        default=3,
        description="Maximum retry attempts for failed operations"
    )
    
    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    log_file_path: str = Field(
        default="logs/knowledge_engine.log",
        description="Path to log file"
    )
    
    # Domain Configuration
    active_domains: List[str] = Field(
        default=[
            "scientific_research",
            "technology_news", 
            "academic_papers",
            "industry_reports"
        ],
        description="List of domains to actively monitor and integrate"
    )
    
    # Cross-Domain Relationship Weights
    relationship_weights: Dict[str, float] = Field(
        default={
            "scientific_research->technology_news": 0.8,
            "academic_papers->industry_reports": 0.9,
            "technology_news->scientific_research": 0.7
        },
        description="Weights for cross-domain relationship strength"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global configuration instance
config = EngineConfig()

# Firebase collections configuration
class FirestoreCollections:
    """Centralized collection names for Firestore."""
    KNOWLEDGE_NODES = "knowledge_nodes"
    DOMAIN_SOURCES = "domain_sources"
    CROSS_DOMAIN_RELATIONS = "cross_domain_relations"
    INTEGRATION_HISTORY = "integration_history"
    ERROR_LOGS = "error_logs"
    EVOLUTION_METRICS = "evolution_metrics"
    
    @classmethod
    def all_collections(cls) -> List[str]:
        """Return all collection names."""
        return [
            cls.KNOWLEDGE_NODES,
            cls.DOMAIN_SOURCES,
            cls.CROSS_DOMAIN_RELATIONS,
            cls.INTEGRATION_HISTORY,
            cls.ERROR_LOGS,
            cls.EVOLUTION_METRICS
        ]