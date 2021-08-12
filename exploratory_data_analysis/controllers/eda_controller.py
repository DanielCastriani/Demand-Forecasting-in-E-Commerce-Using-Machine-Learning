
from dtos.eda_dto import CustomerSummaryDTO
from controllers.database import load_database


def customer_summary(agg: int):
    sales_df = load_database()

    if agg == 1:
        customers = sales_df.groupby(['customer_city'])['customer_id'].nunique()
    elif agg == 2:
        customers = sales_df.groupby(['customer_state'])['customer_id'].nunique()

    customers = customers.reset_index()
    customers = customers.sort_values('customer_id', ascending=False)

    summary = CustomerSummaryDTO(
        rows=len(customers),
        costumers=customers,
        nunique=sales_df['customer_id'].nunique()
    )

    return summary

def seller_summary(agg: int):
    sales_df = load_database()

    if agg == 1:
        customers = sales_df.groupby(['seller_city'])['seller_id'].nunique()
    elif agg == 2:
        customers = sales_df.groupby(['seller_state'])['seller_id'].nunique()

    customers = customers.reset_index()
    customers = customers.sort_values('seller_id', ascending=False)

    summary = CustomerSummaryDTO(
        rows=len(customers),
        costumers=customers,
        nunique=sales_df['seller_id'].nunique()
    )

    return summary
