# genpark-image-token-cost-calculator-skill

Vision token budget and tile decomposition estimator for OpenAI GPT-4o, Claude 3.5 Sonnet, and Gemini multimodal architectures.

## Architecture

```mermaid
flowchart TD
    Dim[Image Dimensions W x H] --> Scaler[Aspect-Preserving Scaler]
    Scaler --> Tiler[512x512 Tile Decomposer]
    Tiler --> Tokens[Token Summation: Tiles * 170 + Base]
    Tokens --> Cost[Estimated USD Cost Output]
```

## Features
- **Accurate Tile Math**: Replicates exact tiling logic used by model API providers.
- **Detail Toggle**: Supports high and low detail vision modes.
