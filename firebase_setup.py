"""
Firebase Firestore initialization and utility functions.
This module provides the database backbone for the knowledge engine.
"""
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from firebase_admin.exceptions import FirebaseError

from config import config, FirestoreCollections

logger = logging.getLogger(__name__)

class FirebaseManager:
    """Manages Firebase Firestore connection and operations."""
    
    _instance = None
    _db = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize_firebase()
            self._initialized = True
    
    def _initialize_firebase(self) -> None:
        """Initialize Firebase connection with error handling."""
        try:
            creds_path = Path(config.firebase_credentials_path)
            
            if not creds_path.exists():
                logger.error(f"Firebase credentials file not found: {creds_path}")
                raise FileNotFoundError(f"Firebase credentials file not found: {creds_path}")
            
            # Load and validate credentials
            with open(creds_path, 'r') as f:
                creds_data = json.load(f)
                required_fields = ["type", "project_id", "private_key_id", "private_key", "client_email"]
                if not all(field in creds_data for field in required_fields):
                    raise ValueError("Invalid Firebase credentials file structure")
            
            # Initialize Firebase
            cred = credentials.Certificate(str(creds_path))
            
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            
            self._db = firestore.client()
            logger.info(f"Firebase Firestore initialized for project: {config.firebase_project_id}")
            
            # Test connection
            self._test_connection()
            
        except (FirebaseError, ValueError, FileNotFoundError) as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during Firebase initialization: {str(e)}")
            raise
    
    def _test_connection(self) -> None:
        """Test Firestore connection by creating a test document."""
        try:
            test_ref = self._db.collection("connection_test").document("test")
            test_ref.set({
                "timestamp": datetime.utcnow(),
                "status": "connected"
            })
            test_ref.delete()
            logger.debug("Firestore connection test successful")
        except FirebaseError as e:
            logger.error(f"Firestore connection test failed: {str(e)}")
            raise
    
    @property
    def db(self) -> firestore.Client:
        """Get Firestore database client."""
        if self._db is