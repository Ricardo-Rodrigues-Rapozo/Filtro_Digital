# Projeto de interpolacao e banco de filtros para FPGA

Este repositorio contem a implementacao de um fluxo de processamento de sinais para estimacao fasorial/harmonica, com foco em validacao por simulacao e posterior embarque completo em uma placa com FPGA.

O projeto e desenvolvido em duas frentes:

- **Python**: modelo de referencia numerica, geracao de sinais de teste, validacao do algoritmo e calculo de metricas como erro de magnitude, erro de fase e TVE.
- **CMM/SAPHO**: implementacao do algoritmo para geracao de hardware. Os codigos CMM sao compilados pelo SAPHO/Aurora e geram os modulos Verilog e arquivos de memoria usados na simulacao.

A versao do SAPHO/Aurora usada como base e a do repositorio:

https://github.com/nipscernlab/aurora.git

## Visao geral

A ideia do projeto e implementar uma cadeia de processamento que recebe um sinal eletrico amostrado, estima a frequencia por cruzamento por zero, aplica suavizacao, faz interpolacao B-Spline/Farrow e alimenta um banco de filtros polifasico/FFT para extrair componentes harmonicas. O objetivo final e levar essa cadeia inteira para hardware em FPGA.

O fluxo recomendado e:

1. Validar o comportamento matematico no Python.
2. Portar/ajustar a implementacao em CMM.
3. Validar o CMM comparando os resultados com o modelo Python.
4. Gerar o Verilog pelo SAPHO/Aurora.
5. Simular o hardware gerado.
6. Integrar e sintetizar para FPGA.

Os testes do hardware devem ser feitos depois da validacao do CMM contra o Python, pois o Python funciona como referencia do algoritmo.

## Estrutura do repositorio

- `Python/`: scripts de referencia e geracao de sinais.
  - `principal_Naiara.py`: fluxo principal em Python para geracao do sinal, estimacao de frequencia, interpolacao, banco de filtros e calculo de erros.
  - `DSPEPS.py`: funcoes de DSP usadas no modelo Python.
  - `sinaisIEC60255_118.py`: geracao de sinais de teste baseados na IEC/IEEE 60255-118.
  - `gerar_rampa.py`: geracao de caso de rampa de frequencia.
- `proc_interp/`: processador CMM/Verilog do interpolador.
  - `Software/proc_interp.cmm`: codigo CMM do interpolador.
  - `Hardware/proc_interp.v`: Verilog gerado pelo SAPHO/Aurora.
  - `Simulation/proc_interp_tb.v`: testbench individual.
- `proc_banco/`: processador CMM/Verilog do banco de filtros.
  - `Software/proc_banco.cmm`: codigo CMM do banco de filtros/FFT.
  - `Hardware/proc_banco.v`: Verilog gerado pelo SAPHO/Aurora.
  - `Simulation/proc_banco_tb.v`: testbench individual.
- `top_level.v`: integracao dos blocos do projeto.
- `top_level_tb.v`: testbench do sistema integrado.
- `interpolador.spf`: projeto do SAPHO/Aurora.
- `sinal_teste.txt`: sinal de entrada usado na simulacao integrada.
- `saida_interp*.txt`: saidas geradas pela simulacao do interpolador.

## Dependencias

Para o modelo Python:

```powershell
cd Python
python -m pip install numpy scipy matplotlib plotly
```

Para a parte CMM/Verilog:

- SAPHO/Aurora da versao indicada acima.
- Simulador Verilog, como ModelSim/Questa ou ferramenta equivalente.
- Ferramentas de FPGA, por exemplo Quartus, para sintese e implementacao na placa.

## Ajuste obrigatorio de caminhos

Este projeto possui caminhos absolutos gerados pelo SAPHO/Aurora. Antes de rodar em outro computador ou em outro diretorio, altere os caminhos nos arquivos `.v`, `.spf` e `.json` para apontarem para o diretorio local do usuario.

Exemplo: trocar ocorrencias como:

```text
C:/Users/Ricardo/Documents/projeto_completo/projeto_completo
```

ou:

```text
C:\Users\Ricardo\Documents\projeto_completo\projeto_completo
```

pelo caminho real onde o repositorio esta salvo, por exemplo:

```text
C:/Users/<usuario>/Documents/Dissertacao
```

Arquivos que atualmente precisam de atencao:

- `top_level_tb.v`: caminhos de leitura de `sinal_teste.txt` e escrita de `saida_interp*.txt`.
- `proc_interp/Simulation/proc_interp_tb.v`: caminhos de `input_0.txt` e `output_*.txt`.
- `proc_banco/Simulation/proc_banco_tb.v`: caminhos de `input_0.txt` e `output_*.txt`.
- `proc_interp/Hardware/proc_interp.v`: parametros `DFILE` e `IFILE`.
- `proc_banco/Hardware/proc_banco.v`: parametros `DFILE` e `IFILE`.
- `interpolador.spf`: `projectPath`, `basePath`, `topLevelFile`, `testbenchFile` e listas de arquivos.
- `testbench/*.json`: caminhos de testbench usados pela configuracao do projeto.

Se esses caminhos nao forem atualizados, a simulacao pode abrir arquivos errados ou falhar ao carregar memorias `.mif`.

## Como rodar

### 1. Validar no Python

Execute o modelo de referencia:

```powershell
cd Python
python principal_Naiara.py
```

Esse script gera sinais, executa a cadeia de processamento em Python e mostra graficos de frequencia, interpolacao, magnitude, fase e TVE. Para testes de rampa:

```powershell
python gerar_rampa.py
```

Se um novo sinal for gerado para o SAPHO/Verilog, copie ou aponte o testbench para o arquivo correto de entrada.

### 2. Validar e gerar os processadores no SAPHO/Aurora

Abra `interpolador.spf` no SAPHO/Aurora, ajuste os caminhos absolutos e gere novamente os blocos dos processadores quando alterar os arquivos CMM:

- `proc_interp/Software/proc_interp.cmm`
- `proc_banco/Software/proc_banco.cmm`

A geracao atualiza os arquivos Verilog e memorias em:

- `proc_interp/Hardware/`
- `proc_banco/Hardware/`

### 3. Simular em Verilog

Compile os modulos gerados e os arquivos de topo no simulador Verilog. No ModelSim/Questa, o fluxo geral e:

```tcl
vlib work
vlog <arquivos_do_sapho_aurora> proc_interp/Hardware/proc_interp.v proc_banco/Hardware/proc_banco.v top_proc_interp.v top_proc_banco.v maq_estados.v top_level.v top_level_tb.v
vsim -c top_level_tb -do "run -all; quit -f"
```

Os arquivos do SAPHO/Aurora devem incluir os modulos de suporte usados pelo Verilog gerado, como `processor` e `addr_dec`. Sem esses modulos, a simulacao falha ao carregar o projeto.

As saidas principais da simulacao integrada sao:

- `saida_interp0.txt`
- `saida_interp1.txt`
- `saida_interp2.txt`
- `saida_interp3.txt`
- `saida_interp4.txt`

## Observacoes importantes

- Sempre confira se os arquivos de entrada e saida dos testbenches apontam para o diretorio correto.
- A escala dos sinais e saidas e definida nos scripts Python e nos `fout` dos arquivos CMM.
- O top-level atual instancia principalmente o caminho do interpolador; a integracao completa com o banco de filtros esta parcialmente preparada/comentada em `top_level.v`.
- Antes de sintetizar para FPGA, valide a equivalencia entre Python, CMM e Verilog para o caso de teste escolhido.
