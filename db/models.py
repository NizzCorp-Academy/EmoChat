"""
Module: models
Author: Arshad
Date: 26-07-2025
Purpose: To define the database models.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.connector import Base

class User(Base):
    """
    Class: User
    Author: Arshad
    Date: 26-07-2025
    Purpose: To define the User model.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chat_logs = relationship("ChatLog", back_populates="user")
    feedback = relationship("Feedback", back_populates="user")

class ChatLog(Base):
    """
    Class: ChatLog
    Author: Arshad
    Date: 26-07-2025
    Purpose: To define the ChatLog model.
    """
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    risk_flag = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="chat_logs")
    feedback = relationship("Feedback", back_populates="chat_log")

class Feedback(Base):
    """
    Class: Feedback
    Author: Arshad
    Date: 26-07-2025
    Purpose: To define the Feedback model.
    """
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chat_log_id = Column(Integer, ForeignKey("chat_logs.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # e.g., 1-5
    comment = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="feedback")
    chat_log = relationship("ChatLog", back_populates="feedback")

class KnowledgeBase(Base):
    """
    Class: KnowledgeBase
    Author: Arshad
    Date: 26-07-2025
    Purpose: To define the KnowledgeBase model.
    """
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content_chunk = Column(Text, nullable=False)
    tags = Column(String(255), nullable=True)

class VectorIndex(Base):
    """
    Class: VectorIndex
    Author: Arshad
    Date: 26-07-2025
    Purpose: To define the VectorIndex model.
    """
    __tablename__ = "vector_index"

    vector_id = Column(String(255), primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("knowledge_base.id"), nullable=False)
    document_metadata = Column(Text) # JSON string or other format
    ##
