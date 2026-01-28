import base64
import io
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

matplotlib.use("Agg")


def EncodeImage(fig):
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)

    # Encode image to base64 string
    img_tag = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)

    return f"data:image/png;base64,{img_tag}"


def plot_to_img_tag_legacy(data, title, xlabel, ylabel):
    # Use subplots for better control over the figure and axes
    fig, ax = plt.subplots(figsize=(12, 6))

    # Convert data to DataFrame with proper structure
    df = pd.DataFrame(data, columns=["date", "currency", "rate"])

    # Pivot the data to have currencies as columns and dates as index
    pivot_df = df.pivot(index="date", columns="currency", values="rate")

    # Reset index to make 'date' a column again for plotting
    pivot_df.reset_index(inplace=True)

    # Plot each currency's rate over time
    for currency in pivot_df.columns[1:]:  # Skip the 'date' column
        ax.plot(pivot_df["date"], pivot_df[currency], marker="o", label=currency)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True)

    # Rotate and align the tick labels so they look better
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    # If still too crowded, show fewer x-axis ticks
    if len(pivot_df) > 20:
        # Show approximately 15 evenly spaced ticks
        ax.xaxis.set_major_locator(plt.MaxNLocator(15))

    # Use automatic layout adjustment to prevent label overlap
    fig.tight_layout()

    # Save plot to a BytesIO object
    return EncodeImage(fig)


def CurrencyRatePlot(data, filters):
    fig, ax = plt.subplots(figsize=(12, 6))

    currency_data = {}
    for date, currency, rate in data:
        if filters is None or currency in filters:
            if currency not in currency_data:
                currency_data[currency] = {"dates": [], "rates": []}
            # Ensure date is datetime object
            if isinstance(date, str):
                date = pd.to_datetime(date)
            currency_data[currency]["dates"].append(date)
            currency_data[currency]["rates"].append(rate)

    # Plot each currency
    for currency, values in currency_data.items():
        ax.plot(
            values["dates"], values["rates"], marker="o", label=currency, linewidth=2
        )

    # Customize the plot
    ax.set_xlabel("Date")
    ax.set_ylabel("Exchange Rate")
    ax.set_title("Currency Exchange Rates Over Time")
    ax.grid(True, alpha=0.3)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    # Calculate appropriate date interval based on data range
    if currency_data:
        # Get the date range from the first currency
        first_currency = list(currency_data.values())[0]
        date_range = (max(first_currency["dates"]) - min(first_currency["dates"])).days

        if date_range > 180:
            interval = 30
        elif date_range > 90:
            interval = 15
        elif date_range > 14:
            interval = 3
        else:
            interval = 1

        # Format x-axis dates with appropriate interval
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))

    plt.tight_layout()

    # Add legend if there are currencies to show
    if currency_data:
        ax.legend(loc="lower left")

    return EncodeImage(fig)


def GraphStockPrice(data):
    stock_data = {}

    # Group data by stock
    for row in data:
        stock_name = row[2]
        if stock_name not in stock_data:
            stock_data[stock_name] = {"dates": [], "prices": []}
        stock_data[stock_name]["dates"].append(row[1])
        stock_data[stock_name]["prices"].append(row[3])

    plt.clf()
    plt.figure(figsize=(12, 6))

    # Plot each stock separately
    for stock_name, values in stock_data.items():
        plt.plot(
            values["dates"],
            values["prices"],
            marker="o",
            linestyle="-",
            label=stock_name,
        )

    plt.title("Stock Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend()
    plt.tight_layout()

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)

    # Encode image to base64 string
    img_tag = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f"data:image/png;base64,{img_tag}"
