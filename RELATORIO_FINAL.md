# Relatorio Final do Trabalho

## Titulo provisiorio

**Fechamento Hierarquico das Equacoes de Movimento no Hamiltoniano BCS Reduzido e sua Verificacao Computacional por Simulacao Quantica**

## 1. Visao Geral

Este trabalho desenvolveu uma reformulacao teorica e computacional do problema BCS a partir das equacoes de movimento de Zubarev. O objetivo nao foi repetir a derivacao padrao da equacao do gap por campo medio, mas reinterpretar o surgimento do formalismo BCS como consequencia de um **fechamento projetivo da hierarquia de operadores** gerada pelo Hamiltoniano interagente.

O resultado central e a construcao de um manuscrito em LaTeX, em estilo proximo ao de artigos da *Physical Review B*, acompanhado por um laboratorio computacional para modelos BCS finitos. O projeto combina fisica de muitos corpos, algebra fermionica, funcoes de Green, teoria de operadores e simulacao quantica via mapeamento de Jordan-Wigner.

## 2. Contribuicao Fisica

O ponto conceitual mais importante do estudo e a mudanca de perspectiva:

> O campo medio BCS nao e tomado como ponto de partida, mas como a projecao de menor ordem de uma hierarquia exata de equacoes de movimento.

Partindo do Hamiltoniano BCS reduzido,

```text
H = sum_{k sigma} xi_k c^dagger_{k sigma} c_{k sigma}
    + sum_{k k'} V_{k k'}
      c^dagger_{k up} c^dagger_{-k down}
      c_{-k' down} c_{k' up},
```

foi introduzido o Liouvilliano,

```text
L A = [A,H],
```

e definida a hierarquia de subespacos de operadores gerada por aplicacoes sucessivas de `L` sobre um operador semente. Para o operador `c_{k up}`, a primeira aplicacao da parte interagente do Liouvilliano produz operadores compostos de tres fermions. Isso mostra explicitamente que a equacao de movimento exata nao se fecha no setor de uma particula.

A estrutura obtida e:

```text
operador de 1 fermion
        |
        L_I
        v
operador de 3 fermions
        |
        L_I
        v
setores de 1, 3 e 5 fermions
```

O retorno ao setor de Nambu ocorre em segunda ordem na interacao, por contracoes fermionicas no canal de pares. O fechamento projetivo desse retorno produz a autoenergia anomalosa:

```text
Sigma_k =
[ 0          Delta_k  ]
[ Delta*_k   0        ]
```

e recupera a equacao de Dyson para a funcao de Green de Nambu.

## 3. Resultado Teorico Principal

O resultado demonstrado no manuscrito pode ser formulado de modo conservador:

> Para o Hamiltoniano BCS reduzido, a cadeia de equacoes de movimento de Zubarev gera uma hierarquia de operadores. Ao projetar a hierarquia no setor de pares de Nambu e reter o retorno de segunda ordem produzido pela algebra fermionica, obtem-se a estrutura de Dyson com autoenergia anomalosa, da qual segue a equacao usual do gap BCS.

Esta afirmacao e mais forte do que uma simples reescrita pedagogica, mas mais prudente do que declarar uma nova teoria completa. Ela estabelece uma interpretacao hierarquica do campo medio BCS.

## 4. O Que Foi Separado com Rigor

O trabalho distingue cuidadosamente tres niveis:

### Resultados demonstrados

- Definicao da hierarquia de operadores via Liouvilliano.
- Crescimento explicito do setor de um fermion para operadores compostos.
- Fechamento projetivo de ordem `V^2` no canal de pares.
- Recuperacao da forma de Dyson.
- Interpretacao do campo medio como projecao da hierarquia.

### Reformulacao fisica defensavel

- O BCS mean-field pode ser entendido como a menor aproximacao nao trivial da hierarquia EOM.
- A autoenergia anomalosa representa o efeito dos setores eliminados sob uma projecao no setor de pares.
- O erro do fechamento pode ser associado a setores residuais da hierarquia.

