import xlrd
import csv

from numbers import Number 
from datetime import datetime


source_workbook = xlrd.open_workbook('fredgraph.xls')

source_workbook_meta = open('ferdgraph_meta.txt', 'w')

# an excel can have multiple sheets:
for sheet_name in source_workbook.sheet_names():
    current_sheet = source_workbook.sheet_by_name(sheet_name)
    output_file = open('xls_'+sheet_name+'.csv', 'w')
    output_writer = csv.writer(output_file) # write to csv 
    is_table_data = False #flag variable to detecht if we hit our table-type data yet

    for row_num, row in enumerate(current_sheet.get_rows()):
        # pulling out the value in the first column of current row
        first_entry = current_sheet.row_values(row_num)[0]

        if first_entry == 'observation_date': #header row of table data
            is_table_data = True

        if is_table_data:
            # extract the table-type values into seperate variables
            the_date_num = current_sheet.row_values(row_num)[0]
            U6_value = current_sheet.row_values(row_num)[1]

            # create a new row object with each of the values
            new_row = [the_date_num, U6_value]

            # if the_date_num is number then the current row is NOT the header row
            # So we need to transform the date:
            if isinstance(the_date_num, Number):
                the_date_num = xlrd.xldate_as_datetime(the_date_num, source_workbook.datemode)

                #overwite the first value in the new row tith the reformatted date
                new_row[0] = the_date_num.strftime('%m/%d/%Y')
            output_writer.writerow(new_row)
        #otherwise this row should be metadata
        
        else:
            for item in current_sheet.row(row_num):
                source_workbook_meta.write(item.value)
                source_workbook_meta.write('\t') #seperate it from next cell with tab

            #at the end of each line of metadata add a new line
            source_workbook_meta.write('\n')

    output_file.close()
    source_workbook_meta.close()
