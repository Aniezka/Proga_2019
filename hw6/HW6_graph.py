from HW6_back_graph import graph_shortest_path
import click
import json
import time


@click.command()
@click.option('--output', default='output.json', help='to this file')
@click.option('--inp',
              default='task.json',
              help='"from"/"to" articles from this json')
@click.option('--n_threads', default=1, help='number of threads')
def start_f(inp, output, n_threads):
    d = {}
    all_task = []
    with open(inp, "r") as f:
        for task in json.load(f):
            start = time.time()
            all_task.append({"from": task['from'],
                             "to": task['to'],
                             "all_shortest_paths": graph_shortest_path(
                                 d,
                                 task['from'],
                                 task['to'],
                                 n_threads)})
            print("time: " + str(time.time() - start))
    with open(output, "w", encoding='utf8') as f:
        json.dump(all_task, f, ensure_ascii=False)


if __name__ == '__main__':
    start_f()
