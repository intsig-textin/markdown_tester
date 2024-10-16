import re


class TableConverter:

    @staticmethod
    def markdown_to_html(markdown_table):
        rows = [row.strip() for row in markdown_table.strip().split('\n')]
        html_table = '<table>\n  <thead>\n    <tr>\n'
        header_cells = [cell.strip() for cell in rows[0].split('|')[1:-1]]
        for cell in header_cells:
            html_table += f'      <th>{cell}</th>\n'
        html_table += '    </tr>\n  </thead>\n  <tbody>\n'
        for row in rows[2:]:
            cells = [cell.strip() for cell in row.split('|')[1:-1]]
            html_table += '    <tr>\n'
            for cell in cells:
                html_table += f'      <td>{cell}</td>\n'
            html_table += '    </tr>\n'
        html_table += '  </tbody>\n</table>\n'
        return html_table

    @staticmethod
    def delete_table_and_body(input_list):
        return [line for line in input_list if not re.search(r'</?t(able|head|body)>', line)]

    @staticmethod
    def merge_tables(input_str):
        input_str = re.sub(r'<!--[\s\S]*?-->', '', input_str)
        table_blocks = re.findall(r'<table>[\s\S]*?</table>', input_str)
        output_lines = []
        for block in table_blocks:
            block_lines = block.split('\n')
            for i, line in enumerate(block_lines):
                if '<th>' in line:
                    block_lines[i] = line.replace('<th>', '<td>').replace('</th>', '</td>')
            final_tr = TableConverter.delete_table_and_body(block_lines)
            if len(final_tr) > 2:
                output_lines.extend(final_tr)
        merged_output = '<table>\n{}\n</table>'.format('\n'.join(output_lines))
        return "\n\n" + merged_output + "\n\n"

    @staticmethod
    def find_md_table_mode(line):
        return bool(re.search(r'-*?:', line) or re.search(r'---', line) or re.search(r':-*?', line))

    @staticmethod
    def replace_table_with_placeholder(input_string):
        lines = input_string.split('\n')
        output_lines = []
        in_table_block = False
        temp_block = ""
        last_line = ""
        org_table_list = []
        in_org_table = False
        for i, line in enumerate(lines):
            if not in_org_table:
                if "<table>" not in last_line and not in_table_block and temp_block:
                    output_lines.append(TableConverter.merge_tables(temp_block))
                    temp_block = ""
                if "<table>" in line:
                    if "<table><tr" in line:
                        org_table_list.append(line)
                        in_org_table = True
                        output_lines.append(last_line)
                        continue
                    else:
                        in_table_block = True
                        temp_block += last_line
                elif in_table_block:
                    if not TableConverter.find_md_table_mode(last_line) and "</thead>" not in last_line:
                        temp_block += "\n" + last_line
                    if "</table>" in last_line:
                        if "<table>" not in line:
                            in_table_block = False
                else:
                    output_lines.append(last_line)
                last_line = line
            else:
                org_table_list.append(line)
                if "</table" in line:
                    in_org_table = False
                    last_line = TableConverter.merge_table(org_table_list)
                    org_table_list = []
        if "</table>" in last_line:
            output_lines.append(TableConverter.merge_tables(temp_block))
        return '\n'.join(output_lines)

    @staticmethod
    def convert_table(input_str):
        output_str = input_str.replace("<table>", "<table border=\"1\" >")
        output_str = output_str.replace("<td>", "<td colspan=\"1\" rowspan=\"1\">")
        return output_str

    @staticmethod
    def convert_table_str(s):
        s = re.sub(r'<table.*?>', '<table>', s)
        s = re.sub(r'<th', '<td', s)
        s = re.sub(r'</th>', '</td>', s)
        res = '\n\n'
        temp_item = ''
        for c in s:
            temp_item += c
            if c == '>' and not re.search(r'<td.*?>\$', temp_item):
                res += temp_item + '\n'
                temp_item = ''
        return res + '\n'

    @staticmethod
    def merge_table(md):
        table_temp = ''.join(md)
        return TableConverter.convert_table_str(table_temp)

    def convert_markdown_to_html(self, markdown_content):
        markdown_content = markdown_content.replace('\r', '')
        pattern = re.compile(r'\|\s*.*?\s*\|\n', re.DOTALL)
        matches = pattern.findall(markdown_content)
        for match in matches:
            html_table = self.markdown_to_html(match)
            markdown_content = markdown_content.replace(match, html_table, 1)
        res_html = self.convert_table(self.replace_table_with_placeholder(markdown_content))
        return res_html
