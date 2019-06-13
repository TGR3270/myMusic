import csv

Name = 'ジョージ'
City = 'ハワイ'

with open('person.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow([Name, City])

csvFile.close()
