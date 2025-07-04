import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuration ---
CLUSTERED_DATA_FILE = "data/clustered_jobs.csv"
VISUALIZATION_FILE = "data/cluster_visualization.png"


def visualize_clusters(file_path, output_path):
    """
    Loads clustered job data and creates a 2D scatter plot visualization.
    """
    print(f"Loading clustered data from {file_path}...")
    df = pd.read_csv(file_path)

    # Separate noise points from actual clusters for better visualization
    noise_df = df[df["cluster"] == -1]
    clustered_df = df[df["cluster"] != -1]

    print("Generating cluster visualization...")
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot noise points first, in the background
    ax.scatter(
        noise_df["x"],
        noise_df["y"],
        c="lightgray",
        s=5,
        alpha=0.5,
        label="Noise",
    )

    # Plot the actual clusters
    scatter = ax.scatter(
        clustered_df["x"],
        clustered_df["y"],
        c=clustered_df["cluster"],
        s=50,
        alpha=0.8,
        cmap="viridis",
    )

    # Aesthetics and labels
    ax.set_title("2D Visualization of Job Description Clusters", fontsize=16)
    ax.set_xlabel("UMAP Dimension 1", fontsize=12)
    ax.set_ylabel("UMAP Dimension 2", fontsize=12)
    legend = ax.legend(
        *scatter.legend_elements(),
        title="Clusters",
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
    )
    ax.add_artist(legend)
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # Save the plot
    print(f"Saving visualization to {output_path}...")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print("Done.")


def main():
    """Main function to run the visualization pipeline."""
    visualize_clusters(CLUSTERED_DATA_FILE, VISUALIZATION_FILE)


if __name__ == "__main__":
    main()