### Pontos ainda nao provados

- Fechamento exato da hierarquia completa.
- Convergencia de fechamentos recursivos superiores.
- Estimativas de norma para os setores residuais.
- Formalizacao em espacos de Banach.
- Interpretacao homologica rigorosa das contracoes.
- Teoremas de universalidade para uma medida de informacao hierarquica.

Essa separacao e essencial para que o trabalho nao prometa mais do que demonstra.

## 5. Relacao com a Literatura

O manuscrito posiciona o estudo em relacao a:

- Bardeen, Cooper e Schrieffer: teoria BCS original.
- Gor'kov: funcoes de Green anomalas.
- Zubarev: funcoes de Green de duplo tempo e equacoes de movimento.
- Dyson: autoenergia e resolvente.
- Fetter e Walecka: teoria quantica de muitos corpos.
- Mahan: funcoes de Green em sistemas interagentes.
- Mori-Zwanzig: projecoes e memoria dinamica.
- BBGKY: hierarquias de distribuicoes e fechamentos.
- Hubbard: hierarquias de operadores em sistemas correlacionados.

A novidade nao esta na equacao do gap em si. A novidade defensavel esta na organizacao da derivacao como um **problema de fechamento hierarquico**.

## 6. Parte Computacional

Foi criado um laboratorio computacional em:

```text
C:\Users\aocbaeta\Documents\hierarchical-bcs-manuscript\quantum-bcs-lab
```

O laboratorio implementa um modelo BCS finito:

```text
H = sum_j xi_j (n_{j up} + n_{j down})
    - g sum_{j,l} P_j^dagger P_l
    - eta sum_j (P_j^dagger + P_j),

P_j = c_{j down} c_{j up}.
```

O termo proporcional a `eta` foi adicionado na etapa final do trabalho para
quebrar explicitamente a simetria de numero de particulas. Ele permite comparar
diretamente amplitudes anomalas exatas `<P_j>_eta` com o perfil anomaloso BCS em
sistemas finitos.

Cada nivel `j` e mapeado para dois modos fermionicos:

```text
2*j     -> k_j up
2*j + 1 -> -k_j down
```

e depois para qubits por Jordan-Wigner.

## 7. Arquitetura Computacional

Foram implementados os seguintes arquivos:

- `bcs_core.py`: operadores fermionicos, Hamiltoniano BCS, diagonalizacao exata, gap BCS e diagnostico hierarquico.
- `pairspace_core.py`: representacao no subespaco de pares, com dimensao `2^N`.
- `pauli_mapper.py`: mapeamento Jordan-Wigner para strings de Pauli.
- `run_benchmark.py`: benchmark numerico principal com `numpy`.
- `run_source_sweeps.py`: varreduras do campo fonte `eta`.
- `run_scaling_sweeps.py`: varredura de escala em `N` e `eta` usando o subespaco de pares.
- `run_extrapolation.py`: ajuste quantitativo do erro em funcao de `1/N`.
- `run_phase_sweeps.py`: fonte complexa e resposta de fase do parametro de ordem.
- `test_consistency.py`: testes de consistencia entre espaco completo, subespaco de pares e mapeamento JW.
- `qiskit_bcs_exact.py`: camada para Qiskit usando `SparsePauliOp`.
- `pennylane_bcs_vqe.py`: ansatz variacional BCS em PennyLane.
- `cirq_bcs_dynamics.py`: construcao do Hamiltoniano em Cirq.
- `requirements.txt`: dependencias opcionais.
- `README.md`: instrucoes de execucao.

Como Qiskit, PennyLane e Cirq ainda nao estavam instalados no ambiente Python local, as camadas foram preparadas de modo modular, mas o benchmark central foi executado com sucesso usando apenas `numpy`.

## 8. Resultado Numerico Obtido

Para o caso:

```text
n_levels = 4
n_qubits = 8
xi = [-1.5, -0.5, 0.5, 1.5]
g = 0.7
```

o benchmark retornou:

