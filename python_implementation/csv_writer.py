import csv
import os


class CsvWriter:
    def __new__(cls):
        # TODO initialize attributes in the constructor
        if not hasattr(cls, 'instance'):
            cls.instance = super(CsvWriter, cls).__new__(cls)
        return cls.instance

    def write(self, data, file_path, labels, item_to_row_func=None, overwrite=False):
        file_name = f"{file_path}.csv"
        if not overwrite:
            result_id = 0
            while os.path.exists(file_name):
                result_id += 1
                file_name = f"{file_path}{result_id}.csv"

        with open(file_name, mode='w', newline='') as csvfile:
            # Creazione dell'oggetto writer
            writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=labels)
            # Scrittura dell'header (nomi delle colonne)
            writer.writeheader()
            # Scrittura dei dati
            for row in data:
                if item_to_row_func is not None:
                    row = item_to_row_func(row)
                writer.writerow(row)

    def read(self, file_path):
        result = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=";")
            for line in reader:
                result.append(line)
        return result

if __name__ == '__main__':
    result = CsvWriter().read("../partial_results/community.csv")