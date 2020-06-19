import logging
import sys

from datacatalog_tag_template_processor import tag_template_datasource_processor


__SUPPORTED_EXTENSION = '.csv'
__SUPPORTED_FILE_SYNTAX = 'datacatalog-sync-tag-templates'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def run(data, _):
    try:
        file_name = data['name']

        if not file_name.endswith(__SUPPORTED_EXTENSION):
            logging.info('File: %s is not a %s, ignoring.',
                         file_name, __SUPPORTED_EXTENSION)
            return

        if not file_name.startswith(__SUPPORTED_FILE_SYNTAX):
            logging.info('File: %s does not contain valid file syntax: %s, ignoring.',
                         file_name, __SUPPORTED_FILE_SYNTAX)
            return

        logging.info('===> Processing file: %s', file_name)

        file_path = 'gs://{}/{}'.format(data['bucket'], file_name)
        tag_template_datasource_processor.TagTemplateDatasourceProcessor(
        ).create_tag_templates_from_csv(file_path=file_path)
    except Exception as err:
        logging.error('Exception on run function %s', str(err))
        raise err
