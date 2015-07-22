
from html.parser import HTMLParser
from html.entities import html5

class Aggregator(HTMLParser):

    def __init__(self, lines):
        
        HTMLParser.__init__(self)
        self.read = lines
        self.text = ''
        self.next_url = ''

        self.current_id = -1

        self.parsing_id = False
        self.parsing_text = False

        self.delim = '\n\n' + '=~'*35 + '\n' + '~='*35 + '\n\n'


    def handle_starttag(self, tag, attrs):

        if tag == 'br' and self.parsing_text:
            self.text += '\n'
        elif len(attrs) < 1:
            return

        if (tag == 'span' and attrs[0][0] == 'class' and attrs[0][1] == 'id'):
            self.parsing_id = True
        elif (tag == 'div' and attrs[0][0] == 'class'
              and attrs[0][1] == 'text' and self.current_id not in self.read):
            self.parsing_text = True
        elif len(attrs) < 2:
            return

        if (tag == 'a' and attrs[0][0] == 'href'
            and attrs[1][0] == 'class' and attrs[1][1] == 'button'):
            self.next_url = 'bash.im' + attrs[0][1]


    def handle_data(self, data):

        if self.parsing_text:
            self.text += data

        elif self.parsing_id:
            self.current_id = data.strip()


    def handle_endtag(self, tag):

        if self.parsing_text:
            self.text += self.delim
            self.read.append(self.current_id)

        self.parsing_text = self.parsing_id = False

    def handle_entityref(self, name):

        self.text += html5[name + ';']
