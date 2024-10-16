import distance
from apted import APTED, Config
from apted.helpers import Tree
from lxml import etree, html


class TableTree(Tree):
    def __init__(self, tag, colspan=None, rowspan=None, content=None, *children):
        self.tag = tag
        self.colspan = colspan
        self.rowspan = rowspan
        self.content = content
        self.children = list(children)

    def bracket(self):
        if self.tag == 'td':
            result = f'"tag": {self.tag}, "colspan": {self.colspan}, "rowspan": {self.rowspan}, "text": {self.content}'
        else:
            result = f'"tag": {self.tag}'
        for child in self.children:
            result += child.bracket()
        return f"{{{result}}}"


class CustomConfig(Config):
    @staticmethod
    def maximum(*sequences):
        return max(map(len, sequences))

    def normalized_distance(self, *sequences):
        return float(distance.levenshtein(*sequences)) / self.maximum(*sequences)

    def rename(self, node1, node2):
        if (node1.tag != node2.tag) or (node1.colspan != node2.colspan) or (node1.rowspan != node2.rowspan):
            return 1.0
        if node1.tag == 'td' and (node1.content or node2.content):
            return self.normalized_distance(node1.content, node2.content)
        return 0.0


class TEDS:
    def __init__(self, structure_only=False, n_jobs=1, ignore_nodes=None):
        assert isinstance(n_jobs, int) and (n_jobs >= 1), 'n_jobs must be an integer greater than or equal to 1'
        self.structure_only = structure_only
        self.n_jobs = n_jobs
        self.ignore_nodes = ignore_nodes

    def tokenize(self, node):
        tokens = ['<%s>' % node.tag]
        if node.text:
            tokens.extend(node.text)
        for n in node.getchildren():
            tokens.extend(self.tokenize(n))
        if node.tag != 'unk':
            tokens.append('</%s>' % node.tag)
        if node.tag != 'td' and node.tail:
            tokens.extend(node.tail)
        return tokens

    def load_html_tree(self, node, parent=None):
        if node.tag == 'td':
            cell = [] if self.structure_only else self.tokenize(node)[1:-1]
            new_node = TableTree(node.tag, int(node.attrib.get('colspan', '1')), int(node.attrib.get('rowspan', '1')),
                                 cell)
        else:
            new_node = TableTree(node.tag)
        if parent:
            parent.children.append(new_node)
        for n in node.getchildren():
            self.load_html_tree(n, new_node)
        return new_node if not parent else None

    def evaluate(self, pred, true):
        if not pred or not true:
            return 0.0
        parser = html.HTMLParser(remove_comments=True, encoding='utf-8')
        pred = html.fromstring(pred, parser=parser)
        true = html.fromstring(true, parser=parser)

        pred_table = pred.xpath('body/table')
        true_table = true.xpath('body/table')
        if pred_table and true_table:
            pred, true = pred_table[0], true_table[0]
            if self.ignore_nodes:
                etree.strip_tags(pred, *self.ignore_nodes)
                etree.strip_tags(true, *self.ignore_nodes)
            n_nodes_pred = len(pred.xpath(".//*"))
            n_nodes_true = len(true.xpath(".//*"))
            n_nodes = max(n_nodes_pred, n_nodes_true)
            tree_pred = self.load_html_tree(pred)
            tree_true = self.load_html_tree(true)
            teds_distance = APTED(tree_pred, tree_true, CustomConfig()).compute_edit_distance()
            return 1.0 - (teds_distance / n_nodes)
        return 0.0
