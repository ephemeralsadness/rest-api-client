from client import TodoElement, Client
import json
import os


def print_todo_list(todo_list) -> None:
    print()
    print('########### TODO LIST ###########')
    task_id_fmt = '{:>8} '
    task_done_fmt = '{:>5}'
    task_name_fmt = ' {}'
    print(task_id_fmt.format('task_id'), end='')
    print(task_done_fmt.format('done'), end='')
    print(task_name_fmt.format('name'))
    for todo_element in todo_list:
        print(task_id_fmt.format(todo_element.task_id), end='')
        print(task_done_fmt.format(int(todo_element.done)), end='')
        print(task_name_fmt.format(todo_element.name))
    print('##################################')


def main():
    url = 'http://104.248.245.109:80'
    username = 'admin'
    password = 'admin'
    client = Client(url=url, username=username, password=password)

    active = True
    while active:
        print_todo_list(client.get_todo_list())
        print('>>>', end=' ')
        req = input().strip().split()
        os.system('cls')
        try:
            if req[0] == 'exit':
                assert(len(req) == 1)
                print('Finishing program...')
                active = False
            elif req[0] == 'add':
                assert (len(req) >= 2)
                task_name = ' '.join(req[1:])
                client.add_todo(task_name)
            elif req[0] == 'change':
                assert (len(req) == 3)
                task_id = int(req[1])
                task_done = req[2] == 'True' or req[2] == 'true'
                client.change_todo(task_id, task_done)
            elif req[0] == 'remove':
                assert(len(req) == 2)
                task_id = int(req[1])
                client.remove_todo(task_id)
            elif req[0] == 'help' or req[0] == 'list':
                print('help | list -- prints list of all commands')
                print('add [task_name] -- add element to todo list')
                print('change [task_id] [task_done] -- change status of todo list element')
                print('remove [task_id] -- remove todo list element from list')
                print('exit -- finishing the program')
            else:
                raise Exception()
        except:
            print('Incorrect command. Enter help or list for list of all commands')


if __name__ == '__main__':
    main()
