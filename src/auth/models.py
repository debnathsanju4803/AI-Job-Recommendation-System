"""
Authentication models and database schema
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, validator
from passlib.context import CryptContext
import secrets
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    """User model for authentication"""
    id: str
    username: str
    email: EmailStr
    hashed_password: str
    full_name: str
    role: str  # 'user', 'admin', 'super_admin'
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None
    login_attempts: int = 0
    locked_until: Optional[datetime] = None
    profile_data: Dict[str, Any] = {}
    
    @classmethod
    def create_user(cls, username: str, email: str, password: str, full_name: str, role: str = "user"):
        """Create a new user with hashed password"""
        return cls(
            id=secrets.token_urlsafe(16),
            username=username,
            email=email,
            hashed_password=pwd_context.hash(password),
            full_name=full_name,
            role=role,
            created_at=datetime.utcnow()
        )
    
    def verify_password(self, password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(password, self.hashed_password)
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        self.login_attempts = 0
        self.locked_until = None
    
    def is_account_locked(self) -> bool:
        """Check if account is locked due to failed attempts"""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False
    
    def increment_login_attempts(self):
        """Increment login attempts and lock account if too many"""
        self.login_attempts += 1
        if self.login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=15)

class Session(BaseModel):
    """Session model for authentication"""
    id: str
    user_id: str
    token: str
    expires_at: datetime
    created_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True
    
    @classmethod
    def create_session(cls, user_id: str, ip_address: str, user_agent: str):
        """Create a new session"""
        return cls(
            id=secrets.token_urlsafe(32),
            user_id=user_id,
            token=secrets.token_urlsafe(64),
            expires_at=datetime.utcnow() + timedelta(hours=24),
            created_at=datetime.utcnow(),
            ip_address=ip_address,
            user_agent=user_agent
        )

class OAuthState(BaseModel):
    """OAuth state for security"""
    state: str
    redirect_uri: str
    created_at: datetime
    
    @classmethod
    def create_state(cls, redirect_uri: str):
        return cls(
            state=secrets.token_urlsafe(32),
            redirect_uri=redirect_uri,
            created_at=datetime.utcnow()
        )

class UserProfile(BaseModel):
    """User profile data"""
    user_id: str
    resume_preferences: Dict[str, Any] = {}
    job_preferences: Dict[str, Any] = {}
    saved_searches: List[Dict[str, Any]] = []
    application_history: List[Dict[str, Any]] = []
    notifications: List[Dict[str, Any]] = []
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create_profile(cls, user_id: str):
        return cls(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

class APIKey(BaseModel):
    """API key for external integrations"""
    id: str
    user_id: str
    key: str
    name: str
    permissions: List[str]
    is_active: bool = True
    created_at: datetime
    last_used: Optional[datetime] = None
    
    @classmethod
    def create_key(cls, user_id: str, name: str, permissions: List[str]):
        return cls(
            id=secrets.token_urlsafe(16),
            user_id=user_id,
            key=f"ak_{secrets.token_urlsafe(32)}",
            name=name,
            permissions=permissions,
            created_at=datetime.utcnow()
        )