from langchain_core.tools import tool

@tool
def get_Stock_price(symbol : str)->float:
    """Get the stock price for a given stock symbol (e.g., SENSEX, MSFT, RIL)."""
    return {
        "MSFT":750.25,
        "RIL":5820.52,
        "AMZN":158.0,
        "SENSEX":81500.02
    }.get(symbol,0.0)


