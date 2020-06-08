#read single-line json prepared by Talend
f=open("E:/0_TAMU - MS MIS - Mays Business School/Semester 3/Advanced Database Management/Team Project/Phase2/sampleinv.json", "r")
if f.mode=="r":
    contents = f.read()

#conversion to multiline json string
contents = contents.replace("},","}\n")
contents = contents.replace("\"\\\"","\"")
contents = contents.replace("{\"data\":[","")
contents = contents.replace("}]}","}")
contents = contents.replace("[{","{")
new_contents = contents.replace("}]","}")

f.close()

#create mew file with converted multiline json string
f1 = open("E:/0_TAMU - MS MIS - Mays Business School/Semester 3/Advanced Database Management/Team Project/Phase2/final_aggregate_json.json", "w+")
f1.write(new_contents)
f1.close()


