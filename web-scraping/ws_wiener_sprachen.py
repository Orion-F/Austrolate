"""
Purpose: run a web-scraping script that:
1. accesses https://sprachen.wien.gv.at/worterbuch/?from_language=18&to_language=12&select_category=0&filter_form_sent=1
2. accesses the table with id="phrases-table"
3. for each element in the 3rd column (excluding the header), add it to the list deutsch_words
4. for each element in the 4th column (excluding the header), add it to the list weinerisch_words
5. click on the link with id="phrases-table_next"
6. repeat steps 2-5 until the link with id="phrases-table_next" is no longer there
"""

