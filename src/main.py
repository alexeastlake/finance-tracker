import csv
from datetime import datetime

transactions = []

class Transaction:
    def __init__(self, type, details, particulars, code, reference, amount, date, account = None, description = None, comments = None):
        self.type = type
        self.details = details
        self.particulars = particulars
        self.code = code
        self.reference = reference
        self.amount = float(amount)
        self.date = date
        
        self.account = account
        self.description = description
        self.comments = comments

    def equals(self, transaction):
        if self.type == transaction.type and self.details == transaction.details and self.particulars == transaction.particulars and self.code == transaction.code and self.reference == transaction.reference and self.amount == transaction.amount and self.date == transaction.date and self.account == transaction.account and self.description == transaction.description and self.comments == transaction.comments:
            return True
        
        return False

    def print(self):
        print("Type: ", self.type)
        print("Details: ", self.details)
        print("Particulars: ", self.particulars)
        print("Code: ", self.code)
        print("Reference: ", self.reference)
        print("Amount: ", self.amount)
        print("Date: ", self.date)

        print("Account: ", self.account)
        print("Description: ", self.description)
        print("Comments: ", self.comments)

def import_transactions(clean):
    importing = True

    print("---")
    print("Import, clean data = ", clean)
    print("---")

    while importing:
        try:
            path = input("Path: (r to return): ")
            
            if path == "r":
                importing = False
                break

            file = open(path)
            print("Opened file")

            reader = csv.DictReader(file)

            transactions_staging = []

            for row in reader:
                if clean:
                    transaction = Transaction(row["Type"], row["Details"], row["Particulars"], row["Code"], row["Reference"], row["Amount"], datetime.strptime(row["Date"], "%d/%m/%Y"), None, None, None)
                else:    
                    transaction = Transaction(row["type"], row["details"], row["particulars"], row["code"], row["reference"], row["amount"], datetime.strptime(row["date"], "%Y-%m-%d 00:00:00"), row["account"], row["description"], row["comments"])

                print("Loaded transaction: ")
                transaction.print()
                print()

                skip = False

                for existing_transaction in transactions:
                    if transaction.equals(existing_transaction):
                        print("Possible Duplicate:")
                        existing_transaction.print()
                        print()

                        skip = (input("Skip loading this transaction? (y/n): ") == "y")
                        print()
                        
                        if skip:
                            break
                
                if skip:
                    print("Skipped loading transaction")
                    continue

                transactions_staging.append(transaction)
                print("Staged transaction")
                print()
            print("Importing staged transactions...")
            for transaction in transactions_staging:
                transactions.append(transaction)
            
            transactions.sort(key = lambda x: x.date, reverse = True)

            print("Imported {} transactions".format(len(transactions_staging)))
        except Exception as e:
            print("An error occured while importing the file")
            print(e)

            continue
        finally:
            try:
                file.close()
                print("Closed file")
            except Exception as e:
                print("Failed to close file")
                print(e)

            print()

def add_transaction():
    adding = True

    print("---")
    print("Add")
    print("---")

    while adding:
        try:
            type = input("Type: ")
            details = input("Details: ")
            particulars = input("Particulars: ")
            code = input("Code: ")
            reference = input("Reference: ")
            amount = input("Amount: ")
            date = input("Date: ")
            account = input("Account: ")
            description = input("Description: ")
            comments = input("Comments: ")
            print()

            transaction = Transaction(type, details, particulars, code, reference, amount, datetime.strptime(date, "%d/%m/%Y"), account, description, comments)

            print("New Transaction -")
            transaction.print()

            print()
            confirm = input("Confirm (y/n)? ")
            print()

            if confirm:
                transactions.append(transaction)
                transactions.sort(key = lambda x: x.date, reverse = True)
        except Exception as e:
            print("An error occured while adding the transaction")
            print(e)

            adding = False

def sort_transactions():
    sorting = True

    print("---")
    print("Sort")
    print("---")

    while sorting:
        try:
            for i, transaction  in enumerate(transactions[:]):
                if not transaction.account:
                    current_sorting = True

                    while current_sorting:
                        print("Transaction - ")
                        transaction.print()
                        print()

                        split = input("Split (y/n)? ")
                        print()

                        print("Existing Accounts: ")
                        accounts = set(t.account for t in transactions)

                        for account in accounts:
                            print(account)
                        
                        print()

                        while split == "y":
                            print("New Transaction -")
                            amount = float(input("Amount (to split from original transaction): "))
                            account = input("Account: ")

                            description = input("Description: ")
                            comments = input("Comments: ")
                            print()

                            split_transaction = Transaction(transaction.type, transaction.details, transaction.particulars, transaction.code, transaction.reference, amount, transaction.date, account, description, comments)

                            transaction.amount -= amount

                            print("New Transaction -")
                            split_transaction.print()

                            print()
                            confirm = input("Confirm (y/n)? ")
                            print()

                            if confirm:
                                transactions[i] = transaction
                                transactions.append(split_transaction)
                            else:
                                continue
                            
                            split = input("Split (y/n)? ")

                            if split != "y":
                                print()
                                print("Original Transaction -")
                        
                        account = input("Account: ")
                        transaction.account = account
                        transaction.description = input("Description: ")
                        transaction.comments = input("Comments: ")

                        print("Updated Transaction- ")
                        transaction.print()
                        print()

                        confirm = input("Confirm (y/n)? ")
                        print()

                        if confirm == "y":
                            transactions[i] = transaction

                            current_sorting = False
                            break
                        else:
                            print()
            sorting = False
            transactions.sort(key = lambda x: x.date, reverse = True)
        except Exception as e:
            print("An error occured while sorting the transactions")
            print(e)

            sorting = False

def print_stats():
    stats = {}

    filter = input("Filter (y/n)? ")
    print()

    if filter == "y":
        description_substring = input("Description Search Substring: ")
        comments_substring = input("Comments Search Substring: ")
        print()
    else:
        description_substring = ""
        comments_substring = ""

    for transaction in transactions:
        if filter == "y":
            if (description_substring not in transaction.description) or (comments_substring not in transaction.comments):
                continue

        if transaction.account in stats.keys():
            stats[transaction.account] += transaction.amount
        elif transaction.account:
            stats[transaction.account] = transaction.amount
    
    print(stats)

def save_transaction():
    try:
        if len(transactions) <= 0:
            raise

        transactions_dicts = []

        for transaction in transactions:
            transactions_dicts.append(vars(transaction))
        
        fileName = datetime.now().strftime("%Y-%m-%d %H-%M-%S") + "_transactions.csv"
        file = open(fileName, mode = "w", newline = "")

        writer = csv.DictWriter(file, fieldnames = transactions_dicts[0].keys())
        writer.writeheader()
        
        for transaction in transactions_dicts:
            writer.writerow(transaction)
        
        file.close()

        print("Transactions saved to ", fileName)
    except Exception as e:
        print("An error occured while saving the transactions")
        print(e)

def main():
    running = True

    while running:
        try:
            selection = input("1 - Import clean data\n2 - Import dirty data\n3 - Sort uncategorized data\n4 - Add transaction\n5 - Generate Stats\n6 - Save data\n7 - Exit\n\nSelect: ")

            match selection:
                case "1":
                    import_transactions(False)
                case "2":
                    import_transactions(True)
                case "3":
                    sort_transactions()
                case "4":
                    add_transaction()
                case "5":
                    print_stats()
                case "6":
                    save_transaction()
                case "7":
                    running = False
        except Exception as e:
            print(e)
            running = False

if __name__ == "__main__":
    main()