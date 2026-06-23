class Document:
    REQUIRED_FIELDS = ["title", "document_number", "year", "division", "report_type"]
    SEARCH_FIELDS = [
        "title",
        "document_number",
        "author",
        "year",
        "division",
        "report_type",
        "investigation_type",
        "client",
        "platform_type",
    ]
