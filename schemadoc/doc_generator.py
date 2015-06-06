import os
from jinja2 import Environment, PackageLoader
import pygraphviz


class DocGenerator(object):
    def __init__(self, db, folder):
        self._db = db
        self._folder = folder
        self._tables_folder = os.path.join(self._folder, 'tables')
        self._env = Environment(loader=PackageLoader('schemadoc', 'static/templates'))
        object.__init__(self)

    def generate_documentation(self):
        table_pages = []

        if not os.path.exists(self._tables_folder):
            os.makedirs(self._tables_folder)
        # generate pages for each table
        for table_name in self._db.tables:
            table = self._db.tables[table_name]
            # store table page url for future references
            table.page_url = self._generate_table_page(table)

        # generate index page
        self._render_main_diagram()
        self._generate_home_page()

    def _write_to_file(self, content, to_file):
        with open(to_file, "wt") as f:
            f.write(content)

    def _get_path_and_url(self, filename):
        path = os.path.join(self._folder, filename)
        url = os.path.relpath(path, self._folder)
        return (path, url)

    def _render_table_page(self, table):
        template = self._env.get_template('table_page.html')
        return template.render(table=table)

    def _generate_table_page(self, table):

        """
        Method which creates documentation page per table
        :param table: TableSpecification object form schema objects
        :return: relative url for newly generate table page
        """
        table_name = table.name
        table_page = self._render_table_page(table)
        table_filename = os.path.join('tables', "%s.html"%table_name)
        table_page_path, url  = self._get_path_and_url(table_filename)
        self._write_to_file(content=table_page, to_file=table_page_path)
        return url

    def _render_home_page(self):
        template = self._env.get_template('home_page.html')
        return template.render(db=self._db)

    def _generate_home_page(self):
        home_page = self._render_home_page()
        home_page_path, url = self._get_path_and_url('index.html')
        self._write_to_file(content=home_page, to_file=home_page_path)

    def _render_main_diagram(self):
        template = self._env.get_template('main_diagram.gv')
        graph = template.render(db=self._db)
        print(graph)
        g=pygraphviz.AGraph(graph)
        main_diagram_path, url = self._get_path_and_url('main_diagram.svg')
        g.draw(path=main_diagram_path, prog='dot', format='svg')
        return url


