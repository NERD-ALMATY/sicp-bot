task = {"summary": "Take out trash", "description": "" }
resp = requests.post('https://todolist.example.com/tasks/', json=task)
if resp.status_code != 201:
    raise ApiError('POST /tasks/ {}'.format(resp.status_code))
print('Created task. ID: {}'.format(resp.json()["id"]))


def get_all_choices(self):
    """ Yields this choice and all its children. """
    stack = [self]
    while stack:
        top = stack.pop()
        yield top
        stack.extend(reversed(top.children))
