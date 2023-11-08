import xlrd
import csv

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
            output_writer.writerow(current_sheet.row_values(row_num))
        else:
            for item in current_sheet.row(row_num):
                source_workbook_meta.write(item.value)
                source_workbook_meta.write('\t') #seperate it from next cell with tab

            #at the end of each line of metadata add a new line
            source_workbook_meta.write('\n')
            
    output_file.close()
    source_workbook_meta.close()
