class Exporter:
 def to_csv(self, data, path):
 import csv
 with open(path, "w", newline="") as f:
 writer = csv.DictWriter(f, fieldnames=data[0].keys())
 writer.writeheader()
 writer.writerows(data)
