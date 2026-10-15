"""
Week 3 Mini Project: File Handling & Libraries
Covers:
1. Read a file and count total lines.
2. Merge two text files.
3. Use Pandas to load and analyze a CSV file.
4. Use Matplotlib to plot a line graph.
5. Create a JSON file and read data from it.

Run:
    python main.py
"""

from pathlib import Path
import json
import sys

try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("A required library is missing.")
    print("Install dependencies using: pip install -r requirements.txt")
    print(f"Details: {exc}")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


def count_lines(file_path: Path) -> int:
    """Return the number of lines in a UTF-8 text file."""
    with file_path.open("r", encoding="utf-8") as file:
        return sum(1 for _ in file)


def merge_text_files(file_one: Path, file_two: Path, output_path: Path) -> None:
    """Merge two text files into one, preserving their contents."""
    with output_path.open("w", encoding="utf-8") as output:
        for source_path in (file_one, file_two):
            with source_path.open("r", encoding="utf-8") as source:
                content = source.read()
            output.write(content)
            if content and not content.endswith("\n"):
                output.write("\n")


def analyze_csv(csv_path: Path) -> pd.DataFrame:
    """Load a CSV file, print a useful summary, and return its DataFrame."""
    df = pd.read_csv(csv_path)
    print("\n--- CSV DATA PREVIEW ---")
    print(df.head().to_string(index=False))
    print("\n--- DATASET INFORMATION ---")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print("\n--- NUMERICAL SUMMARY ---")
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        print("No numeric columns found.")
    else:
        print(numeric.describe().round(2).to_string())
    if "Sales" in df.columns:
        print(f"\nTotal sales: {df['Sales'].sum():.2f}")
        if "Month" in df.columns:
            print("\nSales by month:")
            print(df.groupby("Month", as_index=False)["Sales"].sum().to_string(index=False))
    return df


def plot_line_graph(df: pd.DataFrame, image_path: Path) -> None:
    """Plot sales by month if possible, otherwise plot the first two columns."""
    if {"Month", "Sales"}.issubset(df.columns):
        x = df["Month"]
        y = df["Sales"]
        x_label, y_label = "Month", "Sales"
        title = "Monthly Sales Trend"
    elif len(df.columns) >= 2:
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]
        x_label, y_label = str(df.columns[0]), str(df.columns[1])
        title = f"{y_label} by {x_label}"
    else:
        print("Not enough columns to create a line graph.")
        return

    plt.figure(figsize=(9, 5))
    plt.plot(x, y, marker="o")
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(image_path, dpi=150)
    plt.close()
    print(f"\nLine graph saved to: {image_path}")


def create_and_read_json(json_path: Path) -> None:
    """Create a sample JSON file, then read and display its contents."""
    sample_data = {
        "project": "Week 3 File Handling & Libraries",
        "student": "Student Name",
        "topics": [
            "File handling",
            "Pandas CSV analysis",
            "Matplotlib line graph",
            "JSON read/write"
        ],
        "status": "Completed"
    }
    with json_path.open("w", encoding="utf-8") as file:
        json.dump(sample_data, file, indent=4)

    with json_path.open("r", encoding="utf-8") as file:
        loaded_data = json.load(file)

    print("\n--- JSON DATA READ BACK ---")
    print(json.dumps(loaded_data, indent=4, ensure_ascii=False))


def ensure_sample_files() -> None:
    """Create example input files if they do not already exist."""
    first = DATA_DIR / "file1.txt"
    second = DATA_DIR / "file2.txt"
    csv_path = DATA_DIR / "monthly_sales.csv"

    if not first.exists():
        first.write_text(
            "Python supports file handling.\nFiles can store text data.\n",
            encoding="utf-8"
        )
    if not second.exists():
        second.write_text(
            "Pandas can analyze tabular data.\nMatplotlib can create graphs.\n",
            encoding="utf-8"
        )
    if not csv_path.exists():
        csv_path.write_text(
            "Month,Sales,Expenses\n"
            "January,12000,8000\n"
            "February,14500,9200\n"
            "March,13200,8700\n"
            "April,16800,10100\n"
            "May,17500,10900\n"
            "June,19000,11500\n",
            encoding="utf-8"
        )


def main() -> None:
    ensure_sample_files()

    file_one = DATA_DIR / "file1.txt"
    file_two = DATA_DIR / "file2.txt"
    merged_file = OUTPUT_DIR / "merged.txt"
    csv_file = DATA_DIR / "monthly_sales.csv"
    graph_file = OUTPUT_DIR / "monthly_sales.png"
    json_file = OUTPUT_DIR / "project_data.json"

    print("=" * 55)
    print("WEEK 3 MINI PROJECT: FILE HANDLING & LIBRARIES")
    print("=" * 55)

    print(f"\n1. Lines in {file_one.name}: {count_lines(file_one)}")
    merge_text_files(file_one, file_two, merged_file)
    print(f"2. Files merged successfully: {merged_file}")

    df = analyze_csv(csv_file)
    plot_line_graph(df, graph_file)

    create_and_read_json(json_file)

    print("\nAll five tasks completed successfully.")
    print(f"Input files are in: {DATA_DIR}")
    print(f"Generated files are in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
