from sqlalchemy import Column, Integer, String, Date, Numeric, BigInteger, PrimaryKeyConstraint

from common.base import Base


class DateDim(Base):
    __tablename__ = 'date_dim'

    DateKey = Column(Integer, primary_key=True)
    DateISO = Column(Date)
    Year = Column(Integer)
    QuarterNumber = Column(Integer)
    QuarterName = Column(String(100))
    MonthNumber = Column(Integer)
    MonthName = Column(String(100))
    DayNumber = Column(Integer)
    DayName = Column(String(100))


class CompanyDim(Base):
    __tablename__ = 'company_dim'

    CompanyKey = Column(Integer, primary_key=True)
    TickerSymbol = Column(String(5))
    CompanyName = Column(String(100))
    SectorName = Column(String(100))

    # Define composite primary key constraint
    __table_args__ = (
        PrimaryKeyConstraint('CompanyKey', 'SectorName'),
    )


class IndustryDim(Base):
    __tablename__ = 'industry_dim'

    IndustryKey = Column(Integer, primary_key=True)
    SectorName = Column(String(100))
    SectorCode = Column(Integer)


class FactFinancialRatios(Base):
    __tablename__ = 'fact_financial_ratios'

    FactKey = Column(Integer, primary_key=True)
    DateKey = Column(Integer, primary_key=True)
    CompanyKey = Column(Integer, primary_key=True)
    AssetTurnoverRatio = Column(Numeric(10, 4))
    OperatingRatio = Column(Numeric(10, 4))
    CurrentRatio = Column(Numeric(10, 4))
    QuickRatio = Column(Numeric(10, 4))
    CashRatio = Column(Numeric(10, 4))
    WorkingCapital = Column(BigInteger)
    OperatingCashFlowRatio = Column(Numeric(10, 4))
    GrossMargin = Column(Numeric(10, 4))
    OperatingMargin = Column(Numeric(10, 4))
    NetProfitMargin = Column(Numeric(10, 4))
    InterestCoverageRatio = Column(Numeric(10, 4))

    # Define composite primary key constraint
    __table_args__ = (
        PrimaryKeyConstraint('FactKey', 'DateKey', 'CompanyKey'),
    )


class FactStockPerformance(Base):
    __tablename__ = 'fact_stock_performance'

    FactKey = Column(BigInteger, primary_key=True)
    DateKey = Column(Integer, primary_key=True)
    CompanyKey = Column(Integer, primary_key=True)
    OpenPrice = Column(Numeric(10, 2))
    High = Column(Numeric(10, 2))
    Low = Column(Numeric(10, 2))
    ClosePrice = Column(Numeric(10, 2))
    Volume = Column(BigInteger)

    # Define composite primary key constraint
    __table_args__ = (
        PrimaryKeyConstraint('FactKey', 'DateKey', 'CompanyKey'),
    )
