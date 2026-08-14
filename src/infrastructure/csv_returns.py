class CSVDailyReturnsProvider:
    """V0.2: stub — not yet used by the engine. Wired to establish the API."""

    def __init__(self, data_dir: str = "data/prices"):
        self.data_dir = data_dir

    def load(self, tickers: list[str], start: str, end: str):
        """V0.2: returns None. V0.3+: loads real data from CSV files."""
        return None