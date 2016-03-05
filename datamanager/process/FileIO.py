'''
THIS CODE IS CURRENTLY NOT USED AND ARE KEPT FOR REFERENCE ALONE
'''

import csv
import os

class csvio(object):
    """description of class"""

    def __init__(self):
        """

        """

        self.header = ['Code', 'PriceDate','PriceOpen','PriceHigh','PriceLow','PriceClose', 'Volume']

    def create_path(self, code, exchange):
        """

        """
        filename = exchange + '_' + code +'.csv'
        fp = os.path.join(r'D:\Data\FinancialData\CSV\Price\Daily\History', exchange, filename)

        return fp;

    #Specific methods
    def read_infochimps(self, _filepath):
        """

        """
        lastcode = ''
        newcode = False

        with open(_filepath,'rb') as srcfile:
            csvreader = csv.reader(srcfile)

            for row in csvreader:
                exchange = row[0]
                code = row[1]

                data = row[1:len(row)-1]

                if csvreader.line_num == 1:
                    # currently reading header
                    firstline = True;
 
                elif lastcode != code:
                    # code has changed from previous row
                    newcode = True
                    # output current instrument code to console
                    print(code)

                if newcode:
                    fp = self.create_path(code,exchange)
                    # open/create file and write header to file
                    destfile = open(fp, 'wb')
                    rowWriter = csv.writer(destfile, delimiter=',')
                    rowWriter.writerow(header)
                    rowWriter.writerow(data)
                    newcode = False
                elif firstline:
                    header = data
                    firstline = False
                else:
                    # write data to file
                    rowWriter.writerow(data)
        
                lastcode = code

            destfile.close()

    def read_sharenet(self, _filepath):
        """
        Read data from Sharenet data service files

        INCOMPLETE:

        - Exception handling
        """
        
        lastcode = ''
        newcode = False

        with open(_filepath,'rb') as srcfile:
            csvreader = csv.reader(srcfile)

            # skip headings
            csvreader.next()
            csvreader.next()
            csvreader.next()
            csvreader.next()
            csvreader.next()

            for row in csvreader:
                try:
                    exchange = row[1]
                    code = row[2]

                    date = row[5][0:4]+'/'+row[5][4:6]+'/'+row[5][6:8]
                
                    data = [code,date,row[6],row[7],row[8],row[9],row[10]]

                    if lastcode != code:
                        # code has changed from previous row
                        newcode = True
                        # output current instrument code to console
                        print(code)

                    if newcode:
                        fp = self.create_path(code,exchange)

                        if os.path.isfile(fp):
                            # file already exists
                            try:
                                destfile = open(fp, 'a');
                                rowWriter = csv.writer(destfile, delimiter=',')
                                rowWriter.writerow(data)
                            except:
                                print('Some error')
                            finally:
                                destfile.close()
                        else:
                            # create file and write header to file
                            try:
                                destfile = open(fp, 'wb');
                                rowWriter = csv.writer(destfile, delimiter=',')
                                rowWriter.writerow(header)
                                rowWriter.writerow(data)
                            except:
                                print('Some error')
                            finally:
                                destfile.close()

                        newcode = False
                except:
                    print('Some error')
                finally:    
                    lastcode = code

    def fileMaintenance(self, _dir):
        """

        """

        file = open(_dir + '\\dirlist.txt')
        csvreader = csv.reader(file, delimiter='\n')        

        for row in csvreader:
            filename = row[0]
            print('Open file: ' + filename)

            path = _dir + '\\'+ filename
            new_fn = self.del_emptyrows(path)
            self.del_file(path)
            self.ren_file(new_fn, path)
            print('Finished with: ' + filename    )
            print('')

        file.close()       

    def merge(self, src, tgt):
        """
        Merge the data in two csv files together by merging the source file to the target file
        src: Source file name -full path
        tgt: Target file name -full path
        """

        # open source file
        input1 = open(src,'rb')
        out_fn = src + 'temp'
        output = open(out_fn, 'ab')
        
        csvreader = csv.reader(input1)
        # extract all data in source file into memory


        # open target file

        # extract all data in target file into memory

        # merge the two data sets        

        # write data to temporary file
        writer = csv.writer(output)
        heading = csvreader.next()

        """
        data = [csvreader.next()]

        for row in csvreader:
            # add data to list
            data.append(row)
            writer.writerow(row)

        input1.close()

        input2 = open(tgt, 'rb')
        csvreader = csv.reader(input2)

        for row in csvreader:
            # check if data already in list
            if row in data:
                writer.writerow(row)

        input2.close()
        output.close()

        self.del_file(_part1)
        self.ren_file(out_fn, _part1)
        """

    # Private methods
    def del_emptyrows(self, _fn):
        """

        """
        input = open(_fn, 'rb')
        out_fn = _fn + 'temp'
        output = open(out_fn, 'wb')

        writer = csv.writer(output)
        for row in csv.reader(input):
            if row:
                writer.writerow(row)
        input.close()
        output.close()

        return out_fn

    def del_file(self, _path):
        """
        Delete file at filepat _path
        """
        os.remove(_path)

    def ren_file(self, curname, newname):
        """
        Rename file from curname to newname
        """

        os.rename(curname, newname)

    