"""Module: controller.py"""

from wikiscraper.scraper import Scraper
from wikiscraper.page import Page
from wikiscraper import config
import time
import os
import shutil
import wordfreq
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Controller():
    def __init__(self):
        pass
    
    def run_func(self, args):
        """
        Automatically run the function associated with the subcommand.
        
        args: Namespace from parser.parse_args()
        """
        func = args.func  # The actual function set via set_defaults(func=...)
        
        # Convert Namespace to dict, but remove keys not meant for the function
        arg_dict = vars(args).copy()
        arg_dict.pop("func")
        arg_dict.pop("command")
        
        return func(**arg_dict)
        
    def is_html_in_cache(self, phrase: str):
        path = config.CACHE_DIR/phrase
        return os.path.exist(path)

    def clear_cache(self) -> None:
        folder = config.CACHE_DIR
        for filename in os.listdir(config.CACHE_DIR):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # delete file or symbolic link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # delete folder and its contents
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    
    def clear_json(self) -> None:
        path = config.DATA_DIR/"word_count.json"
        with open(path, 'wb') as file:
            file.write("")
            
    
    def _get_page(self, phrase: str, wait: int= 0) -> Page:
        if self.is_html_in_cache(phrase=phrase):
            sc = Scraper(phrase=phrase, use_local_html_file_instead=True)
            return sc.scrape
        time.sleep(wait)
        
        sc = Scraper(phrase=phrase, use_local_html_file_instead=True)
        return sc.scrape()
    
    def summary(self, phrase: str):
        p = self._get_page(phrase=phrase)
        p.summary()
    
    def count_words(self, phrase: str):
        p = self._get_page(phrase=phrase)
        p.count_words()
    
    def table(self, phrase: str, number: int, output_dir: str = config.DATA_DIR,  first_row_is_header=False):
        p = self._get_page(phrase=phrase)
        p.table(n=number, output_dir=output_dir, first_row_is_header=first_row_is_header) 
    
    def auto_count_words(self, phrase: str, depth: int, wait: int):
        visited = {}
        q = []
        q.append({phrase, 0})
        
        while q.empty():
            current_phrase, current_depth = q.pop() 
            
            if current_phrase in visited:
                continue
            
            visited.add(current_phrase)
            
            current_page = self._get_page(phrase=current_phrase, wait=wait)
            current_page.count_words()
            
            if current_depth >= depth:
                continue
            
            for link in current_page.links():
                q.append({link, current_depth + 1})
    
    def normalyze(self, v: list):
        v = np.array(v)
        v = v/np.sum(v)
        return v
    
    def analyze_relative_word_frequency(self, mode: str, count: int, chart: str = None):
        language = 'en'
        try:
            raw = config.WORD_COUNTS_JSON.read_text(encoding="utf-8").strip()
            data: dict[str, int] = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            data = {}

        if mode == "article":
            sorted_freqs = sorted(data.items(), key=lambda item: item[1], reverse=True)
            words = [k[0] for k in sorted_freqs[:count]]
        else:
            words = wordfreq.top_n_list('en',count)

        words.reverse()
        
        counts_in_article = []    
        counts_in_language = []
        
        for word in words:
            cnt_lan = wordfreq.word_frequency(word, language, wordlist='small')
            if cnt_lan is None:
                cnt_lan = 0
            counts_in_language.append(cnt_lan)
            
            if word in data.keys():
                counts_in_article.append(data[word]) 
            else:
                counts_in_article.append(0) 
                
        
        freq_in_language = self.normalyze(counts_in_language)   
        freq_in_article = self.normalyze(counts_in_article)
        
        df = pd.DataFrame({
            'Word': words,
            'Language_Freq': freq_in_language,
            'Article_Freq': freq_in_article
        })
        
        print(df)
        
        if chart is not None: 
            x = np.arange(count)
            width = 0.35

            plt.xticks(rotation=45)
            plt.bar(x - width/2, freq_in_language, width, color='red', label=language)
            plt.bar(x + width/2, freq_in_article, width, color='blue', label='Article')

            # Labels and title
            plt.xticks(x, words)  # set category labels on x-axis
            plt.ylabel("Frequency in %")
            plt.title("Frequency of some words on Wiki")
            plt.legend()
            plt.tight_layout()
            plt.savefig(chart)
                
                
            
                
            
            

        
            
            
        