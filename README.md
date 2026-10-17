# STKSX2 — pacote de compilação Android

**Estado real:** este repositório é um invólucro de compilação que baixa o código-fonte aberto do emulador **Play!** e tenta gerar um APK com referências de interface/nome **STKSX2** (o pacote interno permanece o original upstream). Não é um núcleo de PS2 escrito do zero nem uma versão do PCSX2/AetherSX2. A compilação remota ainda precisa ser executada no GitHub Actions para confirmar o resultado.

## O que está incluído

- Workflow de GitHub Actions para baixar o Play! com submódulos, instalar JDK/NDK/CMake, aplicar ajustes de interface para STKSX2 e compilar APK debug e release.
- O APK debug gerado pelo Gradle normalmente é assinado com a chave debug da compilação e serve para instalação de teste. O APK release pode sair sem assinatura de distribuição.
- Script que falha explicitamente se não conseguir aplicar o nome STKSX2, em vez de silenciosamente entregar um app com outro nome.
- Plano documentado para testes de desempenho em aparelhos de baixo custo.
- Pacote auxiliar de interface para Sketchware Pro. Ele **não** substitui o build nativo do emulador.

## Como compilar automaticamente

1. Crie um repositório no GitHub chamado `STKSX2`.
2. Extraia o conteúdo deste ZIP e envie **o conteúdo da pasta** para a raiz do repositório, incluindo `.github/workflows/android.yml`.
3. Abra a aba **Actions** e habilite Actions se o GitHub pedir.
4. Faça um commit/push para `main` ou `master`, ou abra o workflow **Build STKSX2 Android APK** e escolha **Run workflow**.
5. Quando terminar com sucesso, abra a execução e baixe o artefato **STKSX2-Android-debug-installable**. O APK estará dentro do ZIP de artefatos do GitHub Actions.

Se falhar, abra a execução em Actions e consulte o primeiro passo vermelho. Não há como confirmar o build até o workflow rodar no GitHub com acesso à internet e aos runners de compilação.

## Sketchware Pro

O arquivo `.swb` fornecido é somente um protótipo auxiliar e não deve ser tratado como um projeto completo/importável garantido para todas as versões do Sketchware Pro. O emulador real usa C++, CMake, Gradle e Android NDK; use GitHub Actions ou Android Studio para esse build.

## Desempenho e compatibilidade

O alvo é oferecer o melhor desempenho possível em aparelhos com menos de 4 GB de RAM, mas **não é tecnicamente honesto prometer 30 FPS em todos os jogos**. O resultado depende do jogo, CPU, GPU, driver, temperatura e compatibilidade do núcleo. Consulte `docs/LOW_END_OPTIMIZATION.md`; otimizações só devem ser anunciadas após medição em dispositivos reais.

## Licença, jogos e BIOS

O código do núcleo é obtido do projeto upstream Play!: https://github.com/jpd002/Play-. Consulte e preserve a licença, os avisos e as condições atuais desse projeto antes de redistribuir qualquer build. Este repositório não inclui jogos, imagens de disco ou firmware proprietário. O README do Play! informa que ele usa BIOS de alta-level integrada e não aceita BIOS externa: https://github.com/jpd002/Play-/blob/master/README.md.

## Limitações que continuam abertas

- O build ainda não foi executado nem validado neste ambiente.
- O núcleo continua sendo o upstream Play!, não uma implementação STKSX2 original.
- O pacote não inclui benchmarking por jogo, perfis de otimização próprios testados, testes de compatibilidade ou certificação de estabilidade.
- O nome do launcher é alterado; o identificador interno do pacote e os nomes internos upstream não são reescritos para evitar quebrar referências Java/JNI.
- O `.swb` é auxiliar e não compila o núcleo nativo.
