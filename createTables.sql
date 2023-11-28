CREATE  TABLE financial_dw.dbo.company_dim ( 
	CompanyKey           int      PRIMARY KEY NONCLUSTERED NOT ENFORCED,
	TickerSymbol         varchar(5)      NULL,
	CompanyName          varchar(100)      NULL,
	SectorName           varchar(100)      NOT NULL 
 );

SELECT * FROM financial_dw.dbo.company_dim;




CREATE  TABLE financial_dw.dbo.industry_dim ( 
	IndustryKey          int      PRIMARY KEY NONCLUSTERED NOT ENFORCED,
	SectorName           varchar(100)      NULL,
	SectorCode           int      NULL
 );

SELECT * FROM financial_dw.dbo.industry_dim;




CREATE  TABLE financial_dw.dbo.date_dim ( 
	DateKey              int      PRIMARY KEY NONCLUSTERED NOT ENFORCED,
	DateISO              date      NULL,
	Year                 int      NULL,
	QuarterNumber        int      NULL,
	QuarterName          varchar(100)      NULL,
	MonthNumber          int      NULL,
	MonthName            varchar(100)      NULL,
	DayNumber            int      NULL,
	DayName              varchar(100)      NULL
 );
 SELECT * FROM financial_dw.dbo.date_dim;




CREATE  TABLE financial_dw.dbo.fact_stock_performance ( 
	FactKey              bigint      PRIMARY KEY NONCLUSTERED NOT ENFORCED,
	DateKey              int      NOT NULL,
	CompanyKey           int      NOT NULL,
	OpenPrice            decimal(10,2)      NULL,
	High                 decimal(10,2)      NULL,
	Low                  decimal(10,2)      NULL,
	ClosePrice           decimal(10,2)      NULL,
	Volume               bigint      NULL
 );

SELECT * FROM financial_dw.dbo.fact_stock_performance;




CREATE  TABLE financial_dw.dbo.fact_financial_ratios ( 
	FactKey              int      PRIMARY KEY NONCLUSTERED NOT ENFORCED,
	DateKey              int      NOT NULL,
	CompanyKey           int      NOT NULL,
	AssetTurnoverRatio   decimal(10,4)      NULL,
	OperatingRatio       decimal(10,4)      NULL,
	CurrentRatio         decimal(10,4)      NULL,
	QuickRatio           decimal(10,4)      NULL,
	CashRatio            decimal(10,4)      NULL,
	WorkingCapital       decimal      NULL,
	OperatingCashFlowRatio decimal(10,4)      NULL,
	GrossMargin          decimal(10,4)      NULL,
	OperatingMargin      decimal(10,4)      NULL,
	NetProfitMargin      decimal(10,4)      NULL,
	InterestCoverageRatio decimal(10,4)      NULL
 );

SELECT * FROM financial_dw.dbo.fact_financial_ratios;



