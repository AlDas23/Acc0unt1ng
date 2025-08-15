import matplotlib
import base64
import io

matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot_to_img_tag(df, title, xlabel, ylabel):
    plt.clf()

    plt.figure(figsize=(12, 6))

    # Plot each point's rate over time
    for point in df.columns[1:]:  # Skip the 'date' column
        plt.plot(df["date"], df[point], marker="o", label=point)

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
    if len(df) > 20:
        # Show approximately 15 evenly spaced ticks
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(15))

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)

    # Encode image to base64 string
    img_tag = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return img_tag