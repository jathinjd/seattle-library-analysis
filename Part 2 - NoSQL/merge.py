path ='E:/0_TAMU - MS MIS - Mays Business School/Semester 3/Advanced Database Management/Team Project/Phase2/'

#prepare filepath for first input json
file1 = path + "final_aggregate_json.json"

#prepare filepath for second input json
file2 = path + "final_aggregate_json2.json"

#prepare filepath for final combined output json
file3 = path + "final_aggregate_combined_json.json"

filenames = [file1, file2]

#open files for combining
with open(file3, 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)