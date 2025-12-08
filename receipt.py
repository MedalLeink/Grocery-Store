""" Enhancements:

 1. Prints days until New Year's Sale (Jan 1)
 2. Prints a "return by" date 30 days in the future at 9:00 PM
 3. Implements Buy One Get One Half Off for product D083
 4 Prints a coupon for the first product ordered """



import csv
from datetime import datetime, timedelta

def read_dictionary(filename, key_column_index):
    """Reads a CSV file and returns a dictionary where the key is from the specified column index."""
    dictionary = {}
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                key = row[key_column_index]
                dictionary[key] = row  # This stores the whole row as the value
    except FileNotFoundError as e:
        print("Error: missing file")
        print(e)
    except PermissionError as e:
        print("Error: permission denied")
        print(e)
    return dictionary

def main():
    store_name = "Inkom Emporium"
    sales_tax_rate = 0.06

    # Read product dictionary
    products_dict = read_dictionary("products.csv", 0)  # Product ID is column 0
    if not products_dict:
        return  # This stops if products_dict failed

    total_items = 0
    subtotal = 0
    first_ordered_product = None

    print(store_name)

    try:
        with open("request.csv", 'r', newline='') as request_file:
            reader = csv.reader(request_file)
            next(reader)  # Skip header row

            for row in reader:
                try:
                    prod_id = row[0]
                    quantity = int(row[1])
                    prod_info = products_dict[prod_id]

                    prod_name = prod_info[1]
                    prod_price = float(prod_info[2])
                    line_total = 0

                    # --- BOGO for D083 with discounted prices displayed ---
                    if prod_id == "D083":
                        discounted_prices = []
                        for i in range(quantity):
                            if i % 2 == 1:  # every second item is half off
                                discounted_prices.append(prod_price / 2)
                                line_total += prod_price / 2
                            else:
                                discounted_prices.append(prod_price)
                                line_total += prod_price

                        # Print each item with its discounted price
                        for idx, price in enumerate(discounted_prices, 1):
                            print(f"{prod_name} ({idx}): ${price:.2f}")
                    else:
                        line_total = quantity * prod_price
                        print(f"{prod_name}: {quantity} @ {prod_price:.2f}")

                    total_items += quantity
                    subtotal += line_total

                    if not first_ordered_product:
                        first_ordered_product = prod_name

                except KeyError:
                    print(f"Error: unknown product ID in the request.csv file\n'{prod_id}'")
                except ValueError:
                    print(f"Error: invalid quantity for product ID {prod_id}")

        sales_tax = subtotal * sales_tax_rate
        total = subtotal + sales_tax

        print(f"Number of Items: {total_items}")
        print(f"Subtotal: {subtotal:.2f}")
        print(f"Sales Tax: {sales_tax:.2f}")
        print(f"Total: {total:.2f}")
        print(f"Thank you for shopping at the {store_name}.")

        # Print current date and time
        now = datetime.now()
        print(now.strftime("%a %b %d %H:%M:%S %Y"))

        # --- Enhancements ---

        # 1. Days until New Year Sale
        next_year = now.year + 1
        new_year = datetime(next_year, 1, 1)
        days_until_new_year = (new_year - now).days
        print(f"Days until New Year's Sale: {days_until_new_year}")

        # 2. Return by date (30 days in future at 9:00 PM)
        return_date = (now + timedelta(days=30)).replace(hour=21, minute=0, second=0)
        print(f"Return by: {return_date.strftime('%a %b %d %Y %I:%M %p')}")

        # 4. Print a coupon for the first product ordered
        if first_ordered_product:
            print(f"Coupon: Get 10% off your next {first_ordered_product} purchase!")

    except FileNotFoundError as e:
        print("Error: missing file")
        print(e)
    except PermissionError as e:
        print("Error: permission denied")
        print(e)

if __name__ == "__main__":
    main()