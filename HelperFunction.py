class HelperFunctions():
    """
    Docstring for HelperFunctions
    """

    def __init__(self, MDB_connectionString):
        self.mongoDBConnectionString = MDB_connectionString

    def constructScrapingList(self, start_date, end_date):
        """
        Docstring for constructScrapingList
        
        Args:
            start_date: Start date to get docs, format dd/MM/YYYY Ex: 7/10/2025 or 13/10/2025
            end_date: End date to get docs, format dd/MM/YYYY Ex: 7/10/2025 or 13/10/2025
        """
        pass