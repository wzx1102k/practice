import json
 
class CCode:
    def str(self, content, encoding='utf-8'):
        return json.dumps(content, encoding=encoding, ensure_ascii=False)

