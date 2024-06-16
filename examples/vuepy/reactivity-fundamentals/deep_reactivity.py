def setup(*args, **kwargs):
    import time
    import threading

    from vuepy import ref

    obj = ref({
        'nested': {'count': 0},
        'arr': ['foo', 'bar'],
    })

    def mutate_deeply(own):
        obj.value['nested']['count'] += 1
        obj.value['arr'].append("baz")

    def async_run(own):
        def task_block():
            print("task start")
            time.sleep(2)
            print("task end")

        thread = threading.Thread(target=task_block, args=())
        thread.start()
        # task_block()

    return locals()
