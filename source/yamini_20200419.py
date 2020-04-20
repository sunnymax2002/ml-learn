import pandas as pd

# Import DataFrame
df = pd.read_excel("D:\Learning\My Code\git_repos\ml-learn\datasets\yamini_20200419_input.xlsx")
print("\n\nInput DataFrame\n\n")
df.info()

# Create column index list, change as required
colIdx = []
c2voff = 4
for c in range(1, 5):
    colIdx.append([c, c + 4])

#print(colIdx)

# Output creation
dfo = pd.DataFrame(columns=['Visitor', 'Country', 'Discipline'])
#dfo.info()

for c, v in colIdx:
    colName = df.columns[c]
    countryVal = colName.split()[1]
    # Slice with column 'c' Not-Null, and select 'Visitor' and v columns
    slc = df[df[colName].notnull()].iloc[:, [0, v]]
    # Insert 'country' column
    slc.insert(1, 'Country', countryVal)
    #print(slc)
    # Rename columns of slice and append to dfo
    slc.columns = dfo.columns
    dfo = dfo.append(slc, ignore_index = True)

dfo.sort_values(by='Visitor', inplace=True)
print("\n\nOutput DataFrame\n\n")
print(dfo)
