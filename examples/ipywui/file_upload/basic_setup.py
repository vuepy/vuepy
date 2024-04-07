import codecs
import json

from vuepy import computed
from vuepy import ref


def setup(props, ctx, vm):
    files = ref([])

    def get_first_file():
        file_info = {}
        if files.value:
            file_info = files.value[0]
            content = file_info['content']
            file_info['content'] = codecs.decode(content, encoding='utf-8')
            file_info['last_modified'] = str(file_info['last_modified'])

        return json.dumps(file_info, indent=2)

    upload_file = computed(get_first_file)

    return locals()
