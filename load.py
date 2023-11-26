from sqlalchemy import text
from common.base import session, engine
from common.tables import DateDim, CompanyDim, IndustryDim, FactFinancialRatios, FactStockPerformance
import transform


def uploadDFtoDW():

    session.execute(text("USE CIS4400DB;"))
    session.execute(text("IF SCHEMA_ID('INSTANCE') IS NULL EXECUTE('CREATE SCHEMA INSTANCE;');"))
    session.commit()

    df_date = transform.date_table()
    df_date.to_sql(DateDim.__tablename__, con=engine, schema='INSTANCE', if_exists='replace', index=False)

    df_company = transform.clean_constituents()
    df_company.to_sql(CompanyDim.__tablename__, con=engine, schema='INSTANCE', if_exists='replace', index=False)

    df_industry = transform.clean_sectors()
    df_industry.to_sql(IndustryDim.__tablename__, con=engine, schema='INSTANCE', if_exists='replace', index=False)

    df_stock_performance = transform.clean_stockprices()
    df_stock_performance.to_sql(FactStockPerformance.__tablename__, con=engine, schema='INSTANCE', if_exists='replace', index=False)

    df_financial_ratios = transform.clean_ratios()
    df_financial_ratios.to_sql(FactFinancialRatios.__tablename__, con=engine, schema='INSTANCE', if_exists='replace', index=False)

    session.commit()

    foreign_key_sql_company_dim_industry_dim = """
        ALTER TABLE INSTANCE.company_dim
        ADD CONSTRAINT fk_company_dim_industry_dim
        FOREIGN KEY(SectorName)
        REFERENCES INSTANCE.industry_dim(SectorName);"""

    foreign_key_sql_fact_financial_ratios_company_dim = """
            ALTER TABLE INSTANCE.fact_financial_ratios
            ADD CONSTRAINT fk_fact_financial_ratios_company_dim
            FOREIGN KEY(CompanyKey)
            REFERENCES INSTANCE.company_dim( CompanyKey );
        """

    foreign_key_sql_fact_financial_ratios_date_dim = """
            ALTER TABLE INSTANCE.fact_financial_ratios
            ADD CONSTRAINT fk_fact_financial_ratios_date_dim
            FOREIGN KEY(DateKey)
            REFERENCES INSTANCE.date_dim( DateKey );
        """

    foreign_key_sql_fact_stock_performance_company_dim = """
                ALTER TABLE INSTANCE.fact_stock_performance
                ADD CONSTRAINT fk_fact_stock_performance_company_dim
                FOREIGN KEY(CompanyKey)
                REFERENCES INSTANCE.company_dim( CompanyKey );
            """

    foreign_key_sql_fact_stock_performance_date_dim = """
                ALTER TABLE INSTANCE.fact_stock_performance
                ADD CONSTRAINT fk_fact_stock_performance_date_dim
                FOREIGN KEY(DateKey)
                REFERENCES INSTANCE.date_dim( DateKey );
            """

    # Execute the SQL statement to add the foreign key constraint
    session.execute(text(foreign_key_sql_company_dim_industry_dim))
    session.execute(text(foreign_key_sql_fact_financial_ratios_company_dim))
    session.execute(text(foreign_key_sql_fact_financial_ratios_date_dim))
    session.execute(text(foreign_key_sql_fact_stock_performance_company_dim))
    session.execute(text(foreign_key_sql_fact_stock_performance_date_dim))

    # Commit the transaction
    session.commit()

    # Close the session
    session.close()


def main():
    uploadDFtoDW()
