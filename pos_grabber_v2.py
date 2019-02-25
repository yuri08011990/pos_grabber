import bs4 as bs
from bs4 import Tag
import urllib.request
import re
import xlsxwriter



def get_text_with_br(tag, result=''):
    for x in tag.contents:
        if isinstance(x, Tag):  						# Check if content is a tag
            if x.name == 'br':  						# If tag is <br> append it as string
                result += str(x)
            else:  										# For any other tag, recurse
                result = get_text_with_br(x, result)
        else:  											# If content is NavigableString (string), append
            result += x
    return result


def remove_duplicates(cleaned_3):    
    uniqueList = []    									# Create an empty list to store unique elements    
    for element in cleaned_3:							# Iterate over the original list    
        if element not in uniqueList:
            uniqueList.append(element)					# Add each element to uniqueList, if its not already there.    
    return uniqueList									# Return the list of unique elements


def clean():
	# cleaned_1 - remove spaces
	# cleaned_2 - split text into list on <br/>
	# cleaned_3 - remove flags from each element of list
	# cleaned_4 - remove duplicate elements
	cleaned_1 = table.replace(u'\xa0', u'')
	cleaned_2 = cleaned_1.split('<br/>')
	cleaned_3 = [re.sub(r'\s+(verb|noun|adj).*$', '', i, flags=re.IGNORECASE) for i in cleaned_2]
	cleaned_4 = remove_duplicates(cleaned_3)
	return cleaned_4


def add_delimiter():
	delimiter = delimeter_type.join(clean())
	return str(delimiter)


def save_result():
	worksheet = workbook.add_worksheet()
	worksheet.write('A1', word)
	worksheet.write('B1', add_delimiter())
	workbook.close()


def print_result():
	print('Результат:', clean())
	print('Результат з розділювачем:', add_delimiter())


def main():
	add_delimiter()
	print_result()

	q_save = None
	while q_save not in ("так", "ні"):
		q_save = input("Зберегти результат у файл? ")
		if q_save == "так":
			save_result()
			print('Результат збережено до', workbook_name)
		elif q_save == "ні":
			print('Результат не збережено.')
		else:
			print('Дайте зрозумілу відповідь (так/ні)')


word = input('Введіть запит: ')
querry = str(urllib.parse.quote(word))
delimeter_type = input('Введіть тип розділювача: ')
sauce = urllib.request.urlopen('https://r2u.org.ua/vesum/?w=' + querry).read()
soup = bs.BeautifulSoup(sauce, 'lxml')	
table = get_text_with_br(soup.find('table', {'class': 'main_tbl'}).find('td'))
workbook_name = 'output.xlsx'
workbook = xlsxwriter.Workbook(workbook_name)




if __name__ == '__main__':
	main()