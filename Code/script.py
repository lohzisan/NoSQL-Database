import json
import os
import re
from cmd import Cmd
from itertools import groupby
from operator import itemgetter


class MyDB(Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = 'MyDB > '
        self.table = None
        self.data = []

    def do_create(self, line):
        try:
            self.table = line.strip()
            if os.path.exists(f'{self.table}.json'):
                print("Table already exists.")
                return

            with open(f'{self.table}.json', 'w') as f:
                json.dump([], f)
            print(f"Table {self.table} created.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def do_insert(self, line):
        try:
            if not self.table:
                print("No table selected.")
                return
            
            data = json.loads(line)
            with open(f'{self.table}.json', 'r+') as f:
                current_data = json.load(f)
                current_data.append(data)
                f.seek(0)
                json.dump(current_data, f, indent=2)
            print("Data inserted.")
        except Exception as e:
            print(f"Error inserting data: {e}")

    def do_load(self, table):
        try:
            with open(f'{table.strip()}.json', 'r') as f:
                self.data = json.load(f)
                self.table = table.strip()
            print(f"Data loaded from {self.table}.json.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def do_find(self, line):
        if self.table is None:
            print("No table is loaded/selected.")
            return

        try:
            # Corrected regular expression pattern
            match = re.search(r"\w+ whose (\w+) is (.+)", line)
            if match:
                field, value = match.groups()
                value = value.strip()

                # Check if the first record's field value is a list
                results = []
                if isinstance(self.data[0][field], list):
                    try:
                        for record in self.data:
                            for item in record[field]:
                                if value in str(item) and record not in results:
                                    results.append(record)
                    except Exception as e:
                        pass
                else:
                    try:
                        results = [record for record in self.data if value in str(record[field])]
                    except Exception as e:
                        pass
                
                if len(results) == 0:
                    print("No matching records found.")
                    return
                
                for record in results:
                    print(json.dumps(record, indent=2))
            else:
                print("Invalid query format.")
                return

        except Exception as e:
            print(f"Error executing find: {e}")

    def do_pick(self, line):
        try:
            if not self.data:
                print("No data loaded.")
                return
            
            parts = line.split(' WHERE ')
            fields = parts[0].strip().split(', ')  # Get the fields to be selected
            
            if len(parts) > 1:  # If there's a WHERE clause
                condition = parts[1].strip()
                
                if 'at least' in condition:
                    field, _, value = condition.partition(' at least ')
                    operator = '>='
                elif 'is' in condition:
                    field, _, value = condition.partition(' is ')
                    operator = '='
                elif 'greater than' in condition:
                    field, _, value = condition.partition(' greater than ')
                    operator = '>'
                elif 'less than' in condition:
                    field, _, value = condition.partition(' less than ')
                    operator = '<'
                elif 'at most' in condition:
                    field, _, value = condition.partition(' at most ')
                    operator = '<='
                else:
                    print("Invalid condition format.")
                    return
                
                value = float(value) if value.replace('.', '', 1).isdigit() else value.strip('"')
            else:
                condition = None

            selected_data = []
            for record in self.data:
                if condition:  # Filter records based on the WHERE clause
                    if operator == '=' and record[field] != value:
                        continue
                    elif operator == '!=' and record[field] == value:
                        continue
                    elif operator == '>' and record[field] <= value:
                        continue
                    elif operator == '<' and record[field] >= value:
                        continue
                    elif operator == '>=' and record[field] < value:
                        continue
                    elif operator == '<=' and record[field] > value:
                        continue

                selected_data.append({field: record[field] for field in fields if field in record})
            
            for item in selected_data:
                print(json.dumps(item, indent=2))
            
        except Exception as e:
            print(f"Error executing pick: {e}")

    def do_update(self, line):
        try:
            if not self.table:
                print("No table selected.")
                return

            if not self.data:
                print("No data loaded.")
                return

            pattern = re.compile(r'(\w+) = (.*?) WHERE (\w+) = (.*?)$')
            match = pattern.match(line.strip())
            if not match:
                print("Invalid update format. Use: field = value WHERE field = value")
                return

            update_field, update_value, condition_field, condition_value = match.groups()
            update_value = update_value.strip(' "')
            condition_value = condition_value.strip(' "')

            updated_count = 0
            for record in self.data:
                if str(record.get(condition_field)) == condition_value:
                    if update_value.isdigit():
                        update_value = int(update_value)
                    record[update_field] = update_value
                    updated_count += 1

            if updated_count == 0:
                print("No records updated.")
                return

            with open(f'{self.table}.json', 'w') as f:
                json.dump(self.data, f, indent=2)

            print(f"{updated_count} records updated.")
        except Exception as e:
            print(f"Error updating records: {e}")

    def do_delete(self, line):
        try:
            if not self.data:
                print("No data loaded.")
                return

            condition = line.strip()
            field, operator, value = re.search(r"(\w+) (>=|<=|>|<|!=|=) (.+)", condition).groups()
            value = float(value) if value.replace('.', '', 1).isdigit() else value.strip('"')

            new_data = []
            deleted_count = 0
            for record in self.data:
                if operator == '=' and record[field] != value:
                    new_data.append(record)
                elif operator == '!=' and record[field] == value:
                    new_data.append(record)
                elif operator == '>' and record[field] <= value:
                    new_data.append(record)
                elif operator == '<' and record[field] >= value:
                    new_data.append(record)
                elif operator == '>=' and record[field] < value:
                    new_data.append(record)
                elif operator == '<=' and record[field] > value:
                    new_data.append(record)
                else:
                    deleted_count += 1

            self.data = new_data
            with open(f'{self.table}.json', 'w') as f:
                json.dump(self.data, f, indent=2)

            print(f"{deleted_count} records deleted.")
            
        except Exception as e:
            print(f"Error executing delete: {e}")

    def do_sortby(self, line):
        try:
            field, order = line.split()
            sorted_data = sorted(self.data, key=itemgetter(field), reverse=(order.upper() == 'DESC'))
            
            for item in sorted_data:
                print(json.dumps(item, indent=2))

        except Exception as e:
            print(f"Error executing sortby: {e}")

    def do_organizeby(self, line):
        try:
            field, aggregate_field, aggregate_func = line.split()
            self.data.sort(key=itemgetter(field))  
            grouped_data = groupby(self.data, key=itemgetter(field))

            for key, group in grouped_data:
                group_list = list(group)
                if aggregate_func == 'SUM':
                    aggregate_value = sum(item[aggregate_field] for item in group_list)
                elif aggregate_func == 'AVG':
                    aggregate_value = sum(item[aggregate_field] for item in group_list) / len(group_list)
                elif aggregate_func == 'COUNT':
                    aggregate_value = len(group_list)
                else:
                    print("Invalid aggregate function.")
                    return

                print(f"{field}: {key}, {aggregate_func}({aggregate_field}): {aggregate_value}")

        except Exception as e:
            print(f"Error executing organizeby: {e}")

    def do_exit(self, line):
        print("Exiting.")
        return True

    def do_join(self, line):
        try:
            table1, table2, on = line.split()
            with open(f'{table1}.json', 'r') as f1, open(f'{table2}.json', 'r') as f2:
                data1 = json.load(f1)
                data2 = json.load(f2)

            joined_data = [
                {**d1, **d2} for d1 in data1 for d2 in data2 if d1[on] == d2[on]
            ]

            for item in joined_data:
                print(json.dumps(item, indent=2))
            
        except Exception as e:
            print(f"Error executing join: {e}")

if __name__ == '__main__':
    MyDB().cmdloop()
