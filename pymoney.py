#!/usr/bin/env python3
import sys

class Record:
    """Represent a record."""
    def __init__(self, category, name, amount):
        """Initialize the record."""
        self._category = category
        self._name = name
        self._amount = int(amount)

    def __repr__(self):
        return self.__class__.__name__ + repr((self._category, self._name, self._amount))
    
class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """Initialize the records."""
        try:
            fh = open("records.txt", 'r')
        except FileNotFoundError:
            try:
                self._initial_money = int(input("How much money do you have? "))
            except:
                sys.stderr.write("Invalid value for money.\nSet to 0 by default.\n")
                self._initial_money = 0
            self._records = []
        else:
            begin = fh.readline()
            if (begin == ""):
                sys.stderr.write("Invalid format in records.txt. Deleting the contents.\n")
                try:
                    self._initial_money = int(input("How much money do you have? "))
                except:
                    sys.stderr.write("Invalid value for money.\nSet to 0 by default.\n")
                    self._initial_money = 0
                self._records = []
            else:
                try:
                    self._initial_money = int(begin)
                except:
                    sys.stderr.write("Invalid format in records.txt. Deleting the contents.\n")
                    try:
                        self._initial_money = int(input("How much money do you have? "))
                    except:
                        sys.stderr.write("Invalid value for money.\nSet to 0 by default.\n")
                        self._initial_money = 0
                    self._records = []
                self._records = []
                rl = fh.readlines()
                for i in rl:
                    if '\n' in i:
                        i = i[:-1]
                    new = Record(i.split()[0], i.split()[1], i.split()[2])
                    self._records.append(new)
                print("Welcome back!")
    
    def add(self, record, categories):
        """Add a record."""
        try: # check if the element can be split into 3 strings
            new_record = Record(record.split()[0], record.split()[1], record.split()[2]) 
        except IndexError:
            sys.stderr.write("The format of a record should be like this: meal breakfast -50.\nFail to add a record.\n")
        except ValueError:
            sys.stderr.write("Invalid value for money.\nFail to add a record.\n")
        else:
            if (categories.is_category_valid(new_record._category)):
                self._records.append(new_record)
                self._initial_money += new_record._amount
            else:
                print('The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a record.')
        return

    def view(self):
        """View the records."""
        print("Here's your expense and income records:")
        print("Category        Description          Amount")
        print("=============== ==================== ======")
        for i in self._records:
            print(i._category, end = "")
            print(" " * (16 - len(i._category)), end = "")
            print(i._name, end = "")
            print(" " * (21 - len(i._name)), end = "")
            print(i._amount)    
        print("=============== ==================== ======")
        print(f"Now you have {self._initial_money} dollars.")

    def delete(self, delete_record):
        """Delete a record."""
        dlist = []
        if (delete_record == '#all'):
            dmoney = 0
            for i in self._records:
                dmoney += i._amount
            self._initial_money -= dmoney
            self._records.clear()
            print("All records have been deleted.")
        else:
            try:
                d = Record(delete_record.split()[0], delete_record.split()[1], delete_record.split()[2]) 
            except IndexError:
                sys.stderr.write("The format to delete a record should be like this: meal breakfast -50.\nFail to delete a record.\n")
            except ValueError:
                sys.stderr.write("Invalid value for money.\nFail to dlete a record.\n")
            else:
                for i in self._records:
                    if (delete_record.split()[0] == i._category and delete_record.split()[1] == i._name and int(delete_record.split()[2]) == i._amount):
                        dlist.append(i)
                if (len(dlist) <= 0):
                    sys.stderr.write(f"There's no record with \"{delete_record}\". Fail to delete a record.\n'")
                elif (len(dlist) >= 2):
                    print(f"The amount of '{delete_record}' is larger than 1, ")
                    t = input("enter which you want to delete by the time order: ")
                    tlist = [index for (index, r) in enumerate(self._records) if delete_record.split()[0] == r._category and delete_record.split()[1] == r._name and int(delete_record.split()[2]) == r._amount] # set time order to the same items with same prices
                    try:
                        del(self._records[tlist[int(t) - 1]])
                        self._initial_money -= dlist[0]._amount
                    except:
                        sys.stderr.write(f'There are not such many "{delete_record}"". Fail to delete a record.\n')
                else:
                    self._initial_money -= dlist[0]._amount
                    self._records.remove(dlist[0])

    def find(self, category, target_categories):
        """Find a specified category with the records."""
        money = 0
        print("Here's your expense and income records under category", f'"{category}":')
        print("Category        Description          Amount")
        print("=============== ==================== ======")
        plist = list(filter(lambda x: x._category in target_categories, self._records))
        for i in plist:
            print(i._category, end = "")
            print(" " * (16 - len(i._category)), end = "")
            print(i._name, end = "")
            print(" " * (21 - len(i._name)), end = "")
            print(i._amount)
            money += i._amount
        print("=============== ==================== ======")
        print(f"The total amount above is {money}.")
        return

    def search(self, k):
        """Search for a specified keyword in the records."""
        money = 0
        klist = []
        for i in self._records:
            if (k in i._category) or (k in i._name) or (k in str(i._amount)):
                klist.append(i)
        print("Here's your search for the keyword", f'"{k}":')
        print("Category        Description          Amount")
        print("=============== ==================== ======")
        for i in klist:
            print(i._category, end = "")
            print(" " * (16 - len(i._category)), end = "")
            print(i._name, end = "")
            print(" " * (21 - len(i._name)), end = "")
            print(i._amount)
            money += i._amount
        print("=============== ==================== ======")
        print(f"The total amount above is {money}.")
        return

    def edit(self, edit_record, categories):
        """Edit a record."""
        elist = []
        try:
            e = Record(edit_record.split()[0], edit_record.split()[1], edit_record.split()[2]) 
        except IndexError:
            sys.stderr.write("The format to choose a record to edit should be like this: meal breakfast -50.\nFail to edit a record.\n")
        except ValueError:
            sys.stderr.write("Invalid value for money.\nFail to edit a record.\n")
        else:
            for i in self._records:
                if (edit_record.split()[0] == i._category and edit_record.split()[1] == i._name and int(edit_record.split()[2]) == i._amount):
                    elist.append(i)
            if (len(elist) <= 0):
                sys.stderr.write(f"There's no record with \"{edit_record}\". Fail to edit a record.\n")            
            else:
                if (len(elist) >= 2):
                    print(f"The amount of \"{edit_record}\" is larger than 1, ")
                    t = input("enter which you want to edit by the time order: ")
                else:
                    t = 1
                elist = [index for (index, r) in enumerate(self._records) if edit_record.split()[0] == r._category and edit_record.split()[1] == r._name and int(edit_record.split()[2]) == r._amount] # set time order to the same items with same prices
                cmd = input(f"Which property do you want to edit for \"{edit_record}\"? ")
                if (cmd == "category"):
                    change = input(f"What category do you want to change for \"{edit_record}\"? ")
                    if (categories.is_category_valid(change)):
                        self._records[elist[int(t) - 1]]._category = change
                    else:
                        print('The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to edit a record.')
                elif (cmd == "name"):
                    change = input(f"What name do you want to change for \"{edit_record}\"? ")
                    self._records[elist[int(t) - 1]]._name = change
                elif (cmd == "amount"):
                    change = input(f"What amount do you want to change for \"{edit_record}\"? ")
                    self._initial_money -= self._records[elist[int(t) - 1]]._amount
                    self._records[elist[int(t) - 1]]._amount = int(change)
                    self._initial_money += int(change)
                else:
                    sys.stderr.write(f"There's no property of \"{cmd}\". Fail to edit a record.\n")
                print(f"The record \"{edit_record}\" has been changed to \"{self._records[elist[int(t) - 1]]._category} {self._records[elist[int(t) - 1]]._name} {self._records[elist[int(t) - 1]]._amount}\".")
        return

    def save(self):
        """Save the records."""
        # calculate the total money
        s = []
        with open("records.txt", 'w') as fh:
            fh.write(str(self._initial_money) + '\n')
            for i in self._records:
                s.append(' '.join([i._category, i._name, str(i._amount)]))
            InToFile = '\n'.join(s)
            fh.writelines(InToFile)
        return

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """Initialize the categories."""
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway'], 'clothing', ['clothes', 'pants', 'coat'], 'entertainment', 'study'], 'income', ['salary', 'bonus', 'investment']]

    def view(self):
        """View the categories."""
        def view_categories(clist, level = 0):
            if (clist == None):
                return
            if type(clist) == list:
                for i in clist:
                    view_categories(i, level + 1)
            else:
                print(f"{' ' * (level * 2 - 2)}- {clist}")
            return
        
        return view_categories(self._categories)

    def is_category_valid(self, category):
        """Check if the category is valid."""
        def check_category_valid(category, categories):
            if categories == None:
                return False
            if type(categories) == list:
                for i in categories:
                    p = check_category_valid(category, i)
                    if p == True:
                        return True
            else:
                return category == categories

        return check_category_valid(category, self._categories)

    def find_subcategories(self, category):
        """Find the subcategories of a category."""
        def find_subcategories_gen(category, categories, found = False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) \
                        and type(categories[index + 1]) == list:
                        # When the target category is found,
                        # recursively call this generator on the subcategories
                        # with the flag set as True.
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                if categories == category or found == True:
                    yield categories

        return [i for i in find_subcategories_gen(category, self._categories)]

#my code
categories = Categories()
records = Records()

while True:
    command = input("\nWhat do you want to do (add / view / delete / view categories / find / search / edit / exit)? ")
    if (command == "add"):
        record = input("Add an expense or income record with description and amount:\n")
        records.add(record, categories) 
    elif (command == "view"):
        records.view()
    elif (command == "delete"):
        delete_record = input("Which record do you want to delete? ")
        records.delete(delete_record)
    elif (command == "view categories"):
        categories.view()
    elif (command == "find"):
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        records.find(category, target_categories)
    elif (command == "search"):
        key = input("Which keyword do you want to search? ")
        records.search(key)
    elif (command == "edit"):
        edit_record = input("Which record do you want to edit? ")
        records.edit(edit_record, categories)
    elif (command == "exit"):
        records.save()
        break
    else:
        sys.stderr.write("Invalid command. Try again.\n")
        continue