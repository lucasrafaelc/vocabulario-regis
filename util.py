from numbers import Number

class Contador(dict):
    '''
    Um contador é uma classe que mantém o controle de contagens para um conjunto de chaves.

    A classe do contador é uma extensão do tipo de dicionário padrão do Python. Ela é especializada em ter valores numéricos (inteiros ou floats) e inclui funções adicionais para facilitar a tarefa de contar dados.
    Em particular, todas as chaves têm por padrão o valor 0. Usando um dicionário:

    >>> a = {}
    >>> print a['test']
    retornaria um erro, enquanto o análogo da classe Counter:

    >>> a = Contador()
    >>> print a['test']
    0
    retorna o valor padrão 0. Note que para referenciar uma chave que você sabe que está contida no contador, você ainda pode usar a sintaxe do dicionário:

    >>> a = Contador()
    >>> a['test'] = 2
    >>> print a['test']
    2
    Isso é muito útil para contar coisas sem inicializar suas contagens, veja por exemplo:

    >>> a['blah'] += 1
    >>> print a['blah']
    1
    O contador também inclui funcionalidades adicionais úteis na implementação dos classificadores para esta atribuição. Dois contadores podem ser adicionados, subtraídos ou multiplicados. Veja abaixo para mais detalhes. Eles também podem ser normalizados e sua contagem total e o argumento máximo podem ser extraídos.
    '''

    def __getitem__(self, indice):
        self.setdefault(indice, 0)
        return dict.__getitem__(self, indice)

    def incrementar_todos(self, chaves: list, valor: Number = 1):
        '''
        Incrementa todos os elemento do dicionário com um mesmo valor.

        >>> a = Contador()
        >>> a.incrementar_todos(['um', 'dois', 'três'], 1)
        >>> a['um']
        1
        >>> a['dois']
        1
        '''
        for chave in chaves:
            self[chave] += valor

    def incrementar(self, chave):
        self[chave] += 1

    def maior(self):
        '''
        Retorna a chave que possui o maior valor
        '''
        if len(self.keys()) == 0:
            return None
        todos_valores = list(self.items())
        valores = [x[1] for x in todos_valores]
        indice_maior = valores.index(max(todos_valores))
        return todos_valores[indice_maior][0]

    def _sinal(self, x: Number) -> int:
        """
        Retorna 1 ou -1 dependendo do sinal de x
        """
        if x >= 0:
            return 1
        else:
            return -1

    def ordenar_chaves(self) -> list:
        '''
        Retorna uma lista das chaves do dicionário ordenadas pelos seus valores. Chaves com valores mais altos aparecem antes de chaves com valores baixos.

        >>> a = Contador()
        >>> a['primeiro'] = -2
        >>> a['segundo'] = 4
        >>> a['terceiro'] = 1
        >>> a.ordenar_chaves()
        ['segundo', 'terceiro', 'primeiro']
        '''
        itens_ordenados = list(self.items())
        itens_ordenados.sort()
        return [x[0] for x in itens_ordenados]

    def soma_contadores(self) -> Number:
        '''
        Retorna a soma de todos os contadores do dicionário
        '''
        return sum(self.values())

    def normalizacao(self) -> None:
        '''
        Normaliza os valores do dicionário de modo que todos somem 1.
        CUIDADO: A normalização em um Contador vazio resulta em um erro!
        '''
        total = float(self.soma_contadores())
        if total == 0:
            return
        for chave in self.keys():
            self[chave] = self[chave] / total

    def dividirTodos(self, divisor: Number) -> None:
        '''
        Divide todos os valores por um divisior
        '''
        divisor = float(divisor)
        for chave in self:
            self[chave] /= divisor

    def copia(self):
        '''
        Retorna uma cópia do contador
        '''
        return Contador(dict.copy(self))

    def __mul__(self, y) -> Number:
        '''
        A multiplicação de dois contadores retorna o produto escalar deles, onde cada chave é considerada um elemento do vetor

        >>> a = Contador()
        >>> b = Contador()
        >>> a['primeiro'] = -2
        >>> a['segundo'] = 4
        >>> b['primeiro'] = 3
        >>> b['segundo'] = 5
        >>> a['terceiro'] = 1.5
        >>> a['quarto'] = 2.5
        >>> a * b
        14
        '''
        soma = 0
        x = self
        if len(x) > len(y):
            x, y = y, x
        for chave in x:
            if chave not in y:
                continue
            soma += x[chave] * y[chave]
        return soma

    def __radd__(self, y) -> None:
        """
        A soma de dois contadores incrementa o contador atual, somando os valores do segundo contador

        >>> a = Contador()
        >>> b = Contador()
        >>> a['primeiro'] = -2
        >>> a['segundo'] = 4
        >>> b['primeiro'] = 3
        >>> b['terceiro'] = 1
        >>> a += b
        >>> a['primeiro']
        1
        """
        for chave, valor in y.items():
            self[chave] += valor

    def __add__(self, y):
        """
        Somar dois contadores retorna um novo contador com a união de todas as chaves e contagens do segundo contador com o primeiro.

        >>> a = Contador()
        >>> b = Contador()
        >>> a['primeiro'] = -2
        >>> a['segundo'] = 4
        >>> b['primeiro'] = 3
        >>> b['terceiro'] = 1
        >>> (a + b)['primeiro']
        1
        """
        resposta = Contador()
        for chave in self:
            if chave in y:
                resposta[chave] = self[chave] + y[chave]
            else:
                resposta[chave] = self[chave]
        for chave in y:
            if chave in self:
                continue
            resposta[chave] = y[chave]
        return resposta

    def __sub__(self, y):
        """
        Subtrai os dois contadores, diminuindo do primeiro as contagens que estão no segundo contador

        >>> a = Contador()
        >>> b = Contador()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a - b)['first']
        -5
        """
        resposta = Contador()
        for chave in self:
            if chave in y:
                resposta[chave] = self[chave] - y[chave]
            else:
                resposta[chave] = self[chave]
        for chave in y:
            if chave in self:
                continue
            resposta[chave] = -1 * y[chave]
        return resposta
