# Plano de otimização para aparelhos modestos

**Este documento é um plano de trabalho, não uma afirmação de que as otimizações já foram implementadas no núcleo.** O alvo são aparelhos Android com menos de 4 GB de RAM e CPUs/GPU antigas.

1. **Medir antes de alterar:** usar uma lista fixa de jogos que o usuário possui legalmente; registrar dispositivo, versão Android, SoC/GPU, FPS médio, 1% low, frame time, crashes, temperatura e pico de RAM.
2. **Escala de resolução:** testar resolução interna baixa/nativa quando o renderer suportar essa opção. Isso pode ajudar em gargalos de GPU, mas não corrige gargalos de CPU.
3. **Memória:** perfilar caches e alocações; limitar crescimento sem comprometer a correção; liberar recursos ao fechar o jogo e lidar com callbacks de pouca memória.
4. **CPU:** perfilar caminhos quentes do interpretador/recompilador antes de alterar algoritmos. Atalhos inseguros podem quebrar temporização e compatibilidade.
5. **Backend gráfico:** escolher backend suportado e estável por aparelho; não forçar Vulkan em drivers incompatíveis ou mais lentos.
6. **Perfis por jogo:** armazenar ajustes por título, com opção de restaurar padrões; não ativar hacks silenciosamente.
7. **Temperatura:** testar sessões de 20–30 minutos, não apenas benchmarks curtos, para detectar redução térmica de desempenho.

## Meta de FPS

30 FPS é uma meta para jogos/dispositivos que consigam sustentá-la, não uma garantia universal. A compatibilidade e o custo de emulação variam muito entre títulos e hardware.
