import bs4 as bs
import urllib.request
import re



word = str(urllib.parse.quote(input('Введіть слово: ')))

sauce = urllib.request.urlopen('https://www.yenotes.com/uk/words/conjugation/search/?word=' + word + '&lang=uk').read()

soup = bs.BeautifulSoup(sauce, 'lxml')


forms = []

for td in soup.find_all('td'):
	forms.append(str(td.get_text()))


emphasis    = 'а́б́в́ѓґ́д́е́є́ж́з́и́і́ї́й́ќл́м́н́о́п́р́с́т́у́ф́х́ц́ч́ш́щ́ь́ю́я́'
no_emphasis = 'а;б;в;г;ґ;д;е;є;ж;з;и;і;ї;й;к;л;м;н;о;п;р;с;т;у;ф;х;ц;ч;ш;щ;ь;ю;я;'


all_forms = ('/'.join(forms)).translate(str.maketrans(emphasis, no_emphasis))

conjugations = soup.find('span',{'class':'word-conjugations-link'}).find('span').text


def replaceMultiple(all_forms, toBeReplaced, all_forms_replaced):
	for element in toBeReplaced :
		if element in all_forms :
			all_forms = all_forms.replace(element, all_forms_replaced)	
	return all_forms

clean_forms = replaceMultiple(all_forms, ['на/у ', ';'] , '')
clean_forms = re.sub(r'\/на\/у ', '', clean_forms)


mis = soup.find(text="Місцевий").findNext('td').decompose()


print(conjugations)
print(clean_forms)