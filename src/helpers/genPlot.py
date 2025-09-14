import matplotlib
import base64
import io
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot_to_img_tag(data, title, xlabel, ylabel):
    # Use subplots for better control over the figure and axes
    fig, ax = plt.subplots(figsize=(12, 6))

    # Convert data to DataFrame with proper structure
    df = pd.DataFrame(data, columns=['date', 'currency', 'rate'])
    
    # Pivot the data to have currencies as columns and dates as index
    pivot_df = df.pivot(index='date', columns='currency', values='rate')
    
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
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)

    # Encode image to base64 string
    img_tag = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    return f"data:image/png;base64,{img_tag}"