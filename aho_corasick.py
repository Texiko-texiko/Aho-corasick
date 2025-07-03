from collections import deque

class ACAutomaton:
    def __init__(self):
        self.root = self.AutomatonNode()

    def add(self, keyword):
        if not keyword:
            return
            
        node = self.root
        keyword_bytes = str(keyword).encode('utf-8')
        for byte in keyword_bytes:
            if node.next[byte] is None:
                node.next[byte] = self.AutomatonNode()
            node = node.next[byte]
        node.add_word(keyword)

    def set_failure_path(self):
        queue = deque()
        self.root.fail = self.root
        for i in range(len(self.root.next)):
            node = self.root.next[i]
            if node is not None:
                node.fail = self.root
                queue.append(node)
        
        while queue:
            current_node = queue.popleft()
            for i in range(len(current_node.next)):
                child = current_node.next[i]
                if child is not None:
                    queue.append(child)
                    fail_link = current_node.fail
                    while fail_link.next[i] is None and fail_link is not self.root:
                        fail_link = fail_link.fail
                    if fail_link.next[i] is not None:
                        child.fail = fail_link.next[i]
                    else:
                        child.fail = self.root
                    child.words.extend(child.fail.words)
    
    def search(self, text):
        results = []
        text_bytes = str(text).encode('utf-8')
        node = self.root

        for i in range(len(text_bytes)):
            byte = text_bytes[i]
            while node.next[byte] is None and node is not self.root:
                node = node.fail
            if node.next[byte] is not None:
                node = node.next[byte]
            if node.words:
                for word in node.words:
                    start = i - len(str(word).encode('utf-8')) + 1
                    results.append((start, word))
        return results
    
    def search_trie(self, text):
        results = []
        text_bytes = str(text).encode('utf-8')

        for i in range(len(text_bytes)):
            node = self.root
            for j in range(i, len(text_bytes)):
                byte = text_bytes[j]
                if node.next[byte] is None:
                    break
                node = node.next[byte]
                if node.words:
                    for word in node.words:
                        results.append((i, word))
        return results

    def print_tree(self):
        """
        トライ木の構造を分かりやすく表示します。
        """
        print("(root)")
        self._print_tree_recursive(self.root, "")

    def _print_tree_recursive(self, node, prefix):
        """
        print_treeの内部で呼ばれる再帰関数。
        
        Args:
            node: 現在のノード
            prefix: 表示行の前に付加する文字列 (例: "│   ")
        """
        # Noneでない子ノードだけをリストアップする
        children = [(i, child) for i, child in enumerate(node.next) if child is not None]
        
        for i, (byte, child_node) in enumerate(children):
            # 現在のノードが、兄弟の中で最後かどうかを判定
            is_last = (i == len(children) - 1)
            
            # 最後のノードなら "└── "、そうでなければ "├── " を使う
            marker = "└── " if is_last else "├── "
            
            # バイトを16進数で表現 (例: 0x61)
            # chr(byte)より確実で、あらゆるバイト値を表現できる
            hex_byte_str = f"0x{byte:02x}"
            
            # そのノードで終わる単語があれば表示する
            output_words = f" -> {child_node.words}" if child_node.words else ""

            # 行をプリント
            print(prefix + marker + hex_byte_str + output_words)

            # 次の階層で使うprefixを準備する
            # is_lastなら"    "、そうでなければ"│   "を追加する
            new_prefix = prefix + ("    " if is_last else "│   ")
            
            # 再帰呼び出し
            self._print_tree_recursive(child_node, new_prefix)


    class AutomatonNode:
        def __init__(self):
            self.words = []
            self.next = [None] * 256
            self.fail = None

        def add_word(self, word):
            self.words.append(word)

if __name__ == '__main__':
    A = ACAutomaton()
    A.add("鳥")
    A.add("鳥類")
    A.add("雛鳥")
    A.add("朝")
    A.add("朝食")
    A.add("鳥居")
    A.add("イカ")
    A.add("he")
    A.add("she")
    A.print_tree()
    A.set_failure_path()
    A.print_tree()