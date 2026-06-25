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
    - g sum_{j,l} P_j^dagger P_l,

P_j = c_{j down} c_{j up}.
```

Cada nivel `j` e mapeado para dois modos fermionicos:

```text
2*j     -> k_j up
2*j + 1 -> -k_j down
```

e depois para qubits por Jordan-Wigner.

## 7. Arquitetura Computacional

Foram implementados os seguintes arquivos:

- `bcs_core.py`: operadores fermionicos, Hamiltoniano BCS, diagonalizacao exata, gap BCS e diagnostico hierarquico.
- `pauli_mapper.py`: mapeamento Jordan-Wigner para strings de Pauli.
- `run_benchmark.py`: benchmark numerico principal com `numpy`.
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

## 10. Interpretacao Computacional do Fechamento Hierarquico

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

## 11. Papel de Qiskit, PennyLane e Cirq

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

## 12. Avaliacao Cientifica

Como trabalho de fisica teorica, a proposta e promissora porque reorganiza uma teoria conhecida sob uma estrutura mais geral. O valor cientifico esta em mostrar que o BCS mean-field pode ser entendido como uma projecao controlada de uma hierarquia exata.

Como trabalho computacional, o projeto e solido porque nao depende apenas de simulacao variacional. Ele parte de diagonalizacao exata, valida o mapeamento fermion-qubit e prepara extensoes em tres bibliotecas distintas de computacao quantica.

Como possivel artigo, o estudo ainda precisa reforcar:

- a prova detalhada dos comutadores;
- a demonstracao explicita das contracoes de segunda ordem;
- uma comparacao numerica sistematica variando `g`, numero de niveis e distribuicao de `xi`;
- uma secao mais robusta sobre relacao com Mori-Zwanzig;
- uma discussao clara sobre limite termodinamico versus sistemas finitos.

## 13. Proximos Passos Recomendados

1. Expandir a prova algebraica do fechamento `V^2` em um apendice.
2. Rodar uma varredura numerica em `g` e `n_levels`.
3. Gerar figuras: energia exata vs BCS, gap vs acoplamento, residual de pares vs acoplamento.
4. Instalar Qiskit, PennyLane e Cirq e executar os tres scripts opcionais.
5. Implementar um pequeno campo externo de quebra de simetria para comparar diretamente `<P_j>`.
6. Criar um notebook unificado para reproducibilidade.
7. Transformar a auditoria de novidade em uma secao final de discussao do artigo.

## 14. Conclusao

O trabalho produziu uma base consistente para um artigo teorico-computacional. A contribuicao principal e a reinterpretacao do formalismo BCS como fechamento de uma hierarquia de equacoes de movimento, com campo medio emergindo como projecao e nao como hipotese inicial.

A parte computacional confirma que o modelo finito pode ser mapeado corretamente para qubits e oferece um caminho concreto para medir a qualidade do fechamento hierarquico. O resultado numerico inicial mostra que os setores residuais da hierarquia nao sao meramente formais: eles aparecem como diferencas mensuraveis na matriz de correlacao de pares.

Em termos de maturidade cientifica, o projeto esta em estagio de **manuscrito inicial forte**, ainda nao pronto para submissao, mas com uma tese clara, uma estrutura teorica defensavel e uma extensao computacional promissora.
