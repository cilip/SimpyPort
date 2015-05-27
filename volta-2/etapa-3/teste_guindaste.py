def guindaste(self, env):
    #sao no total 3 guindastes
    #maximo de dois guindastes panamax e tres para capesize

    guindaste1 = simpy.PreemptiveResource(env, capacity = 1)
    guindaste2 = simpy.PreemptiveResource(env, capacity = 1)
    guindaste3 = simpy.PreemptiveResource(env, capacity = 1)
    guindastesStore = simpy.Store(env, capacity=3)
    guindastesStore.items = [guindaste1, guindaste2, guindaste3]
    
    
    self.tempo_descarregamento = random.expovariate(1/TEMPO_DESCARREGAMENTO_MEDIO)
    
    while True:
        guindaste = yield guindastesStore.get()
        num_guindastes = 1
        
        
    
    
    #request um dos guindastes
    #mudar priority
    #se ha um guindaste na embarcacao, a prioridade dos novos guindastes devem ser para com essa embarcacao e nao para as novas embarcacoes 
    if self.guindaste:
        self.priority = 2
    else:
        self.priority = 3
        
    #mudancas de velociaddaes de descarregamento conforme numero de guindastes operantes na embarcacao
    #valores de carga e tempo_descarregamento sao alterados durante todo o precesso
    #lembrando que guindastes podem ser adicionados, como tambem returados (quebra)
    #lembrar atualizar carga no estoque
    #criar monitor para atualizar contantemente os valores
    self.velocidade_descarregamento = self.num_guindastes*(self.carga/self.tempo_descarregamento)

        
    #request lista de guindastes, com os tres guindastes
    #processo continuo
    #provavelmente o mesmo monitor das atualizacoes de velocidades
    with guindaste.request(priority = self.priority) as req:
       yield req
        
        while self.tempo_descarregamento:
            try:
                if debug:
                    print('%s inicia carregamento em %.1f horas.' % (nome, env.now))  

                start = env.now
                yield env.timeout(tempo_descarregamento)
                tempoOcupadoGuindaste += tempo_descarregamento
                if debug:
                    print('%s termina carregamento em %.1f horas.' % (nome, env.now))  

                tempo_descarregamento = 0
            except simpy.Interrupt:
                if debug:
                    print('%s sofre quebra de guindaste em %.1f horas.' % (nome, env.now))  

                tempo_descarregamento -= env.now - start
               
                
                if debug:
                    print('%s guindaste operante em %.1f horas.' % (nome, env.now))
        
    armazem.put(900)
    estoqueAtual.append((env.now - tempoInicial, armazem.level))

    # Tempo de desatracacao
    yield env.timeout(random.triangular(TEMPO_DESATRACACAO_MIN, TEMPO_DESATRACACAO_MEDIO, TEMPO_DESATRACACAO_MAX))
    
    if debug:
        print('%s deixa o porto em %.1f horas.' % (nome, env.now))  

    if debug:
        print('%s tempo de carregamento: %.1f horas.' % (nome, env.now - start))
    tempoBercoOcupado=tempoBercoOcupado+env.now-start
    numNaviosAtendidos += 1
    cargaEntregue += CARGA_NAVIO



def quebra_guindaste(env, guindaste):
    #deve rodar para cada um dos tres guindastes em questao, simultaneamente (env.process(env, guindaste))
    global broken
    global tempoQuebraGuindaste
    while True:
        yield env.timeout(random.expovariate(1.0/TEMPO_QUEBRA_GUINDASTE))
        if not broken:
            with guindaste.request(priority=1) as req:
                yield req
                if debug:
                    print('Guindaste QUEBROU em %.1f horas.' % (env.now))
                t1 = env.now
                broken=True
                yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_CONCERTO))
                if debug:
                    print('Guindaste LIBERADO em %.1f horas.' % (env.now))
                t2 = env.now
                t = t2 - t1
                tempoQuebraGuindaste += t
                
                broken=False   
    
    
