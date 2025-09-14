import matplotlib
import base64
import io
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot_to_img_tag(data, title, xlabel, ylabel):
    plt.clf()
    plt.figure(figsize=(12, 6))

    # Convert data to DataFrame with proper structure
    df = pd.DataFrame(data, columns=['date', 'currency', 'rate'])
    
    # Pivot the data to have currencies as columns and dates as index
    pivot_df = df.pivot(index='date', columns='currency', values='rate')
    
    # Reset index to make 'date' a column again for plotting
    pivot_df.reset_index(inplace=True)
    
    # Plot each currency's rate over time
    for currency in pivot_df.columns[1:]:  # Skip the 'date' column
        plt.plot(pivot_df["date"], pivot_df[currency], marker="o", label=currency)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    # Rotate and align the tick labels so they look better
    plt.xticks(rotation=45, ha="right")

    # Use automatic layout adjustment to prevent label overlap
    plt.tight_layout()

    # If still too crowded, show fewer x-axis ticks
    if len(pivot_df) > 20:
        # Show approximately 15 evenly spaced ticks
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(15))

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)

    # Encode image to base64 string
    img_tag = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{img_tag}"