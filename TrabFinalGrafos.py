import os
import math

class Grafo:
    def ler_grafo(self):    #Lê o grafo de acordo com arquivo
        self.Grafo = {}
        self.direcionado = None
        self.tempo = 0
        self.ciclo = None
        self.conexo = None
        
        arquivoV = open('vertices.txt', mode='r', encoding='utf-8-sig').read().splitlines()
        arquivoA = open('arestas.txt', mode='r', encoding='utf-8-sig').read().splitlines()        

        if arquivoA[0] == 'True': self.direcionado = True
        else: self.direcionado = False
        for linha in arquivoV:
            self.Grafo[linha] = tuple()
        for vertice in self.Grafo:
            for linha in arquivoA[1:]:
                aresta_peso = linha.split(',')
                if aresta_peso[0] == vertice:
                        self.Grafo[vertice] += [aresta_peso[1],(int(aresta_peso[2]) if len(aresta_peso) == 3 else 1)],
                        if self.direcionado == False:
                            self.Grafo[aresta_peso[1]] += ([aresta_peso[0],(int(aresta_peso[2]) if len(aresta_peso) == 3 else 1)],)
        
    def PrintGrafo(self, G): #Imprime qualquer grafo na forma de lista de adjacência
        print()
        for vertice in G:
            print('v[{0}]  ->  a:'.format(vertice), end='')
            if G[vertice] != ():
                for aresta in G[vertice]:
                    print(' {0} '.format(aresta[0]), end='')
            else: print(' ', end='')
            print()
        print()
       
    def buscar_aresta(self, vertice_origem, vertice_destino): #1. Veriﬁcar a existência de uma determinada aresta
        self.PrintGrafo(self.Grafo)
        for vertice in self.Grafo[vertice_origem]:
            if vertice[0] == vertice_destino: return True
        else: return False

    def grau(self, vertice_grau):   #2. Informar o grau de um dado vértice.
        grau = 0

        for aresta in self.Grafo[vertice_grau]: grau += 1
        for vertice in self.Grafo:
            for aresta in self.Grafo[vertice]:
                if vertice_grau == aresta[0]: grau += 1
        if self.direcionado == False: return int(grau/2)
        else: return grau

    def adjacencia(self, vertice_adj):  #3. Informar a adjacência de um dado vértice.
        adj = []
        adjEntrada = []
        adjSaida = [] #lista de adjacentes

        for vertice in self.Grafo:
            if vertice == vertice_adj:
                    for aresta in self.Grafo[vertice_adj]:
                        if aresta[0] not in adj and aresta[0] != vertice_adj: adjSaida.append(aresta[0])
            else:
                for aresta in self.Grafo[vertice]:
                    if aresta[0] == vertice_adj and vertice not in adj: adjEntrada.append(vertice)
        adj.append(adjEntrada)
        adj.append(adjSaida)
        return adj
        
    
    def ciclico(self):  #4. Veriﬁcar se o grafo é cíclico.
        print('''Para encontrar um ciclo em grafo G pode-se aplicar a busca em profundidade.
Se uma aresta de retorno for encontrada, significa que o grafo possui ciclo''')
        input()
        self.PrintGrafo(self.Grafo)
        self.BuscaEmProfundidade(self.Grafo)
        return 'O grafo é {0}'.format('cíclico' if self.ciclo == True else 'acíclico')
            
    def conexos(self):  #5. Veriﬁcar se o grafo é conexo.
        self.PrintGrafo(self.Grafo)
        if len(self.Grafo.keys()) != 1:
            for vertice in self.Grafo:
                adj = self.adjacencia(vertice)
                if adj == [[],[]]:
                    self.conexo = False
                    return 'O v[{0}] não possui nenhuma ligação, logo o grafo G é desconexo'.format(vertice)
                else:
                    self.conexo = True
            return 'O grafo G é totalmente conexo, pois possui pelo menos uma ligação entre cada par de vértices'
        else:
            self.conexo = True
            return 'O grafo possui 1 vértice, mas ainda é conexo'
            
    def ComponenetesConexos(self): #6. Informar quantos e quais são os componentes fortemente conexos do grafo.
        #Funções aninhadas
        def PrintarValores():
            for v in buscaG:
                print('v[{v}] = cor[{v}]:{cor}\ti:{i1}/{i2}\t'.format(v=v,i1=buscaG[v][1],i2=buscaG[v][2],cor=buscaG[v][0]),'π:{0}'.format(buscaG[v][3] if buscaG[v][3] != None else 'Ø'))
            input()
        
        def transposto(): #6.2 GRAFO TRANSPOSTO Gt DE G
            transpostoG = {}

            for vertice in self.Grafo:
                transpostoG[vertice] = tuple()
            for vertice in self.Grafo:
                for aresta in self.Grafo[vertice]:
                    transpostoG[aresta[0]] += [vertice,aresta[1]],
            return transpostoG

        #Escopo de ComponenetesConexos
        
        buscaG = {}
        indiceTermino = {}
        componente = []
        
        if self.direcionado == True:
            print('GRAFO G')
            self.PrintGrafo(self.Grafo)
            #
            print('Aplicando busca em profundidade')
            buscaG = self.BuscaEmProfundidade(self.Grafo)    #6.1 BUSCA EM PROFUNDIDADE
            #
            print('BUSCA EM PROFUNDIDADE EM G')
            PrintarValores()
            #
            print('GRAFO TRANSPOSTO')
            transpostoG = transposto()   #6.2 GRAFO TRANSPOSTO
            self.PrintGrafo(transpostoG)
            #
            print('Aplicando busca em profundidade no transposto')
            for vertice in buscaG:
                indiceTermino[vertice] = buscaG[vertice][2]
                buscaG[vertice] = ['branco', None, None, None] #buscaG[vertice] += ([cor, cont inicio, cont final, antecessor)
            self.tempo = 0
            while indiceTermino != {}:
                max_vertice = max(indiceTermino.items(), key=lambda x: x[1])[0] #Pega o vértice pelo maior indice de término
                if buscaG[max_vertice][0] == 'branco':
                    buscaG = self.visitaBuscaEmProfundidade(transpostoG,max_vertice,buscaG) #6.3 BUSCA EM PROFUNDIDADE PELO VÉRTICE DE MAIOR TEMPO DE TÉRMINO
                    componente.append(set(max_vertice))
                    input()
                elif buscaG[max_vertice][0] == 'preto':
                    componente[len(componente)-1].add(max_vertice)
                indiceTermino.pop(max_vertice)
            #
            print('BUSCA EM PROFUNDIDADE EM Gt')
            PrintarValores()
            #
            if len(componente) == 1:
                print('O grafo G é um componente fortemente conexo')
                print('Os v[',*componente,'] são parte do componente fortmente conexo')
            else:
                print('O grafo G tem {0} componentes conexos:\n'.format(len(componente)))
                for c in componente:
                    if len(c) == 1: print('O v[{0}] é um componente conexo'.format(*c))
                    else: print('Os v[',*c,'] são parte de um componente conexo')
        else: print('O grafo G não é direcionado, o algoritmo de componentes conexos não pode ser executado')
           
    def BuscaEmProfundidade(self,G): #6.1 e 6.3
        buscaG = {}
            
        for vertice in self.Grafo:
            buscaG[vertice] = ['branco', None, None, None] #buscaG[vertice] += ([visita, cont inicio, cont final, antecessor],)
        self.tempo = 0
        for vertice in buscaG:
            if buscaG[vertice][0] == 'branco': buscaG = self.visitaBuscaEmProfundidade(self.Grafo,vertice,buscaG)
        return buscaG

    def visitaBuscaEmProfundidade(self,G,vertice,buscaG): #PARTE DE 6.1 e 6.3
        print('Visitando v[{0}]'.format(vertice))
        buscaG[vertice][0] = 'cinza'
        self.tempo += 1
        print('cor[{0}] = branco -> cinza'.format(vertice),'\ti:{0}/ '.format(self.tempo))
        buscaG[vertice][1] = self.tempo
        for adjacente in G[vertice]:
            if buscaG[adjacente[0]][0] == 'branco':
                print('Indo ao adjacente do v[{0}] = v[{1}]'.format(vertice,adjacente[0]),'\n')
                buscaG[adjacente[0]][3] = vertice
                input()
                buscaG = self.visitaBuscaEmProfundidade(G,adjacente[0],buscaG)
                print('para v[{0}]\n'.format(vertice))
            elif buscaG[vertice[0]][3] == adjacente[0] or buscaG[adjacente[0]][0] == 'preto': #vertice atual esta visitando seu antecessor
                pass
            elif adjacente[0] != vertice:
                print('Aresta de retorno ({0},{1})'.format(vertice,adjacente[0]), end=' = ')
                self.ciclo = True
                print('v[{0}] está em visita'.format(adjacente[0]))
        print('Não há mais adjacentes para o v[{0}]'.format(vertice))
        buscaG[vertice][0] = 'preto'
        self.tempo += 1
        buscaG[vertice][2] = self.tempo
        print('cor[{0}] = cinza -> preto'.format(vertice),'\ti:{0}/{1}'.format(buscaG[vertice][1],self.tempo))
        if buscaG[vertice][3] != None: print('Retornando do v[{0}] '.format(vertice), end='')
        else: print('Finalizado no v[{0}]'.format(vertice),'\n')
        return buscaG
    
    def euleriano(self):    #7. Veriﬁcar se o grafo é euleriano
        todosPar = True

        print('Verificar se todos os vértices tem grau par')
        input()
        for vertice in self.Grafo:
            grau = self.grau(vertice)
            print('Grau[{0}] = {1}'.format(vertice,grau))
            if grau % 3 == 0: todosPar = False
        if todosPar == False: return '\nNem todos os vértices tem grau par, logo não é euleriano'
        else: return '\nTodos os vértices tem grau par, logo é euleriano'
    
    def dijkstra(self,fonte,chegada): #8. Encontrar o caminho mais curto entre dois vértices.
        #Funções aninhadas
        def init_fonte(fonte): #Inicialização da fonte
            estimativaG = {}
            
            for vertice in self.Grafo:
                estimativaG[vertice] = [math.inf,None,'branco'] #[estimativa,antecessor,cor]
            estimativaG[fonte][0] = 0
            return estimativaG

        def relax(estimativaG,vertice_origem,vertice_destino): #Relaxamento
            print('estimativa do v[{v}] = {dv} > estimativa do v[{u}] = {du} + peso({u},{v}) = {w}?'.format(v=vertice_destino[0],dv=estimativaG[vertice_destino[0]][0] if estimativaG[vertice_destino[0]][0] != math.inf else '∞',u=vertice_origem,du=estimativaG[vertice_origem][0],w=vertice_destino[1]))
            if estimativaG[vertice_destino[0]][0] > estimativaG[vertice_origem][0] + vertice_destino[1]:
                print('Relaxando vértice: d[{v}] = {dv} -> {np}'.format(v=vertice_destino[0],dv=estimativaG[vertice_destino[0]][0] if estimativaG[vertice_destino[0]][0] != math.inf else '∞',np=estimativaG[vertice_origem][0] + vertice_destino[1]),end='\t')
                estimativaG[vertice_destino[0]][0] = estimativaG[vertice_origem][0] + vertice_destino[1]
                print('π[{v}] = {e} -> v[{u}]\n'.format(v=vertice_destino[0],u=vertice_origem,e=estimativaG[vertice_destino[0]][1] if estimativaG[vertice_destino[0]][1] != None else 'Ø'))
                estimativaG[vertice_destino[0]][1] = vertice_origem
            else: print('Não é necessário relaxar\n')
            return estimativaG
        
        def iteracao(estimativaG,iteracao): #printa de forma legível cada iteração de Dijkstra
            print('Iteração {0}'.format(i))
            for vertice in self.Grafo:
                print('v[{v}] = d[{v}]:{dv}\tπ:{e}'.format(v=vertice,dv=estimativaG[vertice][0] if estimativaG[vertice][0] != math.inf else '∞',e=estimativaG[vertice][1] if estimativaG[vertice][1] != None else 'Ø'))
            print()
            return i + 1

        #Escopo de dijkstra
                
        Q = {}
        S = []
        caminho = []
        i = 0

        estimativaG = init_fonte(fonte)
        for vertice in self.Grafo:
            Q[vertice] = estimativaG[vertice][0]
        i = iteracao(estimativaG,i)
        input()
        while Q != {}:
            i = iteracao(estimativaG,i)
            print('Conjunto Q = [',*Q,']')
            min_vertice = min(Q.items(), key=lambda x: x[1])[0] #Pega o vértice pela menor estimativa
            print('Vértice com menor estimativa: {0}'.format(min_vertice))
            Q.pop(min_vertice)
            print('Retirado do conjunto Q = [',*Q,']')
            S.append(min_vertice)
            print('Adicionado ao conjunto S = [',*S,']\n')
            estimativaG[min_vertice][2] = 'cinza'
            for adjacente in self.Grafo[min_vertice]:
                if adjacente[0] != fonte and estimativaG[adjacente[0]][2] == 'branco':
                    print('Tentando relaxar a aresta de v[{0},{1}]'.format(min_vertice,adjacente[0]),)
                    estimativaG = relax(estimativaG,min_vertice,adjacente)
                    if Q != {} and adjacente[0] in Q: Q[adjacente[0]] = estimativaG[adjacente[0]][0]
                estimativaG[adjacente[0]][2] == 'preto'
            input()
        print('Caminho de v[{0}]->v[{1}] ='.format(fonte,chegada,),end=' ')
        caminho.insert(0,chegada)
        while chegada != fonte:
            caminho.insert(0,estimativaG[chegada][1])
            chegada = estimativaG[chegada][1]
        print(*caminho,sep='-')
        
    def AGM(self,fonte):
        #Funções aninhadas
        def init_fonte(fonte): #Inicialização da fonte
            estimativaG = {}
            
            for vertice in self.Grafo:
                estimativaG[vertice] = [math.inf,None,'cinza']
            estimativaG[fonte][0] = 0
            return estimativaG
        
        def iteracao(estimativaG,i): #printa de forma legível cada iteração de AGM
            print('Iteração {0}'.format(i))
            for vertice in self.Grafo:
                print('v[{v}] = d[{v}]:{dv}\tπ:{e}'.format(v=vertice,dv=estimativaG[vertice][0] if estimativaG[vertice][0] != math.inf else '∞',e=estimativaG[vertice][1] if estimativaG[vertice][1] != None else 'Ø'))
            print()
            return i + 1

        def PrintarAGM(estimativaG): #printa a Árvore Geradora Minima
            print('AGM de G')
            for vertice in estimativaG:
                print('v[{0}]\tE: '.format(vertice),end='')
                if estimativaG[vertice][1] != None:
                    print('{e} -> '.format(e=estimativaG[vertice][1]),end='')
                for aresta in estimativaG:
                    if vertice != aresta and estimativaG[aresta][1] == vertice:
                        print('{e} -> '.format(e=aresta),end='')
                print()

        #Escopo de AGM
                
        Q = {}
        i = 0
        pesoAGM = 0
        solucao = []
        
        print('\nGRAFO G - NÃO-DIRECIONADO')
        self.PrintGrafo(self.Grafo)
        input()
        estimativaG = init_fonte(fonte)
        for vertice in self.Grafo:
            Q[vertice] = estimativaG[vertice][0]
        while Q != {}:
            i = iteracao(estimativaG,i)
            PrintarAGM(estimativaG)
            print('Conjunto Q = [',*Q,']')
            min_vertice = min(Q.items(), key=lambda x: x[1])[0] #Pega o vértice pela menor estimativa
            print('Vértice com menor estimativa: {0}'.format(min_vertice))
            Q.pop(min_vertice)
            print('Retirado do conjunto Q = [',*Q,']')
            solucao.append(min_vertice)
            print('Adicionado ao conjunto S = [',*solucao,']\n')
            estimativaG[min_vertice][2] = 'azul'
            for adjacente in self.Grafo[min_vertice]:
                if estimativaG[adjacente[0]][2] == 'cinza':
                    print('Verificando se a estimativa do adjacente v[{a}] = {e} > peso({v},{a}) = {p}'.format(v=min_vertice,a=adjacente[0],p=adjacente[1],e=estimativaG[adjacente[0]][0] if estimativaG[adjacente[0]][0] != math.inf else '∞'))
                    if adjacente[0] in Q.keys() and adjacente[1] < estimativaG[adjacente[0]][0]:
                        print('π[{v}] = {e} -> v[{a}]'.format(v=adjacente[0],e=estimativaG[adjacente[0]][1] if estimativaG[adjacente[0]][1] != None else 'Ø',a=min_vertice))
                        estimativaG[adjacente[0]][1] = min_vertice
                        print('key[{v}] = {e} -> {p}\n'.format(v=adjacente[0],e=estimativaG[adjacente[0]][0] if estimativaG[adjacente[0]][0] != math.inf else '∞',p=adjacente[1]))
                        estimativaG[adjacente[0]][0] = adjacente[1]
                        Q[adjacente[0]] = estimativaG[adjacente[0]][0]
                    else: print('Nada a fazer')
            input()
        for vertice in estimativaG:
            pesoAGM += estimativaG[vertice][0]
        print('Peso da AGM[G]: {0}'.format(pesoAGM))

    pass

