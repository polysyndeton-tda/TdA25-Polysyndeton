# TdA25-Polysyndeton
## Autoři
Petr Laškevič a Luka Králík

## Technologie
První částí aplikace je frontendové řešení,
které poskytuje možnost vytvářet, upravovat, procházet a především hrát
piškvorkové hry v lokálním multiplayeru. Využili jsme JavaScript
frameworku Svelte.js a jeho metaframeworku SvelteKit pro 
routing. Backendová služba zpracovává logiku herního modelu a komunikuje
ve formě REST API. Použitá technologie je Python framework Flask a 
databázovy systém SQLite.

## Spuštění aplikace
Pro spuštění nejdříve repozitář naklonujte.


Samotnou službu spustíte pomocí Dockeru:


```
docker build -t tda-app .
docker run -p 5000:5000 tda-app
```

## Dodatečné informace
Jedná se o Single Page Aplikaci (SPA), která komunikuje s logikou na straně serveru přes REST API.

