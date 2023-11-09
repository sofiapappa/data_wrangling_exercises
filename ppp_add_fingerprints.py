
import csv
import fingerprints

ppp_data = open('public_150k_plus_230930.csv','r')

ppp_data_reader = csv.DictReader(ppp_data)
print(ppp_data_reader.fieldnames)

augment_ppp_data = open('public_150k_plus_fingerprints.csv', 'w') # for writing the modified dataset

augmented_data_writer = csv.writer(augment_ppp_data) # to output whole rows at once



header_row = []
# for loop to create a new header row
for item in ppp_data_reader.fieldnames:
    header_row.append(item)
    if item == 'OriginatingLender':
        header_row.append('OriginatingLenderFingerprint') # add a new column
    augmented_data_writer.writerow(header_row)

for row in ppp_data_reader:
    new_row = [] # empty list to hold the new data row
    for col_name in ppp_data_reader.fieldnames:
        new_row.append(row[col_name])
        if col_name == 'OriginatingLender':
            the_fingerprint = fingerprints.generate(row[col_name]) + '' + row['OriginatingLenderLocationID']
            new_row.append(the_fingerprint)
    augmented_data_writer.writerow(new_row)
augment_ppp_data.close()