case = 0

G = Grafo()
G.ler_grafo()
while case != 10:
    print('GRAFO G - {0}'.format('DIRECIONADO' if G.direcionado == True else 'NÃO-DIRECIONADO'))
    G.PrintGrafo(G.Grafo)
    print('''1 - Verificar a existencia de determinada aresta
2 - Informar o grau de um dado vértice
3 - Informar a adjacência de um dado vértice
4 - Verificar se o grafo é ciclico
5 - Verificar se o grafo é conexo
6 - Informar quantos e quais são os componentes fortemente conexos do grafo
7 - Verificar se o grafo é euleriano
8 - Encontrar o caminho mais curto entre dois vértices.
9 - Árvore Geradora Mínima
10 - Fechar''')
    case = int(input('> '))
    os.system('cls')
    if case == 1:
        print('1 - BUSCAR ARESTA')
        vertice_origem = input('Aresta de origem: ')
        vertice_destino = input('Aresta de destino: ')
        if vertice_origem in G.Grafo.keys() and vertice_destino in G.Grafo.keys():
            print('\nA aresta ({0},{1}) existe'.format(vertice_origem,vertice_destino) if G.buscar_aresta(vertice_origem,vertice_destino) == True else '\nA aresta ({0},{1}) não existe'.format(vertice_origem,vertice_destino))
        else: print('\nParece que um dos vértices digitados não existe, ou os vértices digitados são iguais')
    elif case == 2:
        print('2 - GRAU')
        vertice_grau = input('Verificar o grau do vértice: ')
        if vertice_grau in G.Grafo.keys():
            G.PrintGrafo(G.Grafo)
            grau = G.grau(vertice_grau)
            print('\nGrau[{0}] = {1}'.format(vertice_grau,grau))
        else: print('\nO vértice digitado parece não existir, tente novamente')
    elif case == 3:
        print('3 - ADJACENTES')
        vertice_adj = input('Verificar as adjacências do vértice: ')
        if vertice_adj in G.Grafo.keys():
            G.PrintGrafo(G.Grafo)
            adj = G.adjacencia(vertice_adj)
            if adj == [] or adj[1] == []: print('\nO v[{0}] não possui vértices adjacentes'.format(vertice_adj))
            else: print('\nO v[{0}] possui adjacência com os seguintes v['.format(vertice_adj),*adj[1],']',)
        else: print('\nO vértice digitado parece não existir, tente novamente')
    elif case == 4:
        print('4 - CICLICO')
        print(G.ciclico())
    elif case == 5:
        print('5 - CONEXO')
        print(G.conexos())
    elif case == 6:
        print('6 - COMPONENTES FORTEMENTE CONEXOS')
        G.ComponenetesConexos()
    elif case == 7:
        print('7 - EULERIANO')
        G.conexos()
        if G.conexo == True: print(G.euleriano())
        else: print('O grafo precisa ser conexo para verificar se é euleriano')
    elif case == 8:
        print('8 - CAMINHO MAIS CURTO')
        print('\nGRAFO G - {0}'.format('DIRECIONADO' if G.direcionado == True else 'NÃO-DIRECIONADO'))
        G.PrintGrafo(G.Grafo)
        vertice_origem = input('Digite o vértice que será a fonte: ')
        vertice_destino = input('Digite o vértice de chegada: ')
        if vertice_origem in G.Grafo.keys() and vertice_destino in G.Grafo.keys(): G.dijkstra(vertice_origem,vertice_destino)
        else: print('Parece que um dos vértices digitados não existe')
    elif case == 9:
        print('9 - ÁRVORE GERADORA MÍNIMA')
        print('Verificando se o grafo G é conexo')
        print(G.conexos(),'\n')
        if G.conexo == False: print('O grafo G é desconexo e não se pode aplicar AGM')
        elif G.direcionado == True: print('O grafo G é direcionado e não se pode aplicar AGM')
        else:
            fonte = input('Digite o vértice que será a fonte: ')
            if fonte in G.Grafo.keys(): G.AGM(fonte)
            else: print('\nO vértice digitado parece não existir, tente novamente')
    elif case == 10:
        print('Concluido')
    input()
    os.system('cls')
