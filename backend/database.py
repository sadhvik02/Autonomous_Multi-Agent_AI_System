from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./business_agent.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    location = Column(String)
    website = Column(String, nullable=True)
    social_presence = Column(Text, nullable=True)
    contact_info = Column(String, nullable=True)
    
    analysis = relationship("Analysis", back_populates="business", uselist=False)
    strategy = relationship("Strategy", back_populates="business", uselist=False)
    proposal = relationship("Proposal", back_populates="business", uselist=False)

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    maturity_score = Column(Integer)
    strengths = Column(Text)
    weaknesses = Column(Text)
    missing_assets = Column(Text)
    
    business = relationship("Business", back_populates="analysis")

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    recommended_strategy = Column(Text)
    priority_actions = Column(Text)
    expected_impact = Column(Text)
    
    business = relationship("Business", back_populates="strategy")

class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    proposal_text = Column(Text)
    timeline = Column(String)
    estimated_cost = Column(String)
    expected_roi = Column(String)
    
    business = relationship("Business", back_populates="proposal")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
