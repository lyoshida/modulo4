# coding: utf-8
# referencia: https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
# comando: ./manage.py importar temporeal_dump.txt cp1252

# XXX:  melhorar tratamento de errors
#       - encoding inexistente
#       - nao conseguimos ler o arquivo

import io
from django.core.management.base import BaseCommand, CommandError

from circulante.catalogo.models import Publicacao, Credito

class Command(BaseCommand):
    args = '<arq_delimitado_por_tabs> [<encoding>]'
    help = 'Importa massa de dados da livraria (encoding default: utf-8)'

    def handle(self, *args, **options):
        if len(args)<1:
            raise CommandError('Informe o nome do arquivo a importar.')
        
        nome_arq = args[0]
        if len(args) == 2:
            encoding = args[1]
        else:
            encoding = 'utf-8'
        with io.open(nome_arq, 'rt', encoding=encoding) as arq_ent:
            qt_registros = 0
            try: # evita aparecer um erro muito grande no terminal
                #linhas = arq_ent.readlines()
                for linha in arq_ent:
                    linha = linha.rstrip()
                    if not linha: # tratamento para linhas vazias
                        continue
                    partes = linha.split('\t')
                    id_padrao = None
                    autores = ''
                    if len(partes) >= 3: # para o caso de nao ter os campos completos
                        id_padrao,num_paginas,titulo = partes[:3]
                    if len(partes) == 4:
                        autores = partes[3]                    
                    if id_padrao is None:
                        raise CommandError(repr(partes))
                    num_paginas = int(num_paginas)
                    pub = Publicacao(id_padrao=id_padrao, 
                                        num_paginas=num_paginas,
                                        titulo = titulo)
                    pub.save()
                    for autor in autores.split('/'):
                        autor = autor.strip()
                        if not autor:
                            continue
                        cred = Credito(nome=autor, publicacao=pub)
                        cred.save()
                        self.stdout.write('.') # mostra um ponto para cada import. serve como progresso
                    qt_registros += 1
                    
            except UnicodeDecodeError as exc:
                #import pdb; pdb.set_trace() # quando acontece o erro, joga no prompt do python para depuracao, pdb (python debugger)
                msg = u'Encoding incorreto: "{0.reason}" posicao:{0.start}'
                raise CommandError(msg.format(exc))
        
        self.stdout.write('Importando: %s registros\n' % qt_registros)
        
        

# comandos do pdb:
# h -> help
# dir(exc)
# exc.encoding -> 'utf-8'
# exc.reason -> 'invalid continuation byte'
# exc.start -> 109
# exc.__class__.__name__ -> 'UnicodeDecodeError'
# comandos importantes: next (n) e step (s)
# continue (c) -> continua a execucao
