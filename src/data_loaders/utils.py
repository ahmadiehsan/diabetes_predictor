import pandas as pd


class CSVLoader:
    csv_x_fields = [
        'pregnant_times',
        'plasma_glucose',
        'blood_pressure',
        'skinfold_thickness',
        'serum_insulin',
        'body_mass_index',
        'pedigree_function',
        'age',
    ]
    csv_y_field = 'class_variable'
    csv_all_fields = [*csv_x_fields, csv_y_field]

    def __init__(self, csv_file_path):
        dataframe = pd.read_csv(csv_file_path, names=self.csv_all_fields)
        dataframe.drop_duplicates(inplace=True)

        self._x = dataframe[self.csv_x_fields]
        self._y = dataframe[self.csv_y_field]

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
