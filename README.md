# STKSX2 Alpha 1 — build Android com base ARMSX2/PCSX2

## O que esta adaptação faz

O workflow ativo é `.github/workflows/android.yml`. Ele baixa o código do ARMSX2 com submódulos, instala as dependências Android, prepara o nome visível `STKSX2`, reaproveita os PNGs do ícone do Play! usados pelo workflow anterior e chama o construtor oficial de APK universal do ARMSX2.

A base do emulador passa a ser **ARMSX2, derivada do PCSX2 para Android ARM64**. Isso é uma troca de núcleo/base de aplicativo, não uma atualização pequena do núcleo Play! anterior. A interface de configurações e o menu durante o jogo serão os que existem na versão upstream do ARMSX2, com os recursos implementados nessa versão. Não é uma cópia exata do NetherSX2 e não se afirma paridade de todas as opções.

## Compilação automática

1. Extraia o conteúdo desta pasta para a raiz do repositório GitHub, mantendo a pasta `.github/workflows/`.
2. Faça push para `main` ou `master`, ou abra **Actions → Build STKSX2 Android APK (ARMSX2 core) → Run workflow**.
3. Quando a execução terminar com sucesso, baixe o artefato `STKSX2-Android-universal-debug`.
4. Dentro do artefato estarão `STKSX2-Android-universal.apk` e `STKSX2-build-info.txt`.

O APK universal é montado a partir das variantes nativas ARM64 para páginas de memória de 4 KiB e 16 KiB pelo script upstream. O workflow falha se não encontrar ou validar o APK. A compilação ainda precisa rodar nos runners do GitHub para confirmar o resultado; este ZIP não contém um APK pré-compilado.

## Identidade e ícone

- Nome do launcher configurado como `STKSX2`.
- Identificador Android configurado como `com.stk.stksx2`.
- O script copia os PNGs de `ic_launcher` do código Play! utilizado pela versão anterior e aponta o manifesto para esses recursos. Ele falha se não encontrar os três tamanhos esperados, em vez de trocar silenciosamente o ícone.
- Não são alterados os arquivos de código do núcleo, os menus ou as configurações do ARMSX2 pelo script de branding.

**Nota sobre atualização:** como o identificador do pacote muda para `com.stk.stksx2`, o Android pode tratar o APK como um aplicativo separado do APK anterior. Os saves e as configurações não são migrados automaticamente. Faça backup antes de testar.

## Limites importantes

- O ZIP original continha um protótipo `MainActivity.java`, documentação e scripts; não continha o núcleo de emulação completo. O workflow anterior buscava o Play! durante a compilação.
- O workflow novo baixa o ARMSX2 a partir da branch upstream `master`. Assim, menus e recursos podem mudar conforme o upstream evolui.
- Não foi possível compilar o APK neste ambiente. A validade final depende da execução completa do GitHub Actions e de testes no dispositivo real.
- Não é possível prometer FPS específico em todos os jogos. Desempenho depende do jogo, SoC, GPU, driver, temperatura e configurações.
- Este pacote não implementa automaticamente todos os recursos exclusivos do NetherSX2, não migra saves e não garante equivalência visual com a interface anterior. Recursos adicionais devem ser integrados ao núcleo e testados, não apresentados como simples opções visuais.

## Teste recomendado

1. Baixe e instale o APK do artefato.
2. Teste a abertura, a biblioteca de jogos, os controles na tela, um controle físico, áudio, salvar/carregar e voltar do jogo para o menu.
3. Teste o jogo que apresentou baixo desempenho no aparelho real e registre FPS, temperatura, travamentos e configuração gráfica.
4. Se o workflow falhar, abra o log do primeiro passo vermelho em **Actions**; o arquivo `STKSX2-build-info.txt` só será publicado quando a compilação chegar ao estágio de empacotamento.

## Licenças

Preserve os avisos e licenças dos projetos upstream. Este repositório não inclui jogos, discos de jogos nem firmware proprietário.
