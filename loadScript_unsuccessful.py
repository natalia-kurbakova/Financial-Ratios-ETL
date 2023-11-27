from sqlalchemy import text
from common.base import session, engine
from common.tables import DateDim, CompanyDim, IndustryDim, FactFinancialRatios, FactStockPerformance
import transform
import sqlalchemy
import traceback



def uploadDFtoDW():

    #session.execute(text("USE financial_dw;"))
    session.execute(text("IF SCHEMA_ID('dbo') IS NULL EXECUTE('CREATE SCHEMA dbo;');"))
    print("checked if exists or created schema dbo")
    session.commit()

    df_date = transform.date_table()
    try:
        df_date.to_sql(DateDim.__tablename__, con=session, schema='dbo', if_exists='replace', index=False,
                   dtype={
                       'QuarterName': sqlalchemy.types.VARCHAR(length=100),
                       'MonthName': sqlalchemy.types.VARCHAR(length=100),
                       'DayName': sqlalchemy.types.VARCHAR(length=100)}
                   )
        session.commit()
        print("uploaded the date table!")
    except Exception as e:
        print(e)
        session.close()
        traceback.print_exc()

    df_company = transform.clean_constituents()
    try:
        df_company.to_sql(CompanyDim.__tablename__, con=session, schema='dbo', if_exists='replace', index=False,
                      dtype={'TickerSymbol': sqlalchemy.types.VARCHAR(length=5),
                             'CompanyName': sqlalchemy.types.VARCHAR(length=100),
                             'SectorName': sqlalchemy.types.VARCHAR(length=100)}
                      )
        session.commit()
        print("uploaded the company table!")
    except Exception as e:
        print(e)
        session.close()
        traceback.print_exc()

    df_industry = transform.clean_sectors()
    try:
        df_industry.to_sql(IndustryDim.__tablename__, con=session, schema='dbo', if_exists='replace', index=False,
                       dtype={'SectorName': sqlalchemy.types.VARCHAR(length=100)}
                       )
        session.commit()
        print("uploaded the sector table!")
    except Exception as e:
        print(e)
        session.close()
        traceback.print_exc()

    df_stock_performance = transform.clean_stockprices()
    try:
        df_stock_performance.to_sql(FactStockPerformance.__tablename__, con=session, schema='dbo', if_exists='replace', index=False)
        session.commit()
        print("uploaded the stock history table!")
    except Exception as e:
        print(e)
        session.close()
        traceback.print_exc()

    df_financial_ratios = transform.clean_ratios()
    try:
        df_financial_ratios.to_sql(FactFinancialRatios.__tablename__, con=session, schema='dbo', if_exists='replace', index=False)
        session.commit()
        print("uploaded the ratios table!")
    except Exception as e:
        print(e)
        session.close()
        traceback.print_exc()


    foreign_key_sql_company_dim_industry_dim = """
        ALTER TABLE dbo.company_dim
        ADD CONSTRAINT fk_company_dim_industry_dim
        FOREIGN KEY (SectorName)
        REFERENCES dbo.industry_dim(SectorName);"""

    foreign_key_sql_fact_financial_ratios_company_dim = """
            ALTER TABLE dbo.fact_financial_ratios
            ADD CONSTRAINT fk_fact_financial_ratios_company_dim
            FOREIGN KEY(CompanyKey)
            REFERENCES dbo.company_dim( CompanyKey );
        """

    foreign_key_sql_fact_financial_ratios_date_dim = """
            ALTER TABLE dbo.fact_financial_ratios
            ADD CONSTRAINT fk_fact_financial_ratios_date_dim
            FOREIGN KEY (DateKey)
            REFERENCES dbo.date_dim( DateKey );
        """

    foreign_key_sql_fact_stock_performance_company_dim = """
                ALTER TABLE dbo.fact_stock_performance
                ADD CONSTRAINT fk_fact_stock_performance_company_dim
                FOREIGN KEY (CompanyKey)
                REFERENCES dbo.company_dim( CompanyKey );
            """

    foreign_key_sql_fact_stock_performance_date_dim = """
                ALTER TABLE dbo.fact_stock_performance
                ADD CONSTRAINT fk_fact_stock_performance_date_dim
                FOREIGN KEY (DateKey)
                REFERENCES dbo.date_dim( DateKey );
            """

    # Execute the SQL statement to add the foreign key constraint
    try:
        session.execute(text(foreign_key_sql_company_dim_industry_dim))
        session.commit()
        print("added foreign key 1!")
    except Exception as e:
        print(e)
        traceback.print_exc()

    try:
        session.execute(text(foreign_key_sql_fact_financial_ratios_company_dim))
        session.commit()
        print("added foreign key 2!")
    except Exception as e:
        print(e)
        traceback.print_exc()

    try:
        session.execute(text(foreign_key_sql_fact_financial_ratios_date_dim))
        session.commit()
        print("added foreign key 3!")
    except Exception as e:
        print(e)
        traceback.print_exc()
    try:
        session.execute(text(foreign_key_sql_fact_stock_performance_company_dim))
        session.commit()
        print("added foreign key 4!")
    except Exception as e:
        print(e)
        traceback.print_exc()

    try:
        session.execute(text(foreign_key_sql_fact_stock_performance_date_dim))
        session.commit()
        print("added foreign key 5!")
    except Exception as e:
        print(e)
        traceback.print_exc()


def main():
    uploadDFtoDW()
