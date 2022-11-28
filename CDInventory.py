#-------------------------------------------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# AMorgan, 2022-Nov-20, Edited File
# AMorgan, 2022-Nov-27, Edited File for error handling and saving as binary data
#-------------------------------------------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file'
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def add_inventory(strID, strTitle, strArtist):
        """Applies user input to add a CD to the inventory table

        Args:
            strID (string): the ID of the CD to be added
            strTitle (string): the title of the CD to be added
            strArtist (string): the artist of the CD to be added
            
        Returns:
            lstTbl (list of lists): the CD inventory table, now with a new CD added
        """
        intID = int(strID)
        try:
            for row in lstTbl:
                for ID in row.values():
                    if ID == intID:
                        raise Exception("The ID is already taken. Please try again with a new ID.")
            dicRow = {'ID': intID, 'Title': strTitle, 'Artist': strArtist}
            lstTbl.append(dicRow)
        except Exception as e:
            print("CD was not successfully added.")
            print(e)
        return lstTbl
    
    @staticmethod    
    def del_inventory(intIDDel):
        """Applies user input to delete a CD from the inventory table

        Args:
          intIDDel (integer): the ID of the CD to be removed
          
        Returns:
          lstTbl (list of lists): the CD inventory table, now with a CD removed
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        return lstTbl

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from binary data file identified by file_name into a 2D table

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            with open(file_name, 'rb') as fileObj:
                table = pickle.load(fileObj)
            return table
        except FileNotFoundError as e:
            print('File does not exist!')
            print(e)
        except Exception as e:
            print('There was a general error!')
            print(e)
        

    @staticmethod
    def write_file(file_name, table):
        """Function to write the CD inventory data in memory to a binary data file, replacing what is already in the file.

        Writes the data from the list of dicts table in memory into a binary data file.

        Args:
            file_name (string): name of file to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        with open(file_name, 'wb') as fileObj:
            pickle.dump(table, fileObj)
        

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        try:
           print('======= The Current Inventory: =======')
           print('ID\tCD Title (by: Artist)\n')
           for row in table:
               print('{}\t{} (by:{})'.format(*row.values()))
           print('======================================')
        except:
            print("No data to display")
    @staticmethod
    def add_inventory_menu():
        """Gets user inputs to add a CD to the inventory table


        Args:
            None.

        Returns:
            strID (string): the ID of the CD to be added
            strTitle (string): the title of the CD to be added
            strArtist (string): the artist of the CD to be added

        """
        while True:
            strID = input('Enter ID: ').strip()
            try:
                intID = int(strID)
                break
            except ValueError as e:
                print('ID must be an integer!')
                print(e)
            except Exception as e:
                print('There was a general error!')
                print(e)
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, strArtist

# -- PROCESSING -- #

# 1. When program starts, read in the currently saved Inventory
try:
    FileProcessor.read_file(strFileName, lstTbl)
except FileNotFoundError as e:
    print('File does not exist!')
    print(e) 
    pass
except Exception as e:
    print('There was a general error!')
    print(e)
    pass

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, strArtist = IO.add_inventory_menu()
        # 3.3.2 Add item to the table
        DataProcessor.add_inventory(strID, strTitle, strArtist)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except ValueError as e:
                print('ID must be an integer!')
                print(e)
            except Exception as e:
                print('There was a general error!')
                print(e)
        # 3.5.2 search thru table and delete CD
        DataProcessor.del_inventory(intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