```text
energia exata                  = -6.137034636681297
energia BCS mean-field          = -4.4135325385700686
gap BCS                         =  1.0234995508486207
maior autovalor da matriz pares =  1.1887407872832516
residual da matriz de pares     =  0.6802653952717661
numero de termos de Pauli       =  61
erro do mapeamento JW           =  6.1854469444995704e-15
```

O erro do mapeamento Jordan-Wigner e da ordem de `10^-15`, isto e, o Hamiltoniano em strings de Pauli reproduz a matriz fermionica com precisao numerica.

O residual da matriz de pares nao e pequeno nesse exemplo. Isso e fisicamente interessante: mostra que, em um sistema finito conservando exatamente o numero de particulas, o fechamento BCS de menor ordem nao captura toda a estrutura de correlacao de pares. Esse resultado reforca a motivacao do proprio estudo: os setores residuais da hierarquia sao fisicamente relevantes e podem ser quantificados.

## 9. Sutileza Importante: Simetria de Numero

Durante a implementacao, apareceu uma questao fisica importante. Em diagonalizacao exata de um Hamiltoniano que conserva o numero de particulas, o valor anomaloso

```text
<P_j> = <c_{j down} c_{j up}>
```

e nulo, a menos que seja introduzido explicitamente um campo que quebre a simetria de calibre.

Portanto, comparar diretamente `<P_j>` entre BCS e diagonalizacao exata seria enganoso. O diagnostico foi corrigido para usar a matriz de densidade de pares:

```text
C_{jl} = <P_j^dagger P_l>.
```

Essa e a quantidade correta para estudar correlacoes de emparelhamento em sistemas finitos com conservacao de numero.

## 10. Campo Fonte e Quebra Explícita de Simetria

Para atacar diretamente a sutileza da simetria de numero, foi implementado o Hamiltoniano com fonte:

```text
H_eta = H - eta sum_j (P_j^dagger + P_j).
```

Quando `eta = 0`, a diagonalizacao exata conserva numero de particulas e retorna `<P_j> = 0`. Quando `eta > 0`, a simetria e quebrada explicitamente e a amplitude anomalosa passa a ser mensuravel no estado fundamental exato.

Para `n_levels = 4`, `g = 0.7` e `eta = 0.01`, o benchmark retornou:

```text
energia exata                  = -6.138028153780934
gap BCS                         =  1.0234995508486207
maior autovalor da matriz pares =  1.188768646755869
residual da matriz de pares     =  0.6800176692222228
||<P>_eta||                     =  0.05214933870921273
erro relativo do perfil fonte   =  0.9318941226013666
numero de termos de Pauli       =  69
erro do mapeamento JW           =  6.1854469444995704e-15
```

Esse resultado confirma a interpretacao fisica esperada: a fonte `eta` torna a amplitude anomalosa nao nula, enquanto o mapeamento fermion-qubit continua correto em precisao numerica.

Tambem foi executada uma varredura para:

```text
N = 3, 4, 5 niveis
g = 0.7
eta entre 1e-4 e 0.2
12 pontos por tamanho
```

Os resultados principais foram:

```text
N = 3: ||<P>_eta|| cresce de 0.0002435 para 0.3824441
       erro de perfil cai de 0.9995733 para 0.3452774

N = 4: ||<P>_eta|| cresce de 0.0005231 para 0.5859435
       erro de perfil cai de 0.9993159 para 0.2556911

N = 5: ||<P>_eta|| cresce de 0.0006364 para 0.7209736
       erro de perfil cai de 0.9993280 para 0.2457041
```

Fisicamente, isso mostra que o sistema finito, quando suavemente perturbado por uma fonte de pares, desenvolve uma resposta anomalosa que se aproxima melhor do perfil BCS a medida que `eta` cresce. Essa observacao motivou a etapa seguinte do proprio trabalho: a varredura de escala no subespaco de pares e a extrapolacao preliminar em `1/N`, descritas abaixo.

## 11. Varredura de Escala no Subespaco de Pares

