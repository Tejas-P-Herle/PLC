ESCAPE_CHARS = "+*?^$\.[]{}()|/"

class DataBase:
    def __init__(self, langs):
        """Initiation method of DataBase Class"""
        
        # Initiate class attriburtes
        self.langs = langs
        self.sl_one_offset = None
        self.cols = None

        self.collect_file_details()

    def collect_file_details(self):
        """Collect required file details and store it"""

        # Read first line from db
        self.headings = headings = self.read(sl_no="sl_no")
        print("headings", headings)
        self.cols = [i for i, col in enumerate(headings) if col in self.langs]
        self.total_cols = len(headings) - 1
        with open("regex_gen_data.db") as db:
            db.readline()
            self.sl_one_offset = db.tell()
            total_rows = 0
            while db.readline():
                total_rows += 1
        self.total_rows = total_rows

    def make_data_str(self, data_list, re_id):
        """Make data string to be added to database"""

        data_a, data_b = [d.replace(",", "\\,") for d in data_list]
        cols = self.cols
        data = str(re_id) + " , " * (cols[0]) + data_a
        data += " , " * (cols[1] - cols[0]) + data_b
        data += " , " * (self.total_cols - cols[1]) + "\n"
        return data

    def erase(self, sl_no, db_name="regex_gen_data.db"):
        """Erase the given line from the file"""

        # Write an empty line instead of the existing line
        self.write("", sl_no=sl_no)
        
    def write(self, data, db_name="regex_gen_data.db",
                    mode=None, sl_no=None):
        """Open database connection"""

        # Open connction
        db = open(db_name, "r+" if mode else "a")

        # Check if data exists in database
        if self.exists(data):
            return

        # Overwrite requested line
        data = data if isinstance(data, list) else [data]
        if sl_no:
            
            # Iterate through all lines in database
            offset = 0
            lns = data
            store = False
            ln = db.readline()
            while ln:

                # Start storing future lines if line is required line
                if ln.split(" , ", 1)[0] == sl_no:
                    store = True
                elif store:
                    lns.append(ln)
                else:
                    offset = db.tell()
                ln = db.readline()

            # Clear all lns after specified ln, overwrite with input data
            db.truncate(offset)
            db.seek(offset)
            db.writelines(lns)

        # Else append to end of file
        else:
            db.writelines(data)

    def exists(self, entry, db_name="regex_gen_data.db"):
        """Check if the given entry is in database"""

        # Iterate over lines in database and check equality of entries
        entry = entry.rstrip("\n").split(" , ")[1:]
        for ln in self.read():
            ln.pop(0)
            if ln == entry:
                return True
        return False

   #  def is_regex(self, ln):
   #      """Check if the given line is a regex expression"""
   #      
   #      ln = ln.split(" , ") if isinstance(ln, str) else ln
   #      if ln[0].endswith("r"):
   #          return True
   #      return False
    
    def read(self, db_name="regex_gen_data.db", sl_no=None):
        """Get read database"""
        
        # Open database connection
        db = open(db_name)

        if sl_no:

            # Return requested ln
            try:
                # If headings are requested, return first line of file
                if sl_no == "sl_no":
                    return next(self.read_ln(db, skip=False))
                return self.get_ln(sl_no, db)
            finally:
                if db:
                    db.close()
        else:

            # Return generator object of read line function
            return self.read_ln(db)

    def get_ln(self, sl_no, db):
        """Get particular line from database"""

        # Search line with requested line number
        for ln in self.read_ln(db, skip=False):
            if ln[0] == sl_no:
                return ln

    def read_ln(self, db, skip=True):
        """Read the next line from the file"""
        
        try:

            # Skip over heading line
            if db.tell() == 0 and skip:
                db.seek(self.sl_one_offset)

            # Else retrieve previous cursor position and read next line
            ln = db.readline()
            ln = ln.replace("\\,", ",").rstrip("\n").split(" , ")
            while ln != [""]:
                yield ln
                ln = db.readline().replace("\\,", ",").rstrip("\n")
                ln = ln.split(" , ")
        finally:
            if db:
                db.close()

