# Checklist de validação do STKSX2 (base ARMSX2)

## CI e APK

- [ ] GitHub Actions termina com sucesso no branch principal.
- [ ] O artefato `STKSX2-Android-universal-debug` contém um APK não vazio.
- [ ] O APK passa na verificação de assinatura e alinhamento executada pelo script upstream.
- [ ] O launcher mostra `STKSX2` e mantém os PNGs de ícone copiados do Play! anterior.
- [ ] Instalar o APK em um dispositivo de teste e abrir a biblioteca.

## Funcionalidade

- [ ] Importar e abrir um jogo próprio.
- [ ] Testar controles na tela e controle físico.
- [ ] Testar áudio, menu durante o jogo, configurações por jogo, salvar/carregar e encerramento.
- [ ] Confirmar comportamento de arquivos de jogos e saves; não presumir migração automática da versão anterior.
- [ ] Registrar o jogo, SoC/GPU, Android, backend gráfico, FPS médio, travamentos, temperatura e pico de memória.

## Segurança e distribuição

- Não incluir chaves de assinatura, senhas ou tokens no repositório.
- O script usa a assinatura de teste criada pelo construtor upstream; não é uma chave de publicação protegida para Play Store.
- Revisar as alterações e dependências upstream antes de distribuir APKs.
- Confirmar permissões Android, armazenamento de saves e tratamento de arquivos importados.

## Limites

- O build ainda não foi executado nem validado neste ambiente.
- O workflow usa a branch `master` do ARMSX2 e pode herdar alterações futuras do upstream.
- Não afirmar compatibilidade completa com NetherSX2 ou FPS garantido sem testes reais.
