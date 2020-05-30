from HW6_back import shortest_path
import click
import time


@click.command()
@click.option('--to', default='Теоретическая_физика', help='to this article')
@click.option('--from', '-f', 'from_',
              default='Теория_струн',
              help='from this article')
@click.option('--n_threads', default=1, help='number of threads')
def start_f(to, from_, n_threads):
    start = time.time()
    for i in shortest_path(from_, to, n_threads):
        print(i)
    print("time: " + str(time.time() - start))


if __name__ == '__main__':
    start_f()