Para estudar a ordem dos limites de modo mais eficiente, foi implementada uma representacao no subespaco de pares. Nessa base, cada nivel esta vazio ou ocupado por um par completo. A dimensao cai de:

```text
2^(2N)  para  2^N.
```

O termo fonte `eta` tambem preserva esse subespaco, pois cria ou remove pares completos. Assim, foi possivel executar uma varredura ate:

```text
N = 10 niveis de pares
dimensao maxima = 1024
g = 0.7
eta entre 1e-4 e 0.2
10 pontos por tamanho
```

A representacao foi validada contra o Hamiltoniano fermionico completo em `N = 4`:

```text
diferenca de energia          = 8.881784197001252e-16
diferenca em ||<P>_eta||      = 1.0798653637955624e-16
```

Os resultados no maior valor da fonte, `eta = 0.2`, mostram melhora progressiva do alinhamento com o perfil BCS:

```text
N = 3:  ||<P>_eta|| = 0.3824441, erro de perfil = 0.3452774
N = 6:  ||<P>_eta|| = 0.8991201, erro de perfil = 0.1874310
N = 10: ||<P>_eta|| = 1.3038368, erro de perfil = 0.1463840
```

Esse resultado e importante: ele fornece a primeira evidencia numerica de escala de que o estado exato com simetria explicitamente quebrada se alinha melhor ao perfil anomaloso BCS quando o numero de niveis de pares aumenta.

## 12. Extrapolacao em `1/N` e Fonte Complexa

Para tornar a tendencia de escala mais quantitativa, foi ajustado o erro relativo do perfil fonte contra `1/N` para cada valor fixo de `eta`. Em seguida, a extrapolacao foi refinada comparando tres modelos:

```text
linear em 1/N
quadratico em 1/N
lei de potencia com offset: a + b N^(-alpha)
```

Usando AICc como criterio de selecao para amostra pequena, o modelo linear em `1/N` foi selecionado para todos os valores de `eta` amostrados. Isso nao prova universalidade da escala linear, mas justifica seu uso como primeiro modelo quantitativo para estes dados.

Valores representativos:

```text
eta = 1.0e-4: erro extrapolado ~= 0.9926
eta = 8.6e-2: erro extrapolado ~= 0.0953
eta = 2.0e-1: erro extrapolado ~= 0.0616
```

Isso confirma quantitativamente a tendencia observada nas figuras: para fonte suficientemente forte, a extrapolacao em tamanho aponta para alinhamento muito melhor com o perfil BCS.

Tambem foi implementada uma fonte complexa:

```text
H_eta = H - sum_j (eta P_j^dagger + eta* P_j).
```

Para `N = 8`, `g = 0.7`, `|eta| = 0.05` e 16 fases igualmente espacadas, a diferenca maxima entre a fase da resposta anomalosa `arg(sum_j <P_j>)` e a fase da fonte `arg(eta)` foi:

```text
2.45e-16
```

Esse resultado e uma checagem forte da fisica de quebra de simetria `U(1)`: a resposta anomalosa exata segue a fase imposta pela fonte externa ate precisao numerica.

## 13. Interpretacao Computacional do Fechamento Hierarquico

O laboratorio permite testar numericamente a ideia central do manuscrito:

```text
hierarquia exata -> projecao no setor de pares -> fechamento BCS
```

O residual computado compara:

```text
matriz exata de pares
        versus
aproximacao rank-one gerada pelo perfil BCS projetado.
```

Se o residual for pequeno, o fechamento de menor ordem e bom. Se for grande, a hierarquia residual contem informacao fisica relevante.

Isso transforma a proposta teorica em um programa computacional verificavel.

## 14. Papel de Qiskit, PennyLane e Cirq

### Qiskit

Qiskit e adequado para:

- construir `SparsePauliOp`;
- diagonalizar Hamiltonianos pequenos;
- preparar VQE;
- comparar circuitos com a matriz exata.

No projeto, ele entra como camada de validacao do Hamiltoniano qubitizado.

### PennyLane

