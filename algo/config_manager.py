import logging
from datetime import datetime

import definitions
import xml.etree.ElementTree as ET
import xml.dom.minidom as dom

from definitions import ALGO_CONFIG

_logger = logging.getLogger("config_manager")


def create_config_file(username: str, password: str):
    config = ET.Element('config')
    credentials = ET.SubElement(config, 'credentials')
    login_id = ET.SubElement(credentials, 'LoginId')
    login_password = ET.SubElement(credentials, 'Password')
    login_id.text = username
    login_password.text = password
    _logger.debug("Added Credentials")

    api = ET.SubElement(config, 'api')
    unique_id = ET.SubElement(api, "UniqueId")
    ref_no = ET.SubElement(api, "RefNo")
    modified = ET.SubElement(api, "Modified")
    modified.text = datetime.now().isoformat()
    _logger.debug("Added: %s %s" % (unique_id, ref_no))

    data = dom.parseString(ET.tostring(config, encoding='unicode'))
    xml = data.toprettyxml()
    f = open(ALGO_CONFIG, 'w')
    f.write(xml)
    f.close()


def set_api_credentials(unique_id, ref_no):
    tree = ET.parse(ALGO_CONFIG)
    root = tree.getroot()
    api = root.find('api')
    api[0].text = unique_id
    # print(api[0].text)
    api[1].text = str(ref_no)
    api[2].text = datetime.now().isoformat()
    # tree.write(ALGO_CONFIG)
    get_api_credentials()


def get_api_credentials():
    tree = ET.parse(ALGO_CONFIG)
    root = tree.getroot()
    api = root.find('api')
    unique_id = api[0].text
    ref_no = api[1].text
    modified = api[2].text
    print(unique_id, ref_no, modified)


def get_credentials():
    tree = ET.parse(ALGO_CONFIG)
    root = tree.getroot()
    credentials = root.find('credentials')
    login_id = credentials[0].text
    login_password = credentials[1].text
    return login_id, login_password


if __name__ == '__main__':
    # create_config_file("8288024014", "a@8888888888")
    # get_credentials()
    set_api_credentials(97, "")
