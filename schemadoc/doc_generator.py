import os
from jinja2 import Environment, PackageLoader


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
        self._generate_home_page()

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
        table_page_path = os.path.join(self._tables_folder, "%s.html"%table_name)
        with open(table_page_path, "wt") as f:
            f.write(table_page)
        url = os.path.relpath(table_page_path, self._folder)
        return url

    def _render_home_page(self):
        template = self._env.get_template('home_page.html')
        return template.render(db=self._db)

    def _generate_home_page(self):
        home_page = self._render_home_page()
        home_page_path = os.path.join(self._folder, 'index.html')
        with open(home_page_path, "wt") as f:
            f.write(home_page)

    def _render_main_diagram(self):
        template = self._env.get_template('main_diagram.gv')
        graph = template.render(db = self._db)
