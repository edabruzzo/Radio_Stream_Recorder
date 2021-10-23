import concurrent.futures
import time

'''

https://analyticsindiamag.com/run-python-code-in-parallel-using-multiprocessing/
https://github.com/python/cpython/tree/3.9/Lib/multiprocessing/

'''


class Multiprocessamento():

    def paralelizar_execucao_processo(self, funcao, parametros=None):
        start = time.perf_counter()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            processo = executor.submit(funcao, parametros)
            if processo is not None:
                pass
                #print(f'Return Value: {processo.result()}')
            end = time.perf_counter()
            print(f'Finished in {round(end - start, 2)} second(s)')

            if __name__ == '__main__':
                def teste_1(nome='Emmanmuel', endereco='Rua X', **kwargs):
                    print(f'Processo_1: {nome} Endereço: {endereco}')

                    Multiprocessamento().paralelizar_execucao_processo(teste_1,
                                                                       {'nome': 'Roger Waters', 'endereco': 'Lisboa'})
                    Multiprocessamento().paralelizar_execucao_processo(teste_1, {'nome': 'Camisa de Vênus',
                                                                                 'endereco': 'Brasil'})
                    Multiprocessamento().paralelizar_execucao_processo(teste_1)
