import json

#Set file locations and the filtered role 
file_loc = 'fine_tune_data/fine_tune_data.jsonl'
role = 'system'

#Create temporary location for the modified lines before rewriting to the outfile
modified_lines = []

def json_line_filter(infile_loc, outfile_loc, filter_role):

    with open(infile_loc, 'r', encoding = 'utf-8') as infile:
        for lines in infile:
            #Adding an error handling mechanism
            try:
                #loads the json line into a python dictionary, and parse it
                data = json.loads(lines.strip())
                #Call the 'messages' attribute with in the line dictionary
                messages = data.get('messages')

                #Setting a filter to filter out the unwanted message, and append in a single-line carrier
                filtered_message = []
                for msg in messages:
                    if msg['role'] != filter_role:
                        filtered_message.append(msg)

                #Re-format in the json form and convert the python object back to a json string
                filtered_message = {"messages": filtered_message}
                modified_line = json.dumps(filtered_message, ensure_ascii=False)
                modified_lines.append(modified_line)

            except json.JSONDecodeError:
            #If find out invalid lines, print them out and keep moving forward the program
                print(f'Skipping invalid line: {lines}')

    with open(outfile_loc, 'w', encoding = 'utf_8') as outfile:
        #Write the processed json lines to the outfile location
        for lines in modified_lines:
            outfile.write(lines.strip() + '\n')
        print(f'The processed jsonl file is successfully generated and stored at: {outfile_loc}')

    #To end the script
    return None

#Running the script
if __name__ == '__main__':
    json_line_filter(infile_loc = file_loc, outfile_loc = file_loc, filter_role = role)