PennyLane e adequado para:

- ansatz variacionais diferenciaveis;
- otimizacao automatica dos parametros BCS;
- comparacao entre VQE e fechamento de campo medio;
- calculo de observaveis de pares.

No projeto, ele entra como ponte natural entre o ansatz BCS e algoritmos variacionais quanticos.

### Cirq

Cirq e adequado para:

- circuitos explicitos;
- evolucao temporal;
- Trotterizacao;
- estudo de crescimento de operadores.

No projeto, ele pode ser usado para investigar dinamicamente a profundidade hierarquica por espalhamento de operadores.

## 15. Avaliacao Cientifica

Como trabalho de fisica teorica, a proposta e promissora porque reorganiza uma teoria conhecida sob uma estrutura mais geral. O valor cientifico esta em mostrar que o BCS mean-field pode ser entendido como uma projecao controlada de uma hierarquia exata.

Como trabalho computacional, o projeto e solido porque nao depende apenas de simulacao variacional. Ele parte de diagonalizacao exata, valida o mapeamento fermion-qubit e prepara extensoes em tres bibliotecas distintas de computacao quantica.

Como possivel artigo, o estudo ainda precisa reforcar:

- uma prova ainda mais detalhada dos sinais em todos os comutadores;
- uma comparacao numerica sistematica variando distribuicoes de `xi`;
- um estudo de escala no limite de muitos niveis;
- uma secao mais robusta sobre relacao com Mori-Zwanzig;
- uma discussao clara sobre limite termodinamico versus sistemas finitos.

## 16. Proximos Passos Recomendados

1. Ampliar a extrapolacao para faixas maiores de `N` e testar sua estabilidade fora da malha atual.
2. Rodar varreduras maiores em distribuicoes nao uniformes de `xi`.
3. Comparar o VQE PennyLane com diagonalizacao exata e fechamento BCS.
4. Instalar Qiskit, PennyLane e Cirq e executar os tres scripts opcionais.
5. Estudar fonte complexa em presenca de distribuicoes assimetricas de `xi`.
6. Criar um notebook unificado para reproducibilidade.
7. Transformar a auditoria de novidade em uma secao final de discussao do artigo.

## 17. Conclusao

O trabalho produziu uma base consistente para um artigo teorico-computacional. A contribuicao principal e a reinterpretacao do formalismo BCS como fechamento de uma hierarquia de equacoes de movimento, com campo medio emergindo como projecao e nao como hipotese inicial.

A parte computacional confirma que o modelo finito pode ser mapeado corretamente para qubits e oferece um caminho concreto para medir a qualidade do fechamento hierarquico. O resultado numerico inicial mostra que os setores residuais da hierarquia nao sao meramente formais: eles aparecem como diferencas mensuraveis na matriz de correlacao de pares.

A extensao com campo fonte `eta` fortalece substancialmente o estudo, porque resolve a principal tensao entre diagonalizacao exata finita e o formalismo BCS de simetria quebrada. Com `eta > 0`, a amplitude anomalosa exata se torna diretamente comparavel ao perfil BCS, transformando a discussao de simetria em um diagnostico numerico concreto.

A nova representacao no subespaco de pares leva essa analise um passo adiante: permite estudar escala ate `N = 10` e mostra que, para fonte finita, o erro de perfil diminui com o aumento do numero de niveis. Isso torna a conexao entre diagonalizacao exata, quebra explicita de simetria e fechamento BCS muito mais convincente.

A extrapolacao em `1/N` e a fonte complexa completam o quadro atual: a primeira transforma a tendencia de escala em estimativa quantitativa; a segunda confirma que a fase do parametro de ordem e controlada pela fase da fonte, como esperado para a quebra de simetria `U(1)`.

Em termos de maturidade cientifica, o projeto esta agora em estagio de **manuscrito teorico-computacional promissor**, com uma tese clara, uma estrutura teorica defensavel, validacao por mapeamento fermion-qubit e um primeiro estudo quantitativo da quebra explicita de simetria.
