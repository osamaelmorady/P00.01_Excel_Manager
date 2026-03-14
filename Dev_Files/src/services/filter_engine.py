class FilterEngine:

    def __init__(self, data):

        self.original_data = data
        self.active_filters = {}

    def apply_filter(self, column, value):

        self.active_filters[column] = value

        data = self.original_data

        for col, val in self.active_filters.items():

            data = [
                row for row in data
                if col < len(row) and str(row[col]) == str(val)
            ]

        return data

    def clear_filters(self):

        self.active_filters = {}

        return self.original_data

    def unique_values(self, column):
    
        values = set()
    
        for row in self.original_data:
        
            if column < len(row):
            
                val = row[column]
    
                if val is not None and val != "":
                    values.add(str(val))
    
        return sorted(values)