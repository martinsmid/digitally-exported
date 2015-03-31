
def get_file_content(link, name):
    content = """{link}
EOF
shuffle_mode=S: disabled
repeat_mode=S: disabled
dynamic_mode=S: disabled
current_position=I: -1
name=U: {name}
""".format(link=link, name=name)
    return content


class Exaile(object):
    def __init__(self):
        self.user_path = os.path.expanduser('~/.local/share/exaile/radio_stations')
        self.order_file = open(os.path.join(self.user_path, 'order_file'), 'w')

    def add(self, name, uri):
        logging.info('Adding %s [%s]' % (name, uri))
        norm_name = name.lower().replace(' ', '_')
        file_name = norm_name + '.playlist'
        path = os.path.join(self.user_path, norm_name)
        with open(path, 'w+') as f:
            f.write(
                get_file_content(uri, name)
            )
            self.order_file.write(norm_name + '\n')

    def finish(self):
        self.order_file.write('EOF\n')
