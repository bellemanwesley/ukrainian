import os

main_page = os.popen("curl https://ua.korrespondent.net/").read()
search_index = main_page.find("<div class=\"article_main\">")
link_start = main_page.find("href=\"",search_index) + 6
link_end = main_page.find("\">",link_start)
link = main_page[link_start:link_end]
article_page = os.popen("curl "+link).read()
del(main_page)