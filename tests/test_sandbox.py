from pathlib import Path
from wikiscraper import text_utils
from wikiscraper import config
from wikiscraper import cache 
from wikiscraper import table_utilis as ts


def main():
    path: Path = config.WORD_COUNTS_JSON
    print("Config file:", config.__file__)
    print("WORD_COUNTS_JSON:", path)
    print("Absolute:", path.is_absolute())
    print("Exists:", path.exists())
    print("Is file:", path.is_file())
    
    
    text_utils.count_words("Bad bunny emma")
    text_utils.count_words("Bad bunny ala")
    
    path = Path('tests/data/test.html')
    content = path.read_text(encoding="utf-8")
    
    cache.load('test', content)
    back = cache.get('test')
    
    path = Path('tests/data/table.html')
    content = path.read_text(encoding="utf-8")
    ts.table(content, 1, False)
    ts.table(content, 1, True)
    
    
    

if __name__ == "__main__":
    main()
