"""
Authentication service for basic user management
"""
import secrets
import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from fastapi import HTTPException, status
from src.auth.models import User, Session
from src.utils.logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Basic authentication service"""
    
    def __init__(self):
        self.secret_key = secrets.token_urlsafe(32)
        self.algorithm = "HS256"
        self.token_expiry = timedelta(hours=24)
        self.users_db = {}  # In production, use a proper database
        self.sessions_db = {}
        
        # Initialize default admin user
        self._init_admin_user()
    
    def _init_admin_user(self):
        """Initialize default admin user"""
        admin_user = User.create_user(
            username="admin",
            email="admin@ai-job-recommendation.com",
            password="admin123",
            full_name="System Administrator"
        )
        self.users_db[admin_user.id] = admin_user
        logger.info("Initialized default admin user: admin/admin123")
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(password, hashed_password)
    
    def create_access_token(self, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + (expires_delta or self.token_expiry)
        to_encode = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
    
    async def register_user(self, username: str, email: str, password: str, full_name: str) -> User:
        """Register a new user"""
        # Check if username or email already exists
        for user in self.users_db.values():
            if user.username == username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )
            if user.email == email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Create new user
        user = User.create_user(username, email, password, full_name)
        self.users_db[user.id] = user
        
        logger.info(f"New user registered: {username}")
        return user
    
    async def authenticate_user(self, username: str, password: str, ip_address: str, user_agent: str) -> Dict[str, Any]:
        """Authenticate user and create session"""
        # Find user by username
        user = None
        for u in self.users_db.values():
            if u.username == username:
                user = u
                break
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not user.verify_password(password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Update last login
        user.update_last_login()
        
        # Create session
        session = Session.create_session(user.id, ip_address, user_agent)
        self.sessions_db[session.id] = session
        
        # Create access token
        access_token = self.create_access_token(user.id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name
            },
            "session_id": session.id
        }
    
    async def logout_user(self, session_id: str) -> bool:
        """Logout user and invalidate session"""
        if session_id in self.sessions_db:
            session = self.sessions_db[session_id]
            session.is_active = False
            return True
        return False
    
    async def get_current_user(self, token: str) -> User:
        """Get current user from token"""
        payload = self.verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        user_id = payload.get("sub")
        if not user_id or user_id not in self.users_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user = self.users_db[user_id]
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )
        
        return user
