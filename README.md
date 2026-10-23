# Ondafy HTTPS e Android App Links

Redirect URI obrigatória: `https://ionatasr0.github.io/ondafy/callback`.

O `index.html` existente foi preservado byte a byte. A publicação atual usa a branch `main`, raiz `/`. As alterações foram preparadas em `dev/ondafy-https-applinks`. O pedido de correção urgente autoriza integrar e publicar pela main; a simples existência da branch não publica os arquivos.

- `.nojekyll` mantém arquivos estáticos e o diretório `.well-known` na publicação por branch.
- `.well-known/assetlinks.json`: associação com `com.joojdevs.ondafy`, assinatura debug persistente do APK privado conferida por keytool e, na entrega, por apksigner. Nenhuma chave privada é publicada. Não é um certificado release definitivo. Um APK de CI assinado com outro debug certificado não será associado.
- `ondafy/callback/index.html`: página estática solicitada para recuperação, servida com HTTP 200 em `/ondafy/callback/` e `/ondafy/callback/index.html` após a publicação.
- `404.html`: mesma mensagem para o caminho exato ou rotas desconhecidas, sem retransmissão de parâmetros. O caminho sem barra `/ondafy/callback` pode receber o redirect canônico do Pages para `/ondafy/callback/`. A URI do Spotify **não muda**: o Android deve interceptar o App Link sem barra antes da requisição web. Uma resposta HTTP 200 da página ou o redirect do Pages não comprovam associação ou retorno ao aplicativo.

O App Link é resolvido pelo Android antes da navegação web. Se a verificação falhar, esta página não recupera ou retransmite códigos: remove query/fragment do endereço, mostra instruções para habilitar links e reiniciar o login. Não há analytics, fetch, cookies, armazenamento local, troca de tokens, intent URLs ou URI personalizada. A primeira requisição HTTP ao Pages poderá conter os parâmetros do callback quando o navegador for usado; um site estático não controla os logs e o cache da infraestrutura do GitHub. Não compartilhe URLs de autorização. A limpeza via history não apaga logs já recebidos pelo provedor.

## Validar após integrar e publicar

```sh
curl --fail --proto '=https' --max-redirs 0 -D headers.txt -o assetlinks.json https://ionatasr0.github.io/.well-known/assetlinks.json
python3 -m json.tool assetlinks.json
curl --proto '=https' --max-redirs 0 -D - -o /dev/null https://ionatasr0.github.io/ondafy/callback
```

A associação precisa retornar HTTP 200, `Content-Type: application/json`, JSON exato, sem redirecionamentos e sem autenticação. Depois executar a verificação no Galaxy M34 conforme o guia do aplicativo. A existência do JSON em uma branch não comprova a associação do domínio em um Android.

Fontes: [Android associações](https://developer.android.com/training/app-links/configure-assetlinks), [verificar App Links](https://developer.android.com/training/app-links/verify-applinks), [404 do Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site).
