# Checklist de validação do STKSX2

## CI

- [ ] GitHub Actions termina com sucesso no branch principal.
- [ ] O artefato `STKSX2-Android-debug-installable` contém um APK não vazio.
- [ ] Instalar o APK em um dispositivo de teste e confirmar que o launcher mostra STKSX2.
- [ ] Abrir a aplicação, importar um jogo próprio e testar áudio, controles, suspensão/retorno e encerramento.
- [ ] Confirmar que os jogos e os dados salvos continuam disponíveis após atualizar o APK.

## Desempenho de aparelhos modestos

Para cada jogo, registrar modelo do aparelho, Android, SoC/GPU, configuração gráfica, FPS médio, 1% low, travamentos, temperatura e pico de memória. Testar ao menos 20–30 minutos para identificar throttling térmico. Não generalizar resultado de um jogo para todos os títulos.

## Segurança

- Não incluir chaves de assinatura, senhas ou tokens no repositório.
- Se uma chave de distribuição for configurada, guardar os dados em GitHub Actions Secrets e nunca em texto no código.
- Revisar alterações e dependências upstream antes de publicar APKs.
- Validar permissões Android, armazenamento de saves e tratamento de arquivos importados.
