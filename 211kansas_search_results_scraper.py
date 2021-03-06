import requests
from bs4 import BeautifulSoup
import csv

got_text = False
pages_found = 53
filename = 'filename.csv'

with open(filename, mode='a+', newline='') as csv_file:
    header = ["Name", "Description", "Services", "Street Address", "City, State Zip", "Phone Number"]
    csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(header)

    for i in range(1, pages_found + 1):
        while not got_text:
            result = requests.get(
                f'https://211kansas.myresourcedirectory.com/index.php/component/cpx/?task=search.query&view=&page={i}&search_history_id=155717797&unit_list=0&akaSort=0&advanced=true&query=%20&simple_query=&code=FOOD,BD&name=')
            if result.status_code == 200:
                got_text = True

        content = result.content
        soup_content = BeautifulSoup(content, "html.parser")

        found_items = soup_content.find_all("div", "result-row clearfix")

        for item in found_items:

            title = ""
            description = ""
            services = ""
            address_line_1 = ""
            address_line_2 = ""
            phone_number = ""

            try:
                title = item.find("p", "resource-name").get_text().encode("ascii", "ignore")
            except AttributeError:
                title = ""
                title = title.encode("ascii", "ignore")

            try:
                description = item.find("p", "resource-description").get_text().encode("ascii", "ignore")
            except AttributeError:
                description = ""
                description = description.encode("ascii", "ignore")

            try:
                services = item.find("p", "services").get_text().encode("ascii", "ignore")
            except AttributeError:
                services = ""
                services = services.encode("ascii", "ignore")

            try:
                address_line_1 = item.find("p", "resource-address-line1").get_text().encode("ascii", "ignore")
            except AttributeError:
                address_line_1 = ""
                address_line_1 = address_line_1.encode("ascii", "ignore")

            try:
                address_line_2 = item.find("p", "resource-address-line3").get_text().encode("ascii", "ignore")
            except AttributeError:
                address_line_2 = ""
                address_line_2 = address_line_2.encode("ascii", "ignore")

            try:
                phone_number = item.find("p", "resource-phone").get_text().encode("ascii", "ignore")
            except AttributeError:
                phone_number = ""
                phone_number = phone_number.encode("ascii", "ignore")

            current_row = [title.decode().strip('\n'), description.decode(),
                           services.decode().strip("Services: "), address_line_1.decode(),
                           address_line_2.decode(), phone_number.decode()]
            csv_writer.writerow(current_row)

        got_text = False


